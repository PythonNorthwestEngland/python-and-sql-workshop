from builtins import RuntimeError
import sqlite3

USER_ID = 100000


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


# connect to the database
conn = db_connect("books.db")

# Show there are no python books :(
cur = conn.execute(
    """
SELECT
book_id, title, authors, original_publication_year
FROM books
WHERE title like '%' || :title || '%' -- this allows safe, parameterised, wildcard queries
ORDER BY original_publication_year
LIMIT :limit
""",
    {"title": "python", "limit": 10},
)
for row in cur:
    print(f"{row['book_id']} {row['title']}")

print("== Inserting book==============================================")

# insert a python book successfully
# Also, insert this to our to_read pile
with conn:
    cur = conn.execute(
        """INSERT INTO books(authors, title, original_publication_year, isbn13)
                     VALUES (:authors, :title, :original_publication_year, :isbn13)
         returning book_id""",
        {
            "authors": "Harry J.W. Percival, Bob Gregory",
            "title": "Architecture Patterns With Python",
            "original_publication_year": 2020,
            "isbn13": "9781492052203",
        },
    )

    book_id = cur.fetchone()[0]
    print(f"New book id: {book_id}")

    cur = conn.execute(
        """INSERT INTO to_read(book_id, user_id)
                     VALUES (:book_id, :user_id)
         """,
        {
            "book_id": book_id,
            "user_id": USER_ID,
        },
    )

    cur = conn.execute(
        """
        SELECT * FROM to_read WHERE user_id = :user_id
        """,
        {"user_id": USER_ID},
    )
    print("to_read table (after the first insert):")
    for row in cur:
        print(f"{row['book_id']=} {row['user_id']=}")

print("== Inserting book with an error ========================================")


# insert a python book
# Also, insert this to our to_read pile
# but then we fail due to a RuntimeError :(
try:
    with conn:
        cur = conn.execute(
            """
            INSERT INTO books(authors, title, original_publication_year)
                    VALUES (:authors, :title, :original_publication_year)
            returning book_id
            """,
            {
                "authors": "Luciano Ramalho",
                "title": "Fluent Python",
                "original_publication_year": 2015,
            },
        )
        book_id = cur.fetchone()[0]
        print(f"New book id: {book_id}")

        # use this in our to_read insert statement
        cur = conn.execute(
            """INSERT INTO to_read(book_id, user_id)
                     VALUES (:book_id, :user_id)
         """,
            {
                "book_id": book_id,
                "user_id": USER_ID,
            },
        )

        cur = conn.execute(
            """
        SELECT * FROM to_read WHERE user_id = :user_id
        """,
            {"user_id": USER_ID},
        )
        print("to_read table (just before the error, still in the transaction):")
        for row in cur:
            print(f"{row['book_id']=} {row['user_id']=}")
        print("Both our books are in the to read pile")

        raise RuntimeError("Stop transaction")

except Exception:
    print("Ooops, we failed!")

print("== Querying after the error, outside the transaction =======================")

# Onlyone row in the to_read table
cur = conn.execute(
    """
SELECT * FROM to_read WHERE user_id = :user_id
""",
    {"user_id": USER_ID},
)
print("to_read table (just after the error):")
for row in cur:
    print(f"{row['book_id']=} {row['user_id']=}")

# Show there is a python book!
cur = conn.execute(
    """
SELECT
book_id, title, authors, original_publication_year
FROM books
WHERE title like '%' || :title || '%' -- this allows safe, parameterised, wildcard queries
ORDER BY original_publication_year
LIMIT :limit
""",
    {"title": "python", "limit": 10},
)
for row in cur:
    print(f"{row['book_id']} {row['title']} {row['authors']}")


conn.close()
