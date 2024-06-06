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

if __name__ == '__main__':
    app.run(debug=True)
