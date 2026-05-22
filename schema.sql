CREATE DATABASE IF NOT EXISTS lab6_auth;
USE lab6_auth;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL UNIQUE,
  password VARCHAR(128) NOT NULL
);

INSERT IGNORE INTO users (username, password) VALUES ('admin', 'admin123');
INSERT IGNORE INTO users (username, password) VALUES ('dbuser', 'dbpass');
