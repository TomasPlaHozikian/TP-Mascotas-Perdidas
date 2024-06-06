CREATE TABLE IF NOT EXISTS usuarios (
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    mail VARCHAR(50),
    numero INT,
    contrasena VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS animales (
    nombre VARCHAR(50),
    especie VARCHAR(50),
    raza VARCHAR(50),
    ubicacion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS centros (
    nombre VARCHAR(50),
    direccion VARCHAR(50)
);

INSERT INTO usuarios (nombre, apellido, mail, numero, contrasena) VALUES ('Juan', 'Perez', 'juan@mail.com',123456789, 'hola12345');
INSERT INTO usuarios (nombre, apellido, mail, numero, contrasena) VALUES ('Maria', 'Gonzalez', 'maria@mail.com',987654321, 'hola54321');

INSERT INTO animales (nombre, especie, raza, ubicacion) VALUES ('Firulais', 'Perro', 'Labrador', 'Calle 123');
INSERT INTO animales (nombre, especie, raza, ubicacion) VALUES ('Mishi', 'Gato', 'Siames', 'Calle 456');

INSERT INTO centros (nombre, direccion) VALUES ('Centro de adopcion de animales', 'Calle 789');
INSERT INTO centros (nombre, direccion) VALUES ('Centro de adopcion de animales 2', 'Calle 1011');