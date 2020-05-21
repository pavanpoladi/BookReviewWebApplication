import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#Connect to the database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#Function to read from csv full of books and their info, and add the info to the database
def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader) #skip first line of csv since they are just headers
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", 
        {"isbn": isbn, "title": title, "author": author, "year": year})
        print("Sucessfully added: {}".format(title))
    db.commit()

if __name__ == "__main__":
    main()