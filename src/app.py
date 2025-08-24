from flask import Flask
from flask_controller import FlaskControllerRegister 
from src.models import Base, engine 
<<<<<<< HEAD
from src.controllers.facturas_controller import facturas_bp

app = Flask(__name__)
app.secret_key = 'derly2025'
=======


app = Flask(__name__)

>>>>>>> 19a1a418060f82a1bd470b87b9e26a74659bebf1

register_controllers = FlaskControllerRegister(app)
register_controllers.register_package("src.controllers")

<<<<<<< HEAD


app.register_blueprint(facturas_bp)
=======
Base.metadata.create_all(engine)
>>>>>>> 19a1a418060f82a1bd470b87b9e26a74659bebf1

if __name__ == '__main__':
    app.run(debug=True) 


