from flask import Flask, request, jsonify, render_template
import requests, json # type: ignore

app = Flask(__name__)

@app.route('/registrarUsuario', methods=["GET", "POST"])
def ValidacionUsuario():
    user = request.form["fname"]
    apellido = request.form["lname"]
    email = request.form["email"]
    telefono = request.form["phone"]
    password = request.form["password"]
    usuariosSQL = requests.get('http://localhost:5002/usuarios')
    datosDeUsuario = {"nombre": user, 'apellido': apellido, 'mail': email, "numero": telefono, "contrasena": password}
    # Verifiacion SQL
    def verifNombre(lista_usuarios, nombre_a_buscar):
        for usuario in lista_usuarios:
            if usuario["nombre"].lower() == nombre_a_buscar.lower():
                return True
        return False
    if verifNombre(json.loads(usuariosSQL.text),user) is False:
        SubirUsuario = requests.post("http://localhost:5002/usuarioscargar", data=datosDeUsuario)
        return jsonify({"id": 1})
    else:
        return jsonify({"id": 2})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
