from flask import Flask
from flask_controller import FlaskControllerRegister 
from src.models import Base, engine 
from src.controllers.facturas_controller import facturas_bp

app = Flask(__name__)
app.secret_key = 'derly2025'

register_controllers = FlaskControllerRegister(app)
register_controllers.register_package("src.controllers")



app.register_blueprint(facturas_bp)

if __name__ == '__main__':
    app.run(debug=True) 


