abrir carpeta docker en terminal

ejecutar docker-compose up --build -d

para conectar con azure:

 en conection seleccionar mysql como conection type
 usar localhost como server name
 username root
 clave test

para luego conectar a python se usa el codigo en app.py:


import mysql.connector

def set_connection():
    conn = mysql.connector.connect(
        user='root',
        password='test',
        host='localhost',
        database='tp')
    return conn