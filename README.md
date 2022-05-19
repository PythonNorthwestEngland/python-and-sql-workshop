# SQL and Python: The Workshop

This is the information and code for the Python North West workshop, held on 19th May 2022.

Before starting, ensure you have a suitable Python environment and a code editor to hand. We'll also be [SQLite Browser](https://sqlitebrowser.org/) for our SQL queries and viewing the SQLite database. There are install instructions on the website.

Next up, download the ~~GoodReads~~ [SnakeReads book database](https://github.com/PythonNorthwestEngland/python-and-sql-workshop/releases/download/01_data/books.db).

For the first part of the workshop we'll be learning how to explore the database and insert new data.

In the second part of the workshop we'll take what we've learned and create a Python script to read from the database and insert data.

## Part One

We'll be learning about the main "CRUD" operations and exploring the SnakeReads database.

### Read


First, let's try some querying or reading data

1. Open the database
2. Go to the "Execute SQL" tab
3. Type in `SELECT book_id, title, authors FROM books WHERE original_publication_year = 1937;`

4. `SELECT book_id, title, authors, original_publication_year FROM books WHERE authors like '%iain%banks%'`
5. `SELECT book_id, title, authors, original_publication_year FROM books WHERE authors like '%iain%banks%' ORDER BY original_publication_year`
6. `SELECT book_id, title, authors, original_publication_year FROM books WHERE authors like '%iain%banks%' ORDER BY original_publication_year LIMIT 5`

### Create

Now lets try adding some data.  This data set is missing python books!

1. Replace that entered SQL with `INSERT INTO books(authors, title, original_title, original_publication_year, isbn13) VALUES ('Luciano Ramalho', 'Fluent Python', 'Fluent Python', 2015, '9781491946008') returning book_id`

Feel free to replace those things with your own favourite python book, or other book!

### Update

UPDATE statements - changing something.  Let's give Luciano his full name:

```sql
UPDATE books
SET authors = 'Luciano Gama de Sousa Ramalho'
WHERE book_id=<that book_id>
```

### Delete

We can also delete out data. Let's say user_id 4000 has left our site:

1. `DELETE FROM ratings WHERE user_id = 4000;`

### Joining across tables

Link tables together to get more information using [JOIN statements](https://www.geeksforgeeks.org/sql-join-set-1-inner-left-right-and-full-joins/).


Which books are on user #315's to read pile?

`SELECT book_id FROM to_read WHERE user_id = 315`

... whole bunch of IDs, not so helpful.  We could look them up 'by hand', as it were:

```sql
SELECT
  book_id,
  title,
  authors
FROM books
WHERE book_id IN (
	54,
	374,
	1758,
	1941,
	2218,
	6082
)
```

But a join does this for us!

```sql
SELECT
  books.book_id,
  title,
  authors
FROM to_read
LEFT JOIN books ON books.book_id = to_read.book_id
WHERE user_id = 315
```


### aggregations

How many books are on people's to read pile?

`SELECT count(*) FROM to_read`

and for the hobbit? You might recall from ealier it has a `book_id` of 7

`SELECT count(*) FROM to_read WHERE book_id = 7`

What else can we do?  Lets go to the ratings table:

`SELECT avg(rating) FROM ratings`

Not so useful, this is our average rating across all books.  It's quite high (almost 4!) but this is the "best books" extract.

So lets use `GROUP BY` to compute it per book (And a `LIMIT` clause to get the top 5):

```sql
SELECT
    book_id,
    avg(rating) as avg_rating
FROM ratings
GROUP BY book_id
ORDER BY avg_rating DESC
LIMIT 5
```

This is perhaps still not very useful, it's just the book_id

### aggregations AND joins

But we have ids so, we can join!

```sql
-- this is a common table expression
-- that same query within a query
with best_books as (
SELECT
    book_id,
    avg(rating) as avg_rating
FROM ratings
GROUP BY book_id
ORDER BY avg_rating DESC
LIMIT 5
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

We'll be using the `sqlite3` module to talk to our database, which is part of the Python standard library. The docs are [here](https://docs.python.org/3/library/sqlite3.html)

(Note: you may want to explore using the third-party pysqlite3 library, as this has some nice additional features. It can be installed via `pip install pysqlite3-binary`. More information can be found [here](https://github.com/coleifer/pysqlite3)

Use [this code](https://github.com/PythonNorthwestEngland/python-and-sql-workshop/blob/main/sqlite_python.py) to setup a connection to your books database.

