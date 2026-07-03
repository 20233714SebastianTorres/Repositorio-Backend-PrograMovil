-- migrate:up

INSERT INTO watched_movies (
    id,
    watched_date,
    user_id,
    movie_id
)
VALUES
(
    1,
    '2025-06-10',
    1,
    1
),
(
    2,
    '2025-06-12',
    1,
    2
),
(
    3,
    '2025-06-15',
    2,
    1
);

-- migrate:down

DELETE FROM watched_movies;