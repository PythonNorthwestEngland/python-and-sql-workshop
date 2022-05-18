import sqlite3


def db_connect(database_name: str) -> sqlite3.Connection:
    db = sqlite3.connect(
        database_name,
        detect_types=sqlite3.PARSE_DECLTYPES,
        uri=database_name.startswith("file:"),
    )
    db.row_factory = sqlite3.Row

    db.execute("PRAGMA foreign_keys = ON;")

    return db


conn = db_connect("books.db")
