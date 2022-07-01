CREATE TABLE bancoproj.users
(
    id      SERIAL          NOT NULL,
    hash_password    VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL
);

ALTER TABLE bancoproj.users
    ADD CONSTRAINT users_pk
        PRIMARY KEY (id);

CREATE UNIQUE INDEX users_id_uindex
    ON bancoproj.users (id);

CREATE UNIQUE INDEX users_email_uindex
    ON bancoproj.users (email);

CREATE TABLE bancoproj.authors
(
    author_id      INT          NOT NULL,
    name    VARCHAR(100) NOT NULL,
    picture INT          NOT NULL
);

CREATE UNIQUE INDEX authors_id_uindex
    ON bancoproj.authors (author_id);

ALTER TABLE bancoproj.authors
    ADD CONSTRAINT authors_pk
        PRIMARY KEY (author_id);

CREATE TABLE bancoproj.papers
(
    paper_id              INT          NOT NULL,
    category        VARCHAR(100) NOT NULL,
    title           VARCHAR(100) NOT NULL,
    summary         VARCHAR(100) NOT NULL,
    first_paragraph VARCHAR(255) NOT NULL,
    body            VARCHAR NOT NULL
);

CREATE UNIQUE INDEX papers_id_uindex
    ON bancoproj.papers (paper_id);

ALTER TABLE bancoproj.papers
    ADD CONSTRAINT papers_pk
        PRIMARY KEY (paper_id);
