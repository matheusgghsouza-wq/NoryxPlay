"""NoryxPlay - automação de testes de criativos na Meta.

Uso:
  python main.py check     # confere tokens, contas, páginas e campanhas modelo (só lê)
  python main.py collect   # baixa vídeos novos do grupo do Telegram
  python main.py upload    # repõe criativos nos números sem anúncio ativo
  python main.py rules     # valida o criativo bom e pausa os outros
  python main.py retry     # libera para nova tentativa os uploads que deram erro
  python main.py run       # loop contínuo com tudo acima
  python main.py web       # painel no navegador/celular para enviar vídeos e acompanhar
"""
from __future__ import annotations

import argparse
import logging
import time

import sys

from noryx import check, config, db, rules, uploader
from noryx.meta import MetaPool
from noryx.telegram import Telegram

log = logging.getLogger("noryx")


def step_collect(s, conn, tg):
    new = tg.collect(conn)
    if new:
        tg.send(f"📥 {len(new)} criativo(s) novo(s) no banco. "
                "Vão entrar nos números que ficarem sem anúncio ativo.")


def step_upload(s, conn, tg, meta):
    lines = uploader.upload_all(conn, s, meta)
    if lines:
        tg.send(_header(s, "Reposição de criativos") + "\n".join(lines))


def step_rules(s, conn, tg, meta):
    if not s.auto_rules:
        return
    lines = rules.run(conn, s, meta)
    if lines:
        tg.send(_header(s, "Regras automáticas") + "\n".join(lines))


def _header(s, title):
    return f"{'[SIMULAÇÃO] ' if s.dry_run else ''}{title}\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", choices=["check", "collect", "upload", "rules", "retry", "run", "web"])
    p.add_argument("--config", default="config.yaml")
    p.add_argument("--interval", type=int, default=15, help="minutos entre ciclos no modo run")
    p.add_argument("--port", type=int, default=8080, help="porta do painel (modo web)")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    s = config.load(args.config)
    if args.command == "check":
        sys.exit(0 if check.run(s) else 1)
    if args.command == "web":
        from waitress import serve

        from noryx.web import create_app
        log.info("Painel em http://0.0.0.0:%s", args.port)
        serve(create_app(s), host="0.0.0.0", port=args.port, max_request_body_size=1100 * 1024 * 1024)
        return
    conn = db.connect(s.data_dir)
    tg = Telegram(s)
    meta = MetaPool(s)
    if s.dry_run:
        log.warning("dry_run ATIVO: nada será criado ou alterado na Meta.")

    if args.command == "collect":
        step_collect(s, conn, tg)
    elif args.command == "upload":
        step_upload(s, conn, tg, meta)
    elif args.command == "rules":
        step_rules(s, conn, tg, meta)
    elif args.command == "retry":
        n = conn.execute("DELETE FROM uploads WHERE status = 'error'").rowcount
        conn.commit()
        log.info("%s upload(s) com erro liberado(s) para nova tentativa.", n)
    else:
        while True:
            for step in (lambda: step_collect(s, conn, tg), lambda: step_rules(s, conn, tg, meta),
                         lambda: step_upload(s, conn, tg, meta)):
                try:
                    step()
                except Exception:  # noqa: BLE001 - o loop não pode morrer
                    log.exception("Erro no ciclo")
            time.sleep(args.interval * 60)


if __name__ == "__main__":
    main()
