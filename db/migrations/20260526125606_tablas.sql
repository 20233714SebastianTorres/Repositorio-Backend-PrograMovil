-- migrate:up

PRAGMA foreign_keys = ON;

CREATE TABLE sexs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(30)
);

CREATE TABLE nationalities (
id INTEGER PRIMARY KEY AUTOINCREMENT,
demonym VARCHAR(100)
);

CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR(50),
password VARCHAR(255),
first_name VARCHAR(100),
last_name VARCHAR(100),
email VARCHAR(255),
reset_key VARCHAR(100),
status BOOLEAN,
activation_key VARCHAR(100),
birth_date DATE,
profile_picture TEXT,
bio TEXT,
sex_id INTEGER,
nationality_id INTEGER,

```
FOREIGN KEY (sex_id) REFERENCES sexs(id),
FOREIGN KEY (nationality_id) REFERENCES nationalities(id)
```

);

CREATE TABLE movies (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(255),
year INTEGER,
synopsis TEXT,
genre VARCHAR(100),
duration INTEGER,
average_rating FLOAT,
poster TEXT,
director VARCHAR(255),
actors TEXT,
trailer_url TEXT
);

CREATE TABLE reviews (
id INTEGER PRIMARY KEY AUTOINCREMENT,
content TEXT,
rating FLOAT,
user_id INTEGER,
movie_id INTEGER,

```
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (movie_id) REFERENCES movies(id)
```

);

CREATE TABLE watched_movies (
id INTEGER PRIMARY KEY AUTOINCREMENT,
watched_date DATE,
user_id INTEGER,
movie_id INTEGER,

```
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (movie_id) REFERENCES movies(id)
```

);

-- migrate:down

DROP TABLE IF EXISTS watched_movies;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS nationalities;
DROP TABLE IF EXISTS sexs;
