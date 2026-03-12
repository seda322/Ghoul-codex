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