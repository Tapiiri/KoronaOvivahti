CREATE TABLE Spaces (
    id SERIAL PRIMARY KEY, 
    title TEXT, 
    owner INT, 
    date DATE
    );
CREATE TABLE Users (
    id SERIAL PRIMARY KEY, 
    handle TEXT, 
    name TEXT,
    chatState TEXT
    );
CREATE TABLE DoorEvents (
    id SERIAL PRIMARY KEY, 
    createdAt TIMESTAMP, 
    eventId INT, 
    userId INT, 
    inOrOut BOOLEAN
    );
CREATE TABLE Admins (
    id SERIAL PRIMARY KEY, 
    createdAt TIMESTAMP, 
    eventId INT, 
    userId INT,
    approvingAdminId INT,
    AdminStatus BOOLEAN
);