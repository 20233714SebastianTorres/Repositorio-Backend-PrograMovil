-- migrate:up

INSERT INTO movies (
    id,
    title,
    year,
    synopsis,
    genre,
    duration,
    average_rating,
    poster,
    director,
    actors,
    trailer_url
)
VALUES
(
    1,
    'Interstellar',
    2014,
    'Viaje espacial para salvar a la humanidad.',
    'Ciencia Ficcion',
    169,
    4.8,
    'img/movies/interstellar.jpg',
    'Christopher Nolan',
    '["Matthew McConaughey","Anne Hathaway","Jessica Chastain"]',
    'https://youtube.com/watch?v=zSWdZVtXT7E'
),
(
    2,
    'The Dark Knight',
    2008,
    'Batman enfrenta al Joker.',
    'Accion',
    152,
    4.9,
    'img/movies/dark_knight.jpg',
    'Christopher Nolan',
    '["Christian Bale","Heath Ledger","Gary Oldman"]',
    'https://youtube.com/watch?v=EXeTwQWrcwY'
);

-- migrate:down

DELETE FROM movies;