from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import psycopg2

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

def conectar():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                session["usuario"] = user[1]
                return redirect(url_for("usuarios_registrados"))
            else:
                return render_template("login.html", error="Credenciales inválidas")
        except Exception as e:
            return render_template("login.html", error=str(e))

    return render_template("login.html")

@app.route("/usuarios")
def usuarios_registrados():
    if "usuario" not in session:
        return redirect(url_for("login"))

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM usuarios")
        usuarios = cur.fetchall()
        cur.close()
        conn.close()

        return render_template("usuarios.html", usuarios=usuarios)
    except Exception as e:
        return f"Error: {e}"

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))
