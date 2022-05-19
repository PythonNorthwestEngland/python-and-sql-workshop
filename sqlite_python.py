import sqlite3


def db_connect(database_name: str) -> sqlite3.Connection:
    """
    Helper function to connect to sqlite3 from python

    This function mostly exists to set the `row_factory` option to
    allow 'string' or index based access of row elements and also
    to set the important PRAGMA foreign_keys to ON, which means
    the database will enforce foreign key constraints (an important
    data integrity measure across tables)

    """
    db = sqlite3.connect(
        database_name,
        detect_types=sqlite3.PARSE_DECLTYPES,
        uri=database_name.startswith("file:"),
    )
    db.row_factory = sqlite3.Row

    db.execute("PRAGMA foreign_keys = ON;")

    return db


conn = db_connect("books.db")
