--  Users Table
CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--  Documents Table
CREATE TABLE IF NOT EXISTS Documents (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'uploaded',
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

--  Content Table
CREATE TABLE IF NOT EXISTS Content (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL,
    original_content TEXT NOT NULL,
    improved_content TEXT,
    FOREIGN KEY (document_id) REFERENCES Documents(id) ON DELETE CASCADE
);


