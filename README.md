# SQL and Python: The Workshop

This is the information and code for the Python North West workshop, held on 19th May 2022.

Before starting, ensure you have a suitable Python environment and a code editor to hand. We'll also be [SQLite Browser](https://sqlitebrowser.org/) for our SQL queries and viewing the SQLite database. There are install instructions on the website.

Next up, download the [SnakeReads book database](https://github.com/PythonNorthwestEngland/python-and-sql-workshop/releases/download/01_data/books.db).

For the first part of the workshop we'll be learning how to explore the database and insert new data.

In the second part of the workshop we'll take what we've learned and create a Python script to read from the database and insert data.

## Part One

We'll be learning about the main "CRUD" operations and exploring the SnakeReads database.

### Create

INSERT statements

### Read

SELECT statements

### Update

UPDATE statements

### Delete

DELETE statements

### Joining across tables

Link tables together to get more information using [JOIN statements](https://www.geeksforgeeks.org/sql-join-set-1-inner-left-right-and-full-joins/).

First, let's try some querying

1. Open the database
2. Go to the "Execute SQL" tab
3. Type in `SELECT book_id, title, authors FROM books WHERE original_publication_year = 1937;`

4. `SELECT book_id, title, authors FROM books WHERE title like '%hitchhiker%'`

Now lets try adding some data.  This data set is missing python books!

1. Replace that entered SQL with `INSERT INTO books(authors, title, original_title, original_publication_year, isbn13) VALUES ('Luciano Ramalho', 'Fluent Python', 'Fluent Python', 2015, '9781491946008')`

We can also delete out data

1. `DELETE FROM books WHERE original_publication_year = 2000; -- the millenium was overrated`

### aggregations

How many reviews do we have?

`SELECT count(*) FROM ratings`

and for the hobbit?

`SELECT count(*) FROM ratings WHERE book_id = 7`

What else can we do?

`SELECT avg(rating) FROM ratings`

Not so useful, this is our average rating across all books

`SELECT book_id, avg(rating) as avg_rating FROM ratings GROUP BY book_id ORDER BY avg_rating DESC`

But we have IDS so join!

```
with best_books as (
	SELECT book_id, avg(rating) as avg_rating FROM ratings GROUP BY book_id ORDER BY avg_rating DESC LIMIT 5
)
SELECT
	books.book_id,
	books.title,
	books.authors,
	avg_rating
FROM best_books
LEFT JOIN books ON best_books.book_id = books.book_id;
```

## Part Two

We'll be using sqlite3 to talk to our database, which is part of the Python standard library. The docs are [here](https://docs.python.org/3/library/sqlite3.html)

(Note: you may want to explore using the third-party pysqlite3 library, as this has some nice additional features. It can be installed via `pip install pysqlite3-binary`. More information can be found [here](https://github.com/coleifer/pysqlite3)

Use [this code](https://github.com/PythonNorthwestEngland/python-and-sql-workshop/blob/main/sqlite_python.py) to setup a connection to your books database.

