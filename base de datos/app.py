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

@app.route('/refugios', methods=['GET','POST'])
def refugios():
    if request.method == 'GET':
        try:
            conn = set_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM centros')
            result = cursor.fetchall()
            conn.close()
            refugios = []
            for refugio in result:
                refugios.append({
                    'id': refugio[0],
                    'nombre': refugio[1],
                    'numero_de_telefono': refugio[2],
                    'email': refugio[3],
                    'provincia': refugio[4],
                    'municipio': refugio[5],
                    'localidad': refugio[6],
                    'calle': refugio[7],
                    'numero_de_calle': refugio[8]
                })
            return jsonify(refugios)
        except SQLAlchemyError as e:
            return str(e)
    elif request.method == 'POST':
        try:
            conn = set_connection()
            cursor = conn.cursor()
        # conseguir valores mediante request
            nuevo_refugio = request.get_json()
            nombre = nuevo_refugio['nombre']
            numero_de_telefono = nuevo_refugio['numero_de_telefono']
            email = nuevo_refugio['email']
            provincia = nuevo_refugio['provincia']
            municipio = nuevo_refugio['municipio']
            localidad = nuevo_refugio['localidad']
            calle = nuevo_refugio['calle']
            numero_de_calle = nuevo_refugio['numero_de_calle']
        # insertar valores en la tabla
            cursor.execute(f"INSERT INTO centros (nombre, numero_de_telefono, email, provincia, municipio, localidad, calle, numero_de_calle) VALUES ('{nombre}', {numero_de_telefono}, '{email}', '{provincia}', '{municipio}', '{localidad}', '{calle}', {numero_de_calle})")
            conn.commit()
            conn.close()
            return jsonify({'message': 'Refugio creado correctamente'})
        except SQLAlchemyError as e:
            return str(e)



@app.route('/borrar_refugio/<nombre>', methods=['DELETE'])
def borrar_refugio(nombre):
    try:
        conn = set_connection()
        cursor = conn.cursor()
        # eliminar valores en la tabla
        #cursor.execute(f"SELECT nombre FROM centros WHERE nombre='{nombre}'")
        cursor.execute(f"DELETE FROM centros WHERE nombre='{nombre}'")
        conn.commit()
        conn.close()
        return jsonify({'message': 'Refugio eliminado correctamente'})
    except SQLAlchemyError as e:
        return str(e)


@app.route('/modificar_refugio/<nombre>', methods=['PATCH'])
def modificar_refugio(nombre):
    try:
        modificaciones = request.get_json()
        conn = set_connection()
        cursor = conn.cursor()

        for modificacion in modificaciones:
            cursor.execute(f"UPDATE centros SET {modificacion}='{modificaciones[modificacion]}' WHERE nombre='{nombre}'")
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Refugio modificado correctamente'})
    except SQLAlchemyError as e:
        return str(e)



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


@app.route('/getanimales', methods=['GET'])
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
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]
        conn.close()
        return jsonify(result)
    except SQLAlchemyError as e:
        return str(e)


#luego se utilizara fetch mediante javascript para recibir datos del html en formato json,
#se añadira un event listener al submit del form que recibira los datos y los parseara a json.
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

        cursor.execute('SELECT * FROM usuarios')
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]

        # busca la lista de usuarios para ver si existe
        def verifNombre(lista_usuarios, nombre_a_buscar):
            for usuario in lista_usuarios:
                if usuario["nombre"].lower() == nombre_a_buscar.lower():
                    return True
            return False
        print(nombre)
        print(verifNombre(result,nombre))

        if verifNombre(result,nombre) is False:
            cursor.execute(f"INSERT INTO usuarios (nombre, apellido, mail, numero, contrasena) VALUES ('{nombre}', '{apellido}', '{mail}', '{numero}', '{contrasena}')")
            conn.commit()
            conn.close()
            return jsonify({"message":"User inserted successfully","id":1})
        else:
            return jsonify({"message": "ese usuario ya existe", "id": 2})
        
    except SQLAlchemyError as e:
        return str(e)





@app.route('/animales', methods=['GET','POST'])
def animales():
    if request.method == 'GET':
        try:
            conn = set_connection()
            cursor = conn.cursor()

            #params del request
            nombre = request.args.get('nombre')
            especie = request.args.get('especie')
            raza = request.args.get('raza')
            provincia = request.args.get('provincia')
            municipio = request.args.get('municipio')
            localidad = request.args.get('localidad')

            #query armada
            query = 'SELECT * FROM animales WHERE 1=1'
            if nombre:
                query += f" AND nombre='{nombre}'"
            if especie:
                query += f" AND especie='{especie}'"
            if raza:
                query += f" AND raza='{raza}'"
            if provincia:
                query += f" AND provincia='{provincia}'"
            if municipio:
                query += f" AND municipio='{municipio}'"
            if localidad:
                query += f" AND localidad='{localidad}'"
            
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return jsonify(result)
        except SQLAlchemyError as e:
            return str(e)
    elif request.method == 'POST':
        try:
            conn = set_connection()
            cursor = conn.cursor()
        # conseguir valores mediante request
            nuevo_animal = request.get_json()
            nombre = nuevo_animal['nombre']
            especie = nuevo_animal['especie']
            raza = nuevo_animal['raza']
            provincia = nuevo_animal['provincia']
            municipio = nuevo_animal['municipio']
            localidad = nuevo_animal['localidad']
            calle = nuevo_animal['calle']
            numero = nuevo_animal['numero']
            foto = nuevo_animal['foto']
        # insertar valores en la tabla
        #{ "direccion" : "calzada", "nombre": "polideportivo" }
        #{"nombre": "Jorge", "especie" : "Gato", "raza" : "Calle", "provincia": "Buenos Aires", "municipio": "Lanus", "localidad": "Valentin Alsina", "calle": "Paraguay", "numero": "3254", "foto": "https://www.warrenphotographic.co.uk/photography/sqrs/17693.jpg"}
            cursor.execute(f"INSERT INTO animales (nombre, especie, raza, provincia, municipio, localidad, calle, numero, foto) VALUES ('{nombre}', '{especie}', '{raza}', '{provincia}', '{municipio}', '{localidad}', '{calle}', '{numero}', '{foto}')")
            conn.commit()
            conn.close()
            return jsonify({'message': 'animal añadido correctamente'})
        except SQLAlchemyError as e:
            return str(e)

if __name__ == '__main__':
    app.run()
