from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)

mysql = MySQL()

app.config["MYSQL_HOST"] = "localhost"
# app.config['MySQL_PORT'] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "dbcrud"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pregfrec")
def pregfrec():
    return render_template("modulos/firmantes/pregfrec.html")


@app.route("/firmantes")
def index_firmantes():

    sql = "SELECT * FROM firmantes"

    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql)
    firmantes = cursor.fetchall()
    conexion.commit()
    return render_template("modulos/firmantes/index.html", firmantes=firmantes)


@app.route("/firmantes/create")
def create():
    return render_template("modulos/firmantes/create.html")


@app.route("/firmantes/create/guardar", methods=["POST"])
def firmantes_guardar():
    nombre = request.form["nombre"]
    dni = request.form["dni"]
    mail = request.form["mail"]
    fecha = request.form["fecha"]

    sql = "INSERT INTO firmantes(nombre, dni, mail, fecha) VALUES(%s, %s, %s, %s)"
    datos = (nombre, dni, mail, fecha)
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect("/firmantes")


@app.route("/firmantes/borrar/<int:id>")
def firmantes_borrar(id):
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM firmantes WHERE id=%s", (id,))
    conexion.commit()
    return redirect("/firmantes")


@app.route("/firmantes/edit/<int:id>")
def firmantes_editar(id):
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM firmantes WHERE id=%s", (id,))
    firmantes = cursor.fetchone()
    conexion.commit()
    return render_template("modulos/firmantes/edit.html", firmantes=firmantes)


@app.route("/firmantes/edit/actualizar", methods=["POST"])
def firmante_actualizar():
    id = request.form["txtid"]
    nombre = request.form["nombre"]
    dni = request.form["dni"]
    mail = request.form["mail"]
    fecha = request.form["fecha"]

    sql = "UPDATE firmantes SET nombre=%s, dni=%s, mail=%s, fecha=%s WHERE id=%s"
    datos = (nombre, dni, mail, fecha, id)
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect("/firmantes")


if __name__ == "__main__":
    app.run(debug=True)
