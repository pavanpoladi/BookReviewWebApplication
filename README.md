# Project 1

A video demo of this Project is included in the uploaded files

In this project I created a book review web application where users can register, login, search for books, see reviews for those books along with writing their own reviews, see Average ratings and other information for books using a GoodReads API, and finally get information directly from this website using its very own api.

To start off, users can register using a username and password, and then go ahead and login using the same information. A message will pop up telling the user if the information they entered is incorrect. Once the user closes the application or goes back to the home page, they will automatically be logged out.

After logging in users can search for books by typing in the book's title, author, ISBN, or any part of what I just mentioned. For example If I type in "cold" a list of books will pop up that all contain the word "cold".

Once a user clicks on the book they will be taken to a page that displays various information about the book, as well as the average rating and number of ratings the book has recieved from a GoodReads API. The user will also see reviews posted by other users and also write his own review for the book. Each user will only be allowed to write one review per book and a message will pop up telling the user this if he tries to write more than one review for a book.

Lastly if the user changes the route to /api/ where isbn is the ISBN number of a book, the web application returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score, so that users can also use information directly from this web application.
