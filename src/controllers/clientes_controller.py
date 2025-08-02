from flask import render_template, request
from flask_controller import FlaskController
from src.models.clientes import Clientes
from src.app import app

class ClientesController(FlaskController):
    @app.route('/formulario_clientes.html')
    def gestion_clientes():
     return render_template('formulario_clientes.html',titulo='Ver productos')
    