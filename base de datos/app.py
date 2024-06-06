from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


import mysql.connector

app = Flask(__name__)

"""
def set_connection():
    conn = create_engine('mysql+mysqlconnector://root:test@localhost/tp')
    connection = conn.connect()
    return connection
"""

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cargaranimal')
def cargaranimal():
    return render_template('cargaranimal.html')

@app.route('/cargarusuario')
def cargarusuario():
    return render_template('cargarusuario.html')

def set_connection():
    conn = mysql.connector.connect(
        user='root',
        password='test',
        host='localhost',
        database='tp')
    return conn


def show_animales():
    conn = set_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM animales')
    result = cursor.fetchall()
    conn.close()
    return result


@app.route('/animales', methods=['GET'])
def get_animales():
    try:
        conn = set_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animales')
        result = cursor.fetchall()
        conn.close()
        return jsonify(result)
    except SQLAlchemyError as e:
        return str(e)
    
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        conn = set_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios')
        result = cursor.fetchall()
        conn.close()
        return jsonify(result)
    except SQLAlchemyError as e:
        return str(e)


@app.route('/animalescargar', methods=['POST'])
def cargar_animal():
    try:
        conn = set_connection()
        cursor = conn.cursor()
        # conseguir valores mediante request
        nombre = request.form.get('nombre')
        especie = request.form.get('especie')
        raza = request.form.get('raza')
        ubicacion = request.form.get('ubicacion')
        # insertar valores en la tabla
        cursor.execute(f"INSERT INTO animales (nombre, especie, raza, ubicacion) VALUES ('{nombre}', '{especie}', '{raza}', '{ubicacion}')")
        conn.commit()
        conn.close()
        return 'Animal inserted successfully'
    except SQLAlchemyError as e:
        return str(e)


@app.route('/usuarioscargar', methods=['POST'])
def cargar_usuario():
    try:
        conn = set_connection()
        cursor = conn.cursor()
        # conseguir valores mediante request
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        mail = request.form.get('mail')
        numero = request.form.get('numero')
        contrasena = request.form.get('contrasena')
        # insertar valores en la tabla
        cursor.execute(f"INSERT INTO usuarios (nombre, apellido, mail, numero, contrasena) VALUES ('{nombre}', '{apellido}', '{mail}', '{numero}', '{contrasena}')")
        conn.commit()
        conn.close()
        return 'User inserted successfully'
    except SQLAlchemyError as e:
        return str(e)






if __name__ == '__main__':
    app.run()
