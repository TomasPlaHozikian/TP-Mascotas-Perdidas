from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


import mysql.connector

app = Flask(__name__)

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

"""
def set_connection():
    conn = create_engine('mysql+mysqlconnector://root:test@localhost/tp')
    connection = conn.connect()
    return connection


def show_animales(connection):
    query = text('SELECT * FROM animales')
    try:
        result = connection.execute(query)
        connection.commit()
    except SQLAlchemyError as err:
        print("error", err._cause_)
    return result


@app.route('/animales')
def animales():
    connection = set_connection()
    site = show_animales(connection)
    data = []
    for row in site:
        result = {}
        result['nombre'] = row.nombre
        result['especie'] = row.especie
        result['raza'] = row.raza
        result['ubicacion'] = row.ubicacion
        data.append(result)
    return jsonify(data), 200
"""




if __name__ == '__main__':
    print(show_animales())
    app.run()
