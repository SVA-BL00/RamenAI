CREATE DATABASE IF NOT EXISTS ramenAI;
USE ramenAI;

CREATE TABLE IF NOT EXISTS Usuarios (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(255) NOT NULL UNIQUE
);