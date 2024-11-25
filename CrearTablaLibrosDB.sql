--create database LibrosDB;

USE LibrosDB;

CREATE TABLE Libros (
    Id INT IDENTITY(1,1) PRIMARY KEY, -- Columna Id autoincremental y clave primaria
    Titulo NVARCHAR(255) NOT NULL,    -- Columna Titulo, no permite valores nulos
    Autor NVARCHAR(255) NOT NULL,     -- Columna Autor, no permite valores nulos
    A�o INT NOT NULL                  -- Columna A�o, no permite valores nulos
);
