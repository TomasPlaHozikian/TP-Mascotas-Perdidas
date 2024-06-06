from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/busqueda')
def buscar():
    return render_template('buscaranimal.html')

@app.route('/login')
def iniciar_sesion():
    return render_template('iniciosesion.html')

@app.route('/registrar_usuario')
def registrar_usuario():
    return render_template('registrarusuario.html')

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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
