from flask import render_template, request
from flask_controller import FlaskController
from src.app import app

class FacturaController(FlaskController):
    @app.route('/factura.html')
    def facturacion():
        facturas = Facturas.traer_facturas()
        return render_template('factura.html', titulo="ver productos", facturas = facturas)
   

