from flask import render_template, request
from flask_controller import FlaskController
from src.app import app

class FacturaController(FlaskController):
    @app.route('/facturacion.html')
    def factura():
        return render_template('factura.html')


