from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
	print(__name__)
	return "Hola Mundo"

if __name__ == "__main__":
	app.run(debug = True, port = 81) 		
						
						