-- Add migration script here
CREATE TABLE page(
    title text NOT NULL,
    keywords text,
    id uuid,
    description text,
    author text,
    url text NOT NULL PRIMARY KEY
);