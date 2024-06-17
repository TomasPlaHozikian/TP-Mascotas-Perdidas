from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import requests

app = Flask(__name__)

app.secret_key = "helloworld"

@app.route('/')
def home():
    response = requests.get('https://apianimalesperdidos.pythonanywhere.com/animales')
    response2 = requests.get('https://apianimalesperdidos.pythonanywhere.com/usuarios')
    data = response.json()
    data2 = response2.json()
    return render_template('home.html', data=data, data2=data2, logged_in="user_info" in session)

@app.route('/resultado', methods=['GET', 'POST'])
def resultado():
    response2 = requests.get('https://apianimalesperdidos.pythonanywhere.com/usuarios')
    data2 = response2.json()
    params = {
            'nombre': request.form.get('fnombre'),
            'especie': request.form.get('fespecie'),
            'raza': request.form.get('fraza'),
            'provincia': request.form.get('fprovincia'),
            'municipio': request.form.get('fmunicipio'),
            'localidad': request.form.get('flocalidad')
        }

    response = requests.get('https://apianimalesperdidos.pythonanywhere.com/animales', params=params)
    data = response.json()
    return render_template('resultado.html', data=data, logged_in="user_info" in session, data2=data2)


@app.route('/busqueda')
def buscar():
    return render_template('buscaranimal.html', logged_in="user_info" in session)

def verifUsuario(lista_usuarios, nombre_a_buscar, contrasena_a_buscar):
    for usuario in lista_usuarios:
        if (usuario["nombre"].lower() == nombre_a_buscar.lower()) and (usuario["contrasena"].lower() == contrasena_a_buscar.lower()):
            return usuario
    return None

@app.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('iniciosesion.html', logged_in="user_info" in session, error="")

@app.route('/login', methods=["POST"])
def login():
    user = request.form.get("user")
    password = request.form.get("password")
    usuarios = requests.get('https://apianimalesperdidos.pythonanywhere.com/usuarios')

    logged_in_user = verifUsuario(usuarios.json(), user, password)
    error=""
    if logged_in_user is not None:
        session['user_info'] = logged_in_user
        return redirect(url_for('home'))

    return render_template('iniciosesion.html', logged_in="user_info" in session, error="Usuario o contraseña incorrectos")

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('user_info', None)
    return redirect(url_for('home'))

@app.route('/registrar_usuario')
def registrar_usuario():
    return render_template('registrarusuario.html', logged_in="user_info" in session)

@app.route('/mandar_usuario', methods=["POST"])
def mandar_usuario():
        nombre = request.form.get("fname")
        apellido = request.form.get("lname")
        email = request.form.get("email")
        telefono = request.form.get("phone")
        password = request.form.get("password")
        payload = {"nombre": nombre, "apellido": apellido, "mail": email, "numero": telefono, "contrasena": password }
        NuevoUsuario = requests.post('https://apianimalesperdidos.pythonanywhere.com/usuarioscargar', data=payload)
        NUJson = NuevoUsuario.json()
        if NUJson["id"] == 1:
            usuarios = requests.get('https://apianimalesperdidos.pythonanywhere.com/usuarios')
            logged_in_user = verifUsuario(usuarios.json(), nombre, password)
            if logged_in_user is not None:
                session['user_info'] = logged_in_user
            return redirect(url_for('perfilpropio', nombre=nombre, email=email, telefono=telefono))
        else:
            return redirect(url_for('registrar_usuario'))

@app.route('/perfilpropio')
def perfilpropio():
    id = session['user_info']['id']
    params = {
            'creado_por': id
        }
    response = requests.get('https://apianimalesperdidos.pythonanywhere.com/animales', params=params)
    data = response.json()
    if "user_info" in session:
        nombre = session['user_info']['nombre'] + " " + session['user_info']['apellido']
        email = session['user_info']['mail']
        telefono = session['user_info']['numero']
        return render_template('perfilpropio.html', nombre=nombre, email=email, telefono=telefono, logged_in="user_info" in session, data=data)
    return redirect(url_for('iniciar_sesion'))

@app.route('/perfilajeno')
def perfilajeno():
    id = request.args.get('id')
    response = requests.get(f'https://apianimalesperdidos.pythonanywhere.com/obtener_usuario_particular/{id}')
    data = response.json()
    if not data:
        data = "no encontrado"
    else:
        id, nombre, apellido, mail, numero, _ = data[0]
    return render_template('perfilajeno.html', nombre=nombre, apellido=apellido, mail=mail, numero=numero, logged_in="user_info" in session)

@app.route('/registrar_mascota')
def registrar_mascota():
    return render_template('registarmascota.html', logged_in="user_info" in session)
      
@app.route ('/vercentro')
def ver_centro():
    response = requests.get('https://apianimalesperdidos.pythonanywhere.com/refugios')
    data = response.json()
    return render_template('mostrarcentro.html', data = data, logged_in="user_info" in session)


@app.route('/cargar_mascota', methods=['GET', 'POST'])
def cargar_mascota():
    if request.method == 'POST':
        data = {
            'creado_por': session['user_info']['id'],
            'nombre': request.form.get('fname'),
            'especie': request.form.get('fespecie'),
            'raza': request.form.get('fraza'),
            'provincia': request.form.get('fprovincia'),
            'municipio': request.form.get('fmunicipio'),
            'localidad': request.form.get('flocalidad'),
            'calle': request.form.get('fcalle'),
            'numero': request.form.get('fnumero'),
            'foto': request.form.get('ffoto')
        }
        response = requests.post('https://apianimalesperdidos.pythonanywhere.com/animales', json=data)
        # Handle the response
    return render_template('registarmascota.html', logged_in="user_info" in session)

@app.route ('/quienes_somos')
def quienes_somos():
    return render_template('quienes_somos.html', logged_in="user_info" in session)

@app.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    return render_template('preguntas_frecuentes.html', logged_in="user_info" in session)

@app.route ('/contacto')
def contacto():
    return render_template('contacto.html', logged_in="user_info" in session)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def error_en_el_servidor(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
