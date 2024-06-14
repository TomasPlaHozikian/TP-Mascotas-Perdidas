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
    if "user" in session:
        return render_template('home.html', data=data, data2=data2, logged_in=True)
    return render_template('home.html', data=data, data2=data2)

@app.route('/resultado', methods=['GET', 'POST'])
def resultado():
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
    return render_template('resultado.html', data=data)


@app.route('/busqueda')
def buscar():
    return render_template('buscaranimal.html')

def verifUsuario(lista_usuarios, nombre_a_buscar, contrasena_a_buscar):
    for usuario in lista_usuarios:
        if (usuario["nombre"].lower() == nombre_a_buscar.lower()) and (usuario["contrasena"].lower() == contrasena_a_buscar.lower()):
            return True
    return False

@app.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('iniciosesion.html')

@app.route('/login', methods=["POST"])
def login():
    user = request.form.get("user")
    password = request.form.get("password")
    usuarios = requests.get('https://apianimalesperdidos.pythonanywhere.com/usuarios')


    if verifUsuario(usuarios.json(), user, password) is True:
        session['user'] = user
        return redirect(url_for('perfilpropio'))

    return render_template('iniciosesion.html')

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/registrar_usuario')
def registrar_usuario():
    return render_template('registrarusuario.html')

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
        print(NUJson["id"])
        if NUJson["id"] == 1:
            return redirect(url_for('perfilpropio', nombre=nombre, email=email, telefono=telefono))
        else:
            return redirect(url_for('registrar_usuario'))

@app.route('/perfilpropio')
def perfilpropio():
    if "user" in session:
        nombre = session['user']
        return render_template('perfilpropio.html', nombre=nombre)
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
    return render_template('perfilajeno.html', nombre=nombre, apellido=apellido, mail=mail, numero=numero)

@app.route('/registar_centro')
def registrar_centro():
    return render_template('registrarcentro.html')

@app.route('/registrar_mascota')
def registrar_mascota():
    return render_template('registarmascota.html')
      
@app.route ('/vercentro')
def ver_centro():
    response = requests.get('https://apianimalesperdidos.pythonanywhere.com/refugios')
    data = response.json()
    return render_template('mostrarcentro.html', data = data)


@app.route('/cargar_mascota', methods=['GET', 'POST'])
def cargar_mascota():
    if request.method == 'POST':
        data = {
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
    return render_template('registarmascota.html')

@app.route ('/quienes_somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    return render_template('preguntas_frecuentes.html')

@app.route ('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
