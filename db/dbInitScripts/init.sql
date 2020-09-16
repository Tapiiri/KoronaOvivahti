CREATE TABLE Spaces (
    id SERIAL PRIMARY KEY, 
    title TEXT, 
    handle TEXT UNIQUE,
    owner_id INT, 
    date DATE
    );
CREATE TABLE Users (
    id SERIAL PRIMARY KEY, 
    tg_id INT UNIQUE,
    handle TEXT, 
    name TEXT
    );
CREATE TABLE DoorEvents (
    id SERIAL PRIMARY KEY, 
    created_at TIMESTAMP, 
    event_id INT, 
    user_id INT, 
    in_or_out BOOLEAN
    );
CREATE TABLE Admins (
    id SERIAL PRIMARY KEY, 
    created_at TIMESTAMP, 
    event_id INT, 
    user_id INT,
    approving_admin_id INT,
    admin_status BOOLEAN
);