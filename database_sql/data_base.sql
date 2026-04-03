CREATE DATABASE nickname_generator;

USE nickname_generator;

CREATE TABLE words (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(255) NOT NULL,
    type ENUM('base', 'prefix', 'suffix', 'emotional') NOT NULL
);

INSERT INTO words (word, type) VALUES
('zxc', 'prefix'),
('king', 'prefix'),
('less', 'suffix'),
('love', 'emotional'),
('hope', 'emotional'),
('love', 'emotional');

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),

    nicknames_generated INT DEFAULT 0,
    builds_created INT DEFAULT 0
);