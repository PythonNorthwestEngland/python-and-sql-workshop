# SQL and Python: The Workshop

This is the information and code for the Python North West workshop, held on 19th May 2022.

Before starting, ensure you have a suitable Python environment and a code editor to hand. We'll also be [SQLite Browser](https://sqlitebrowser.org/) for our SQL queries and viewing the SQLite database. There are install instructions on the website.

Next up, download the [SnakeReads book database](https://github.com/PythonNorthwestEngland/python-and-sql-workshop/releases/download/01_data/books.db).

For the first part of the workshop we'll be learning how to explore the database and insert new data.

In the second part of the workshop we'll take what we've learned and create a Python script to read from the database and insert data.

## Part One

-- details here

## Part Two

We'll be using sqlite3 to talk to our database, which is part of the Python standard library. The docs are [here](https://docs.python.org/3/library/sqlite3.html)

(Note: you may want to explore using the third-party pysqlite3 library, as this has some nice additional features. It can be installed via `pip install pysqlite3-binary`. More information can be found [here](https://github.com/coleifer/pysqlite3)

Use [this code](https://github.com/PythonNorthwestEngland/python-and-sql-workshop/blob/main/sqlite_python.py) to setup a connection to your books database.

