-- migrate:up

INSERT INTO reviews (
    id,
    content,
    rating,
    user_id,
    movie_id
)
VALUES
(
    1,
    'Excelente película.',
    5,
    1,
    1
),
(
    2,
    'Una obra maestra.',
    4.5,
    2,
    1
),
(
    3,
    'El mejor Batman.',
    5,
    1,
    2
);

-- migrate:down

DELETE FROM reviews;