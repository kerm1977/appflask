# IMPORTS  ************************************************************************************
#**********************************************************************************************
from flask import Flask
from flask import request, make_response, redirect, render_template, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, EmailField
from wtforms.validators import DataRequired, Length, Email,  EqualTo, ValidationError
from flask_bcrypt import Bcrypt



app = Flask(__name__) 	
#**********************************************************************************************
#**********************************************************************************************








#DATABASE SQLITE ******************************************************************************
#**********************************************************************************************
import os
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/db.db" #CONECTOR - RUTA ABSOLUTA
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '0b254d802b768739f4a9c07dc2be6efa849524cb3a371a50f28a80f469abfba9'
#**********************************************************************************************
#**********************************************************************************************








#FORMULARIO TABLAS LOGIN Y DE REGISTRO ********************************************************
#**********************************************************************************************
class formularioRegistro(FlaskForm):
 # CAMPOS EN DB			   TIPO DE DATO		NOMBRE DE CAMPO EN HTML Y VALIDACIONES	
	username 			= 	StringField		('username', validators=[DataRequired(), Length(min=3, max=20)]) 
	email 				= 	EmailField		('email', 	validators=[DataRequired(), Email()])
	password 			= 	PasswordField	('password',validators=[DataRequired(), Length(min=8, max=20)]) 
	confirmpassword 	= 	PasswordField	('confirmpassword',validators=[DataRequired(), EqualTo('password', message='Password No Coincide')], id="confirm")
	submit 				= 	SubmitField		('Registrarme')

	def validate_username(self, username):
		user = User.query.filter_by(username.username.data).first()
		if user:
			flash("El usuario ya fue tomado. Use otro ")
			
	def validate_email(self, email):
		user = User.query.filter_by(email.email.data).first()
		if user:
			flash("El email ya fue tomado. Use otro ")

class formularioLogin(FlaskForm):
 # CAMPOS EN DB			   TIPO DE DATO		NOMBRE DE CAMPO EN HTML Y VALIDACIONES
	email 				= 	StringField		('email', validators=[DataRequired(), Email()])
	password 			= 	PasswordField	('password', validators=[DataRequired()]) 
	rememberme 			= 	BooleanField	('checkbox')
	submit 				= 	SubmitField		('Ingresar')

#**********************************************************************************************
#**********************************************************************************************








#MODELOS  *************************************************************************************
#**********************************************************************************************
class User(db.Model):
	id 					=	db.Column(db.Integer, 		primary_key=True)
	username 			= 	db.Column(db.String(20),	unique=True, 	nullable=False)
	email 				= 	db.Column(db.String(120),	unique=True, 	nullable=False)
	password 			= 	db.Column(db.String(60),	unique=True, 	nullable=False)
	confirmpassword		= 	db.Column(db.String(60),	unique=True, 	nullable=False)
	imagen_perfil		= 	db.Column(db.String(20),	nullable=False, default="default.jpg")
	posts 				= 	db.relationship("Post", 	backref="author", 	lazy=True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.password}','{self.confirmpassword}','{self.imagen_perfil}')"

class Post(db.Model):
	id 					=	db.Column(db.Integer, 		primary_key=True)
	title 				= 	db.Column(db.String(100),	nullable=False)
	date_posted			= 	db.Column(db.DateTime,		nullable=False,	default=datetime.utcnow)
	content 			= 	db.Column(db.Text, 			nullable=False)
	user_id 			=	db.Column(db.Integer,		db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}','{self.content}')"

#**********************************************************************************************
#**********************************************************************************************








#VIEWS  ***************************************************************************************
#**********************************************************************************************
@app.route("/") 
@app.route("/home") 
def home():
	titulo="Inicio"
	return render_template("index.html", vtitulo=titulo)

@app.route("/login", methods=["GET","POST"]) 
def login():
	titulo="Login"
	form = formularioLogin()

	return render_template("login.html", vtitulo=titulo, form=form)

@app.route("/registro", methods=["GET","POST"]) 
def registro():
	titulo="Registro"
	form = formularioRegistro()

	if request.method == "POST":
		username = User.query.filter_by(username=request.form["username"].lower()).first()
		email = User.query.filter_by(email=request.form["email"].lower()).first()
		if username or email:
			flash("Email o Usuario ya existen intente con otro", "warning")
		elif {form.password.data} != {form.confirmpassword.data}:
			flash(f"La contraseña y la verificación NO son iguales", "danger")
			return redirect(url_for("registro"))
		else:
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')	
			user = User(username=form.username.data, email=form.email.data, password=hashed_password, confirmpassword=hashed_password)
			db.session.add(user)
			db.session.commit()
			flash(f"Cuenta creada por {form.username.data}", "success")
			return redirect(url_for("login"))
	return render_template("registro.html", vtitulo=titulo, form=form)
#**********************************************************************************************
#**********************************************************************************************









#RUN*******************************************************************************************
#**********************************************************************************************
if __name__ 	== "__main__":
	db.create_all()
	app.run(debug = True, port = 81) 		
#**********************************************************************************************
#**********************************************************************************************						