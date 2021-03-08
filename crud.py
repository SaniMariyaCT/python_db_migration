### crud.py ###
import config
import models
from sqlalchemy import create_engine
from datetime import datetime 


engine = create_engine(config.DATABASE_URI)       #engine

def recreate_database():                          #db create and recreate
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker           # session
Session = sessionmaker(bind=engine)

recreate_database()                         

book = models.Book(                                #first entry to table
    title='Deep Learning',
    author='Ian Goodfellow',
    pages=775,
    published=datetime(2016, 11, 18)
)
s = Session()

s.add(book)                                       #add and commit to db table
s.commit()
q1 = s.query(models.Book).first()
print(q1)

s.close_all()                                    # ending session to avoid dupication in entries
recreate_database()
s = Session()                                     

import yaml                                       # table entries to table from a yml file 

for data in yaml.load_all(open('books.yaml')):
    book = models.Book(**data)
    s.add(book)
    
s.commit()

q2 = s.query(models.Book).all()                  # querry     
print("\n All 5 entries in table \n" + str(q2) + "\n")                                        # to print the values in terminal

start_date = datetime(2009, 1, 1)                #filtering based on start and end date
end_date = datetime(2012, 1, 1)
q3 = s.query(models.Book).filter(models.Book.published.between(start_date, end_date)).all()
print("\n start and end date \n" + str(q3) + "\n")

from sqlalchemy import and_                      # and and or for querrying- import from sqlalchemy   
q4 = s.query(models.Book).filter(
    and_(
       models.Book.pages > 750,
       models.Book.published > datetime(2016, 1, 1)
    )
).all()
print("\n using AND \n" + str(q4) + "\n" )

q5 = s.query(models.Book).order_by(models.Book.pages.desc()).limit(3).all() 
print(q5)                                       # limit, orderby  

q6 = s.query(models.Book.id, models.Book.pages).all() 
print(q6)                                       # showing only required columns  - 'key not included - only values'
s.close_all()                                  
