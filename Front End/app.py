from flask import Flask, render_template, request, jsonify, redirect, url_for

import requests

app = Flask(__name__)



@app.route('/')
def home():
    response = requests.get('http://127.0.0.1:5000/animales')
    data = response.json()
    return render_template('home.html', data=data)

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

    response = requests.get('http://127.0.0.1:5000/animales', params=params)
    data = response.json()
    return render_template('resultado.html', data=data)


@app.route('/busqueda')
def buscar():
    return render_template('buscaranimal.html')

@app.route('/login')
def iniciar_sesion():
    return render_template('iniciosesion.html')

@app.route('/registrar_usuario')
def registrar_usuario():
    return render_template('registrarusuario.html')
"""
@app.route('/registrar', methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        nombre = request.form["fname"]
        apellido = request.form["lname"]
        email = request.form["email"]
        telefono = request.form["phone"]
        password = request.form["password"]
        payload = {"fname": nombre, "lname": apellido, "email": email, "phone": telefono, "password": password }
        NuevoUsuario = requests.post('http://localhost:5000/registrarUsuario', data=payload)
        print(NuevoUsuario)
        if NuevoUsuario["id"] == 1:
            return render_template('home.html', nombre=nombre)
        else:
            return redirect(url_for('registrar'))
    else:
        return render_template('iniciosesion.html')
"""
@app.route('/perfilpropio')
def perfil():
    return render_template('perfilpropio.html')

@app.route('/perfilajeno')
def perfilajeno():
    return render_template('perfilajeno.html')

@app.route('/registar_centro')
def registrar_centro():
    return render_template('registrarcentro.html')

@app.route('/registrar_mascota')
def registrar_mascota():
    return render_template('registarmascota.html')
      
@app.route ('/vercentro')
def ver_centro():
    return render_template('mostrarcentro.html')


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
        response = requests.post('http://127.0.0.1:5000/animales', json=data)
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
