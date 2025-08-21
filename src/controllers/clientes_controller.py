from flask import render_template, request
from flask_controller import FlaskController
from src.models.clientes import Clientes
from src.models import Session,Base
from src.app import app

class ClientesController(FlaskController):

    @app.route('/clientes.html')
    def gestion_clientes():
     clientes = Clientes.traer_clientes()
     return render_template('clientes.html',titulo='Clientes', clientes = clientes )

    @app.route('/formulario_clientes.html', methods = ['GET', 'POST'] )
    def formulario_clientes():
     if request.method == 'POST':
                nombre = request.form.get('nombre')
                fecha_nacimiento = request.form.get('fecha_nacimiento')
                cedula = request.form.get('cedula')
                telefono = request.form.get('telefono')        
                email = request.form.get('email')
                cliente = Clientes(nombre,fecha_nacimiento,cedula,telefono,email,)
                Clientes.crear_cliente(cliente)
                
     return render_template('formulario_clientes.html', titulo='Clientes')

    @app.route('/editar_clientes/<id>', methods = ['GET', 'POST'] )
    def editar_clientes(id):
        cliente = Clientes.traer_cliente_id(id)
        if request.method == 'POST':
                nombre = request.form.get('nombre')
                fecha_nacimiento = request.form.get('fecha_nacimiento')
                cedula = request.form.get('cedula')
                telefono = request.form.get('telefono')        
                email = request.form.get('email')
                cliente = Clientes(nombre,fecha_nacimiento,cedula,telefono,email,)
                Clientes.crear_cliente(cliente)
                
        return render_template('editarcliente.html', cliente = cliente, titulo='Editar Cliente')
