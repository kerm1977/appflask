from flask import Flask #Del módulo de flask importar la clase de flask
from flask import request, make_response, redirect, render_template, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) 	#__name__ almacena el módulo donde nos encontramos
						# Es como decir app = main.py

#Configuración de La Base de Datos
import os
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/db.db" #Esta es la ruta de la db
# Clave Secreta
app.config['SECRET_KEY'] = '0b254d802b768739f4a9c07dc2be6efa849524cb3a371a50f28a80f469abfba9'

app.config['SQLALCHEMY_DATABASE_URI'] = dbdir # Crea la DB en la misma ruta de main.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False	
#Instancia de la DB
db = SQLAlchemy(app)
app.app_context().push()

@app.route("/") #Decorador
def home():
	return "Hola Mundo"

@app.route("/saludo") #/url saludo va luego de la dirección 127.0.0.1/saludo 
def saludo(): #Otra función que saluda
	return "Otro saludo" #Retorna este texto

# STRING
@app.route("/user/<string:user>") #Ruta con variable http://127.0.0.1:81/user/kenth
def username(user):	#Almacena el valor de tipo cadena de texto
	return f"Hola {user}" #Concatena con f-string el parámetro (user)

# INT
@app.route("/num/<int:num>") #Ruta con variable http://127.0.0.1:81/user/kenth
def numero(num):	#Almacena el valor de tipo cadena de texto
	return f"Hola {num}" #Concatena con f-string el parámetro (user)

# COMBINAR STRING + NUM
@app.route("/mix/<int:id>/<string:name>") #Ruta con variable http://127.0.0.1:81/mix/10/kenth
def mix(id,name):	#Almacena el valor de tipo cadena y entero
	return f"Hola {name} tu id es {id}" #Concatena con f-string los parámetros (id) y (name)
				  #kenth		   10

# SUMA FLOTANTES
@app.route("/suma/<float:n1>/<float:n2>") #Ruta con variable http://127.0.0.1:81/suma/10/kenth
def suma(n1,n2):	#Almacena el valor de tipo flotantes
	return f"La suma de {n1}+{n2} es {n1+n2}" #Concatena con f-string los parámetros (n1) y (n2)

# RESPUESTAS DEFAULT
@app.route("/dft/")
@app.route("/dft/<string:dft>") #Ruta con variable http://127.0.0.1:81/suma/10/kenth
def default(dft="respuesta por default"):	#Almacena el valor de tipo cadena de texto
	return f"La respuesta default es {dft}" #Concatena con f-string los parámetros (n1) y (n2)





#app o main se transforma en un módulo principal adoptando el valor de main
#y name al compararse a main o ser igual ejecuta el servidor local app.run
#para comprobarlo escribir print(__name__) dentro de cualquier función
#al ejecutar el servidor debe aparecer en consola  __main__
if __name__ 	== "__main__":
	db.create_all()
	app.run(
		debug = True, 	#Permite la ejecución en modo error para actualizar los cambios
		port = 81) 		#Pero debe ser desactivado en producción y activar en desarrollo
						#Asigna un puerto si entra en conflicto con algún otro
						#Y otro valor pero casi no se usa es host = "0,0,0,0"