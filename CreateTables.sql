CREATE TABLE books
(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    passwrd VARCHAR NOT NULL
);

CREATE TABLE reviews
(
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    txt VARCHAR NOT NULL,
    number_of_stars INTEGER NOT NULL
);
