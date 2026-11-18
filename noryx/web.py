"""Painel web: enviar criativos pelo celular e ver como está a operação.

Rode com:  python main.py web   (porta 8080)
Protegido por senha (PANEL_PASSWORD no .env).
"""
from __future__ import annotations

import hmac
import os
import secrets
import uuid
from functools import wraps
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Flask, Response, flash, jsonify, redirect, render_template, request, session, url_for

from . import db, status
from .config import Settings

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}
MAX_UPLOAD_MB = 1024


def create_app(settings: Settings, password: str | None = None) -> Flask:
    password = password if password is not None else os.environ.get("PANEL_PASSWORD", "")
    if not password:
        raise SystemExit("Defina PANEL_PASSWORD no .env para proteger o painel.")

    app = Flask(__name__)
    app.secret_key = os.environ.get("PANEL_SECRET") or secrets.token_hex(32)
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
    videos_dir = settings.data_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

    def conn():
        return db.connect(settings.data_dir, check_same_thread=False)

    def login_required(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if not session.get("ok"):
                if request.path.startswith("/api/"):
                    return jsonify(error="login"), 401
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapper

    tz = ZoneInfo(os.environ.get("PANEL_TZ", "America/Sao_Paulo"))

    @app.template_filter("quando")
    def quando(value: str, only_time: bool = False) -> str:
        """'2026-11-18 03:34:00' (UTC) -> '18/11 00:34' no horário de Brasília."""
        if not value:
            return ""
        try:
            dt = datetime.fromisoformat(value.strip())
        except ValueError:
            return value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)  # o banco grava em UTC
        dt = dt.astimezone(tz)
        return dt.strftime("%H:%M" if only_time else "%d/%m %H:%M")

    @app.context_processor
    def common():
        return {"dry_run": settings.dry_run}

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            if hmac.compare_digest(request.form.get("password", ""), password):
                session["ok"] = True
                session.permanent = True
                return redirect(url_for("home"))
            flash("Senha errada.")
        return render_template("login.html")

    @app.route("/sair")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/")
    @login_required
    def home():
        c = conn()
        try:
            data = status.overview(c, settings)
        finally:
            c.close()
        return render_template("home.html", d=data)

    @app.route("/enviar")
    @login_required
    def send_page():
        return render_template("enviar.html", products=list(settings.products),
                               default_product=settings.default_product, max_label="1 GB")

    @app.post("/api/enviar")
    @login_required
    def api_send():
        product = request.form.get("product") or settings.default_product
        if product not in settings.products:
            return jsonify(error="Produto inválido"), 400
        variant = (request.form.get("variant") or "").strip()[:120]
        file = request.files.get("video")
        if not file or not file.filename:
            return jsonify(error="Nenhum vídeo enviado"), 400
        ext = Path(file.filename).suffix.lower()
        if ext not in VIDEO_EXT:
            return jsonify(error=f"Formato {ext or '?'} não aceito. Use MP4 ou MOV."), 400

        uid = uuid.uuid4().hex
        dest = videos_dir / f"web_{uid}{ext}"
        file.save(dest)
        label = variant or Path(file.filename).stem[:120]
        c = conn()
        try:
            cur = c.execute(
                "INSERT INTO creatives (tg_file_unique_id, caption, product_key, variant, local_path)"
                " VALUES (?, ?, ?, ?, ?)", (f"web:{uid}", file.filename, product, label, str(dest)))
            c.commit()
            cid = cur.lastrowid
        finally:
            c.close()
        return jsonify(ok=True, id=cid, name=label)

    @app.route("/manifest.json")
    def manifest():
        return jsonify({
            "name": "Noryx", "short_name": "Noryx", "start_url": "/", "display": "standalone",
            "background_color": "#0f1115", "theme_color": "#0f1115",
            "icons": [{"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml"}],
        })

    @app.route("/icon.svg")
    def icon():
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" '
               'fill="#4f7cff"/><path d="M24 18v28l22-14z" fill="#fff"/></svg>')
        return Response(svg, mimetype="image/svg+xml")

    @app.errorhandler(413)
    def too_big(_):
        return jsonify(error=f"Vídeo maior que {MAX_UPLOAD_MB} MB"), 413

    return app
