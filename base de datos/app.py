from flask import Flask, request, jsonify, render_template, redirect
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


import mysql.connector

app = Flask(__name__)

def set_connection():
    conn = mysql.connector.connect(
        user='APIAnimalesperdi',
        password='PruebadbIntro',
        host='APIAnimalesperdidos.mysql.pythonanywhere-services.com',
        database='APIAnimalesperdi$tp')
    return conn


#En caso de que la request sea GET, permite obtener todos los refugios
#En caso de que la request sea POST, recibe:
#id, nombre, numero de telefono, email, provincia, municipio, localidad, calle, numero de calle,
#y los agrega a la base de datos.
#Pre: Se manda un GET o un POST con los datos previamente dichos
#Post: Se obtienen, en caso de un GET todos los refugios, en caso de un POST se anade el refugio a la base de datos.
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


#Permite borrar un refugio mediante un request de metodo DELETE, con un nombre como input
#Pre: existe un refugio
#Post: elimina el refugio de la base de datos
@app.route('/borrar_refugio/<nombre>', methods=['DELETE'])
def borrar_refugio(nombre):
    try:
        conn = set_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM centros WHERE nombre='{nombre}'")
        conn.commit()
        conn.close()
        return jsonify({'message': 'Refugio eliminado correctamente'})
    except SQLAlchemyError as e:
        return str(e)


#Mediante una request de metodo PATCH, dado un nombre y una modificacion, permite cambiar un atributo especifico de un centro.
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


#Mediante el metodo GET, permite obtener todos los usuarios en la base de datos
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


#Dado un id, mediante un metodo GET, permite obtener un usuario especifico
@app.route('/obtener_usuario_particular/<id>', methods=['GET'])
def get_usuario_particular(id):
    try:
        conn = set_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM usuarios WHERE id='{id}'")
        result = cursor.fetchall()
        conn.close()
        return jsonify(result)
    except SQLAlchemyError as e:
        return str(e)


#Funcion usada para verificar si existe un usuario mediante su mail
def verifMail(lista_usuarios, mail_a_buscar):
    for usuario in lista_usuarios:
        if usuario["mail"].lower() == mail_a_buscar.lower():
            return True
    return False


#Permite, mediante metodo POST, crear un usuario y cargarlo a la base de datos, recibiendo:
#nombre, apellido, mail, numero de telefono y contrasena
#En caso de que no hayan suficientes datos, devuelve id 0 y el mensaje "Faltan datos"
#En caso de que el mail del usuario ya exista, devuelve el id 2 y el mensaje "Ese usuario ya existe"
#En caso de que no exista el mail, lo anade a la base de datos, y devuelve id 1 y el mensaje "Usuario insertado"
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
        #Verificar que todos los campos esten llenos
        if not all([nombre, apellido, mail, numero, contrasena]):
            return jsonify({"message": "Faltan datos", "id": 0}), 400
        cursor.execute('SELECT * FROM usuarios')
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]
        # buscar la lista de usuarios para ver si existe
        if verifMail(result,mail) is False:
            cursor.execute(f"INSERT INTO usuarios (nombre, apellido, mail, numero, contrasena) VALUES ('{nombre}', '{apellido}', '{mail}', '{numero}', '{contrasena}')")
            conn.commit()
            conn.close()
            return jsonify({"message":"Usuario insertado","id":1})
        else:
            conn.commit()
            conn.close()
            return jsonify({"message": "Ese usuario ya existe", "id": 2})
    except SQLAlchemyError as e:
        return str(e)


#Mediante el metodo DELETE, dado un id, permite borrar un usuario especifico
@app.route('/borrar_usuario/<id>', methods=['DELETE'])
def borrar_usuario(id):
    try:
        conn = set_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM usuarios WHERE id='{id}'")
        conn.commit()
        conn.close()
        return jsonify({'message': 'Usuario eliminado correctamente'})
    except SQLAlchemyError as e:
        return str(e)


#Si el metodo es GET, arma un query con los datos que se le dan, y busca en la base de datos todos
#los animales que tengan esos datos
#Si el metodo es POST, toma los datos enviados y anade el animal a la base de datos.
@app.route('/animales', methods=['GET','POST'])
def animales():
    if request.method == 'GET':
        try:
            conn = set_connection()
            cursor = conn.cursor()
            #params del request
            creado_por = request.args.get('creado_por')
            nombre = request.args.get('nombre')
            especie = request.args.get('especie')
            raza = request.args.get('raza')
            provincia = request.args.get('provincia')
            municipio = request.args.get('municipio')
            localidad = request.args.get('localidad')
            #query armada
            query = 'SELECT * FROM animales WHERE 1=1'
            if creado_por:
                query += f" AND creado_por='{creado_por}'"
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
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
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
            creado_por = nuevo_animal['creado_por']
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
            cursor.execute(f"INSERT INTO animales (creado_por, nombre, especie, raza, provincia, municipio, localidad, calle, numero, foto) VALUES ('{creado_por}','{nombre}', '{especie}', '{raza}', '{provincia}', '{municipio}', '{localidad}', '{calle}', '{numero}', '{foto}')")
            conn.commit()
            conn.close()
            return jsonify({'message': 'animal añadido correctamente'})
        except SQLAlchemyError as e:
            return str(e)
        


#Permite borrar animales de la base de datos, mediante el metodo POST 
#que dentro de si mismo tiene un input de type hidden con nombre _method y value DELETE
@app.route('/borrar_animal/<id>', methods=['POST'])
def borrar_animal(id):
    if request.form.get('_method') == 'DELETE':
        try:
            conn = set_connection()
            cursor = conn.cursor()
            # eliminar valores en la tabla
            cursor.execute(f"DELETE FROM animales WHERE id='{id}'")
            conn.commit()
            conn.close()
            return redirect('https://frontanimalesperdidos.pythonanywhere.com/perfilpropio')
        except SQLAlchemyError as e:
            return str(e)



if __name__ == '__main__':
    app.run()