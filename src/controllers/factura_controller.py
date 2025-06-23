from flask import render_template, request
from flask_controller import FlaskController
from src.models.facturacion import Facturacion
from src.app import app

@app.route('/facturacion.html')
def facturacion():
    return render_template('facturacion.html')

