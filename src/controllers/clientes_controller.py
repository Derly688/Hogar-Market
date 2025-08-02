from flask import render_template, request
from flask_controller import FlaskController
from src.models.clientes import Clientes
from src.app import app

class ClientesController(FlaskController):
    @app.route('/clientes.html')
    def gestion_clientes():
     return render_template('clientes.html',titulo='Ver productos')
    