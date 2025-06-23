from flask import render_template, request
from flask_controller import FlaskController
from src.models.factura import Factura
from src.app import app

@app.route('/factura.html')
def factura():
    return render_template('factura.html')


