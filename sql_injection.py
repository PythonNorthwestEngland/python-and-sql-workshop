"""
This file shows SQL injection

I've just used the module as is, to keep it simpler
"""

import sqlite3


def print_rows(cursor):
    """
    helper method to print rows
    """
    for row in cursor:
        print(", ".join(str(r) for r in row))


# connect
conn = sqlite3.connect(
    "books.db",
)

print("== Working example ========================== ")
title = "The Hobbit"

cur = conn.execute(
    f"""
    SELECT book_id, title, authors
    FROM books
    WHERE title = '{title}'
    LIMIT 10
    """
)

print_rows(cur)
print()
print()


print("== Working example ========================== ")
title = "The Hobbit' OR 1=1 --"

cur = conn.execute(
    f"""
    SELECT book_id, title, authors
    FROM books
    WHERE title = '{title}'
    LIMIT 10
    """
)

print_rows(cur)
print()
print()

print("== With parameters ========================== ")
title = "The Hobbit' OR 1=1 --"

cur = conn.execute(
    """
    SELECT book_id, title, authors
    FROM books
    WHERE title = :title
    LIMIT 10
    """,
    {"title": title},
)

print_rows(cur)
