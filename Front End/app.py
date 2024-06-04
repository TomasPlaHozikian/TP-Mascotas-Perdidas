from flask import Flask, jsonify, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")



if __name__ == "__main__":
    app.run()
