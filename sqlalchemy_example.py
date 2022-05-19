# adapted from https://docs.sqlalchemy.org/en/14/orm/tutorial.html

from sqlalchemy import Column, Integer, String, create_engine, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///books.db", echo=True)

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, name="book_id")
    books_count = Column(Integer)
    isbn = Column(String)
    isbn13 = Column(String)
    authors = Column(String)
    original_publication_year = Column(Integer)
    original_title = Column(String)
    title = Column(String)
    language_code = Column(String)


class Rating(Base):
    __tablename__ = "ratings"
    book_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    rating = Column(Integer)


class ToRead(Base):
    __tablename__ = "to_read"
    book_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)


# make tables if we need to
Base.metadata.create_all(engine)

# make a sessionmaker
Session = sessionmaker(bind=engine)

# ... and a session
session = Session()

# query
print("QUERY ==========================================================")
for instance in (
    session.query(Book.title, Book.authors)
    .order_by(Book.id)
    .filter(Book.original_publication_year == 1937)
):
    print(f'"{instance.title}", by {instance.authors}')
print("QUERY END ======================================================")

session.add(
    Book(
        title="Spot's First Christmas",
        authors="Eric Hill",
        original_publication_year=1983,
    )
)
session.commit()
