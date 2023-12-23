-- Створення таблиць
CREATE TABLE IF NOT EXISTS vehicle (
    number INT PRIMARY KEY,
    Machinery VARCHAR(50),
    Count INT,
    fuel INT,
    Manpower INT,
    num_rota INT,
    BK VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Persons (
    id INT PRIMARY KEY,
    FIO VARCHAR(255),
    size_clothes INT,
    size_shoes INT,
    serial_num BIGINT,
    name_weapon VARCHAR(50),
    num_rota INT,
    rank VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS ITO (
    id INT PRIMARY KEY,
    classification VARCHAR(50),
    num_rota INT,
    name VARCHAR(50),
    count INT
);

CREATE TABLE IF NOT EXISTS electro (
    id INT PRIMARY KEY,
    serial_number BIGINT,
    num_rota INT,
    name VARCHAR(50),
    count INT
);

CREATE TABLE IF NOT EXISTS food (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    count VARCHAR(50),
    num_rota INT
);