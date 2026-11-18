"""Estado local em SQLite: criativos recebidos, uploads e ações das regras."""
from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS creatives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_file_unique_id TEXT UNIQUE NOT NULL,
    tg_message_id INTEGER,
    caption TEXT,
    product_key TEXT NOT NULL,
    variant TEXT,
    local_path TEXT,
    received_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creative_id INTEGER NOT NULL REFERENCES creatives(id),
    account_key TEXT NOT NULL,
    number_key TEXT NOT NULL,
    video_id TEXT,
    creative_meta_id TEXT,
    campaign_id TEXT,
    adset_id TEXT,
    ad_id TEXT,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending | done | error
    error TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(creative_id, account_key, number_key)
);
CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_id TEXT NOT NULL,  -- id do anúncio
    action TEXT NOT NULL,  -- pause | validate
    detail TEXT,
    day TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);
"""


def connect(data_dir: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(data_dir / "noryx.db")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def get_kv(conn: sqlite3.Connection, key: str, default: str = "") -> str:
    row = conn.execute("SELECT v FROM kv WHERE k = ?", (key,)).fetchone()
    return row["v"] if row else default


def set_kv(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute("INSERT INTO kv (k, v) VALUES (?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v", (key, value))
    conn.commit()
