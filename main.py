"""NoryxPlay - automação de testes de criativos na Meta.

Uso:
  python main.py collect   # baixa vídeos novos do grupo do Telegram
  python main.py upload    # repõe criativos nos números sem anúncio ativo
  python main.py rules     # valida o criativo bom e pausa os outros
  python main.py retry     # libera para nova tentativa os uploads que deram erro
  python main.py run       # loop contínuo com tudo acima
"""
from __future__ import annotations

import argparse
import logging
import time

from noryx import config, db, rules, uploader
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
    p.add_argument("command", choices=["collect", "upload", "rules", "retry", "run"])
    p.add_argument("--config", default="config.yaml")
    p.add_argument("--interval", type=int, default=15, help="minutos entre ciclos no modo run")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    s = config.load(args.config)
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
