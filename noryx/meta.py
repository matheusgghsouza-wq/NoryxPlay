"""Cliente mínimo da Marketing API oficial da Meta (Graph API)."""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import requests

log = logging.getLogger(__name__)


class MetaError(RuntimeError):
    pass


class Meta:
    def __init__(self, token: str, version: str = "v23.0", dry_run: bool = True):
        self.token = token
        self.base = f"https://graph.facebook.com/{version}"
        self.video_base = f"https://graph-video.facebook.com/{version}"
        self.dry_run = dry_run
        self._fake = 0

    # ---------- baixo nível ----------
    def _request(self, method: str, path: str, base: str | None = None, files=None, **params):
        url = f"{base or self.base}/{path.lstrip('/')}"
        params = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in params.items()}
        params["access_token"] = self.token
        for attempt in range(4):
            if method == "GET":
                r = requests.get(url, params=params, timeout=120)
            else:
                r = requests.post(url, data=params, files=files, timeout=600)
            data = r.json() if r.content else {}
            err = data.get("error") if isinstance(data, dict) else None
            if not err:
                return data
            # 4/17/32/613 = limite de requisições: espera e tenta de novo
            if err.get("code") in (4, 17, 32, 613) and attempt < 3:
                time.sleep(30 * (attempt + 1))
                continue
            raise MetaError(f"{method} {path}: {err.get('message')} (code {err.get('code')})")

    def get(self, path: str, **params):
        return self._request("GET", path, **params)

    def post(self, path: str, base: str | None = None, files=None, **params):
        if self.dry_run:
            self._fake += 1
            fake_id = f"dry_{self._fake}"
            log.info("[DRY-RUN] POST %s %s -> %s", path, {k: v for k, v in params.items()}, fake_id)
            return {"id": fake_id, "copied_adset_id": fake_id, "success": True}
        return self._request("POST", path, base=base, files=files, **params)

    # ---------- criativos ----------
    def upload_video(self, ad_account_id: str, path: Path, title: str) -> str:
        with open(path, "rb") as f:
            res = self.post(f"act_{ad_account_id}/advideos", base=self.video_base,
                            files={"source": (path.name, f, "video/mp4")}, name=title)
        return res["id"]

    def wait_video_ready(self, video_id: str, timeout: int = 600) -> None:
        if self.dry_run:
            return
        start = time.time()
        while time.time() - start < timeout:
            status = self.get(video_id, fields="status").get("status", {}).get("video_status")
            if status == "ready":
                return
            if status == "error":
                raise MetaError(f"Processamento do vídeo {video_id} falhou")
            time.sleep(10)
        raise MetaError(f"Vídeo {video_id} não ficou pronto em {timeout}s")

    def video_thumbnail(self, video_id: str) -> str:
        if self.dry_run:
            return "https://example.com/thumb.jpg"
        thumbs = self.get(f"{video_id}/thumbnails").get("data", [])
        preferred = next((t for t in thumbs if t.get("is_preferred")), thumbs[0] if thumbs else None)
        if not preferred:
            raise MetaError(f"Vídeo {video_id} sem thumbnail")
        return preferred["uri"]

    def create_video_creative(self, ad_account_id: str, name: str, page_id: str, video_id: str,
                              thumb_url: str, message: str, headline: str, link: str, cta: str,
                              instagram_user_id: str = "") -> str:
        story = {
            "page_id": page_id,
            "video_data": {
                "video_id": video_id,
                "image_url": thumb_url,
                "message": message,
                "title": headline,
                "call_to_action": {"type": cta, "value": {"link": link}},
            },
        }
        if instagram_user_id:
            story["instagram_user_id"] = instagram_user_id
        return self.post(f"act_{ad_account_id}/adcreatives", name=name, object_story_spec=story)["id"]

    # ---------- estrutura de teste ----------
    def copy_adset(self, template_adset_id: str, new_name: str, status: str) -> str:
        res = self.post(f"{template_adset_id}/copies", deep_copy="false", status_option=status,
                        rename_options={"rename_strategy": "NO_RENAME"})
        adset_id = res.get("copied_adset_id") or res["id"]
        self.post(adset_id, name=new_name)
        return adset_id

    def create_ad(self, ad_account_id: str, name: str, adset_id: str, creative_id: str, status: str) -> str:
        return self.post(f"act_{ad_account_id}/ads", name=name, adset_id=adset_id,
                         creative={"creative_id": creative_id}, status=status)["id"]

    # ---------- leitura e ajustes ----------
    def adsets_insights(self, ad_account_id: str, date_preset: str = "today") -> list[dict]:
        rows, after = [], None
        while True:
            params = dict(level="adset", date_preset=date_preset, limit=500,
                          fields="adset_id,adset_name,spend,actions,action_values")
            if after:
                params["after"] = after
            data = self.get(f"act_{ad_account_id}/insights", **params)
            rows.extend(data.get("data", []))
            after = data.get("paging", {}).get("cursors", {}).get("after")
            if not data.get("paging", {}).get("next"):
                return rows

    def adset_info(self, adset_id: str) -> dict:
        return self.get(adset_id, fields="name,status,effective_status,daily_budget")

    def pause(self, object_id: str) -> None:
        self.post(object_id, status="PAUSED")

    def set_daily_budget(self, adset_id: str, budget_cents: int) -> None:
        self.post(adset_id, daily_budget=str(budget_cents))
