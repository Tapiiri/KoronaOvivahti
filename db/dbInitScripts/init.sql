CREATE TABLE spaces (
    id SERIAL PRIMARY KEY, 
    title TEXT, 
    handle TEXT UNIQUE,
    owner_id INT, 
    date DATE
    );

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    tg_id INT UNIQUE,
    handle TEXT, 
    name TEXT
    );

CREATE TABLE doorevents (
    id SERIAL PRIMARY KEY, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    space_id INT, 
    user_id INT, 
    in_or_out SMALLINT
    );

CREATE TABLE admins (
    id SERIAL PRIMARY KEY, 
    created_at TIMESTAMP, 
    space_id INT, 
    user_id INT,
    approving_admin_id INT,
    admin_status BOOLEAN
);