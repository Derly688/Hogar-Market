from src.app import app
from flask import render_template
from flask_controller import FlaskController


class HomeController(FlaskController):
    
    
    @app.route('/index.html')
    def cerrar_sesion():
        return render_template('index.html')