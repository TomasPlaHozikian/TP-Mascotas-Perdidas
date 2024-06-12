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
    provincia VARCHAR(50),
    municipio VARCHAR(50),
    localidad VARCHAR(50),
    calle VARCHAR(50),
    numero INT,
    foto VARCHAR(1000)
);

CREATE TABLE IF NOT EXISTS centros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    numero_de_telefono INT,
    email VARCHAR(50),
    provincia VARCHAR(50),
    municipio VARCHAR(50),
    localidad VARCHAR(50),
    calle VARCHAR(50),
    numero_de_calle INT
);

INSERT INTO usuarios (nombre, apellido, mail, numero, contrasena) VALUES ('Juan', 'Perez', 'juan@mail.com',123456789, 'hola12345');
INSERT INTO usuarios (nombre, apellido, mail, numero, contrasena) VALUES ('Maria', 'Gonzalez', 'maria@mail.com',987654321, 'hola54321');

INSERT INTO animales (nombre, especie, raza, provincia, municipio, localidad, calle, numero, foto) VALUES ('Firulais', 'Perro', 'Labrador', 'Buenos Aires', 'Lomas de Zamora', 'Banfield', 'Alvear', 800, 'https://cdn.discordapp.com/attachments/601110619646853134/1249859721423228969/labrador.jpg?ex=6668d612&is=66678492&hm=db205e119841e841ae9dddd506b8c5513dbc8492552d34dfc35bcfa165b42908&');
INSERT INTO animales (nombre, especie, raza, provincia, municipio, localidad, calle, numero, foto) VALUES ('Mishi', 'Gato', 'Siames', 'Buenos Aires', 'Lanus', 'Remedios De Escalda', 'Lugones', 200, 'https://cdn0.soyungato.com/es/razas/0/2/0/gato-siames_20_9_150_square.jpg');
INSERT INTO animales (nombre, especie, raza, provincia, municipio, localidad, calle, numero, foto) VALUES ('Jorge', 'Gato', 'Calle', 'Buenos Aires', 'Lanus', 'Valentin Alsina', 'Paraguay', 4000, 'https://www.warrenphotographic.co.uk/photography/sqrs/17693.jpg');

INSERT INTO centros (nombre, numero_de_telefono, email, provincia, municipio, localidad, calle, numero_de_calle) VALUES ('Centro de adopcion de animales', 11111111, 'centro1@gmail.com', 'Buenos Aires', 'Lanus', 'Lanus', 'Ituzaingo', 1282);

INSERT INTO centros (nombre, numero_de_telefono, email, provincia, municipio, localidad, calle, numero_de_calle) VALUES ('Centro de adopcion de animales 2', 11111111, 'centro2@gmail.com', 'Buenos Aires', 'Almirante Brown', 'Rafael Calzada', 'AV San Martin', 1562);

INSERT INTO centros (nombre, numero_de_telefono, email, provincia, municipio, localidad, calle, numero_de_calle) VALUES ('Centro de adopcion de animales 3', 11111111, 'centro3@gmail.com', 'Buenos Aires', 'CABA', 'CABA', 'Av. Rivadavia', 1300);

INSERT INTO centros (nombre, numero_de_telefono, email, provincia, municipio, localidad, calle, numero_de_calle) VALUES ('Centro de adopcion de animales 4', 11111111, 'centro4@gmail.com', 'Buenos Aires', 'CABA', 'CABA', 'Av. Costanera Sur', 700);

INSERT INTO centros (nombre, numero_de_telefono, email, provincia, municipio, localidad, calle, numero_de_calle) VALUES ('Centro de adopcion de animales 5', 11111111, 'centro5@gmail.com', 'Buenos Aires', 'CABA', 'CABA', 'Av. Callao', 1234);

