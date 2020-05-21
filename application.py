import os
import requests

from flask import Flask, session,flash, request, render_template, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

goodReadsKey = "K177sdmuIdt4Gzr1Y2T4gA"


#Home Route
@app.route("/", methods = ["GET", "POST"])
def index():
    session.clear()

    if(request.method == "POST"):
        if not request.form.get("username"):
            return render_template("index.html", danger_msg = "Did not enter username")
        elif not request.form.get("passwrd"):
            return render_template("index.html", danger_msg = "Did not enter password")
        
        else:
            username = request.form.get("username")
            user = db.execute("SELECT * FROM users WHERE username = :username;", {"username": username}).fetchone()
            if user == None:
                return render_template("index.html", danger_msg = "That user doesn't exist. Please try again.")
            else:
                passwrd = request.form.get("passwrd")
                user = db.execute("SELECT * FROM users WHERE passwrd = :passwrd;", {"passwrd": passwrd}).fetchone()
                if user == None:
                    return render_template("index.html", danger_msg = "That user doesn't exist. Please try again.")
                else:
                    session["user_id"] = user["id"]
                    return render_template("search.html", success_msg = "Login Successful")
    else:
        return render_template("index.html")


#Register Route
@app.route("/register", methods = ["GET", "POST"])
def register():
    session.clear

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("register.html", danger_msg = "Please enter username")
        elif not request.form.get("passwrd"):
            return render_template("register.html", danger_msg = "Please enter password")
        elif len(request.form.get("passwrd")) < 6:
            return render_template("register.html", danger_msg = "Please enter a password atleast 6 characters long")
        else:
            username = request.form.get("username")
            user = db.execute("SELECT * FROM users WHERE username = :username;", {"username": username}).fetchone()
            if user is None:
                passwrd = request.form.get("passwrd")
                db.execute("INSERT INTO users (username, passwrd) VALUES (:username, :passwrd)", 
                {"username": username, "passwrd": passwrd})
                db.commit()
                return render_template("index.html", success_msg = "Registration Success. Please login")
            else:
                return render_template("register.html", danger_msg = "This User already exists. Please try again")
    else:
        return render_template("register.html")


#Search Route
@app.route("/search", methods = ["POST"])
def search():
    if request.method == "POST":
        if request.form.get("searchInput"):
            search = request.form.get("searchInput").lower()  #using .lower() function to ignore case sensitivity
        if request.args.get("searchInput"):
            search = request.args.get("searchInput").lower()
        
        finalSearchInput = "%" + search + "%" # Using % sign allows search to see characters before and after user input
        books = db.execute("SELECT * FROM books WHERE lower(title) LIKE :searchInput OR lower(author) LIKE :searchInput OR lower(isbn) LIKE :searchInput", {"searchInput": finalSearchInput}).fetchall()
        return render_template("bookOptions.html", books = books)

    else:
        return render_template("search.html")


#Chosen Book Route
@app.route("/search/<int:chosenBookID>")
def chosenBook(chosenBookID):
    #using the chosenBookID run a query to get all the reviews for the book
    #return chosenBookReviews.html passing in all the reviews

    global chosenBook
    chosenBook = db.execute("SELECT* FROM books WHERE id = :id", {"id": chosenBookID}).fetchone()
    isbn = chosenBook["isbn"]

    ratingInfo = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"key": goodReadsKey, "isbns": isbn})
    officialRating = ratingInfo.json()["books"][0]

    reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": chosenBookID}).fetchall()
    listOfNames = []
    for review in reviews:
        userid = review["user_id"]
        user = db.execute("SELECT * FROM users WHERE id = :id", {"id": userid}).fetchone()
        username = user["username"]
        listOfNames.append(username)

    return render_template("reviewsForBook.html", chosenBook=chosenBook, reviews=reviews, officialRating=officialRating, listOfNames=listOfNames)

#Create Review Route
@app.route("/createReview/<int:chosenBookID>", methods = ["GET", "POST"])
def createReview(chosenBookID):
    if request.method == "POST":
        global chosenBook
        chosenBook = db.execute("SELECT* FROM books WHERE id = :id", {"id": chosenBookID}).fetchone()

        user_id = session["user_id"]
        txt = request.form.get("txt")
        number_of_stars = int(request.form.get("number_of_stars"))

        ratingInfo = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"key": goodReadsKey, "isbns": chosenBook["isbn"]})
        officialRating = ratingInfo.json()["books"][0]

        #user = db.execute("SELECT * FROM users where id = :id", {"id": userID}).fetchone()
        #personName = user.username

        reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": chosenBookID}).fetchall()
        listOfNames = []
        for review in reviews:
            userid = review['user_id']
            user = db.execute("SELECT * FROM users WHERE id = :id", {"id": userid}).fetchone()
            username = user["username"]
            listOfNames.append(username)
            #person_Name = review.personName
            #listOfNames.append(person_Name)
        
        reviewCheck = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": user_id, "book_id": chosenBookID}).fetchone()

        if reviewCheck is None:
            db.execute("INSERT INTO reviews (book_id, user_id, txt, number_of_stars) VALUES (:book_id, :user_id, :txt, :number_of_stars)", {"book_id": chosenBookID, "user_id": user_id, "txt": txt, "number_of_stars": number_of_stars})
            db.commit()
            reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": chosenBookID}).fetchall()
            listOfNames = []
            for review in reviews:
                userid = review['user_id']
                user = db.execute("SELECT * FROM users WHERE id = :id", {"id": userid}).fetchone()
                username = user["username"]
                listOfNames.append(username)
                #person_Name = review.personName
                #listOfNames.append(person_Name)
            
            return render_template("reviewsForBook.html", chosenBook=chosenBook, reviews=reviews, officialRating=officialRating, listOfNames=listOfNames, success_msg = "Review Successful")
        else:
            return render_template("reviewsForBook.html", chosenBook=chosenBook, reviews=reviews, officialRating=officialRating, listOfNames=listOfNames, danger_msg = "Review Failed. You can only write one review per book")


#API Route
@app.route("/api/<string:isbn>", methods = ["GET", "POST"])
def api(isbn):
    chosenBook = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn": isbn}).fetchone()
    if chosenBook is None:
        return jsonify({"error": "Invalid isbn"}), 404

    ratingInfo = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"key": goodReadsKey, "isbns": chosenBook["isbn"]})
    officialRating = ratingInfo.json()["books"][0]
    
    return jsonify(
    {
        "title": chosenBook.title,
        "author": chosenBook.author,
        "year": chosenBook.year, 
        "isbn": chosenBook.isbn,
        "average_score": officialRating["average_rating"],
        "review_count": officialRating["work_ratings_count"]
    })

