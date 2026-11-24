import sqlite3
from datetime import datetime

BANCO = "clima.db"


def _conectar():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn


def iniciar_banco():
    with _conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS clima (
                cidade TEXT NOT NULL,
                data TEXT NOT NULL,
                temp_max REAL,
                temp_min REAL,
                chuva_mm REAL,
                vento_max REAL,
                tipo TEXT,
                atualizado_em TEXT,
                PRIMARY KEY (cidade, data)
            )
            """)


def salvar(cidade, registros):
    agora = datetime.now().isoformat(timespec="seconds")
    with _conectar() as conn:
        conn.executemany(
            """
            INSERT INTO clima
                (cidade, data, temp_max, temp_min, chuva_mm, vento_max, tipo, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(cidade, data) DO UPDATE SET
                temp_max = excluded.temp_max,
                temp_min = excluded.temp_min,
                chuva_mm = excluded.chuva_mm,
                vento_max = excluded.vento_max,
                tipo = excluded.tipo,
                atualizado_em = excluded.atualizado_em
            """,
            [
                (
                    cidade,
                    r["data"],
                    r["temp_max"],
                    r["temp_min"],
                    r["chuva_mm"],
                    r["vento_max"],
                    r["tipo"],
                    agora,
                )
                for r in registros
            ],
        )


def listar(cidade, limite=7):
    with _conectar() as conn:
        linhas = conn.execute(
            "SELECT * FROM (SELECT * FROM clima WHERE cidade = ? ORDER BY data DESC LIMIT ?) ORDER BY data",
            (cidade, limite),
        ).fetchall()
    return [dict(l) for l in linhas]
