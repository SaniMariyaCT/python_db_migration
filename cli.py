###  cli.py  ###
from models import Book
import config
from sqlalchemy import create_engine
engine = create_engine(config.DATABASE_URI)       
from sqlalchemy.orm import sessionmaker          
Session = sessionmaker(bind=engine)

s = Session()
books = s.query(Book).all()

for book in books:                                          ##runtime value entered in terminal
    price = input(f"Price for '{book.title}':$")
    book.price = price
    s.add(book)

s.commit() 
s.close()

s = Session()
q7 = s.query(Book.title, Book.price).all()
print(q7)
s.close()

