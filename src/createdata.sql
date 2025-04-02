-- Tạo database
CREATE DATABASE IF NOT EXISTS english;
USE english;

-- Tạo bảng user
CREATE TABLE IF NOT EXISTS user (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    admin TINYINT(1) DEFAULT 0
);

-- Tạo bảng words
CREATE TABLE IF NOT EXISTS words (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(100) NOT NULL,
    meaning VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu cho bảng user
INSERT INTO user (username, email, password, admin) VALUES
('admin', 'admin@example.com', 'admin123', 1),
('user1', 'user1@example.com', '123', 0);

-- Thêm dữ liệu mẫu cho bảng words
INSERT INTO words (word, meaning) VALUES
('hello', 'xin chào'),
('goodbye', 'tạm biệt'),
('apple', 'quả táo'),
('book', 'sách');