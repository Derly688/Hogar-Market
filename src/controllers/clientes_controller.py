<<<<<<< HEAD
from flask import render_template, request, redirect, url_for, flash
from flask_controller import FlaskController
from src.models.clientes import Clientes
from src.app import app
from src.models import session as db_session
from datetime import datetime
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

    @app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
    def editar_cliente(id):
        try:
            cliente = Clientes.traer_cliente_id(id)

            if not cliente:
                flash('Cliente no encontrado', 'error')
                return redirect(url_for('clientes'))
            
            if request.method == 'POST':
                
                datos = {
                    'nombre': request.form.get('nombre'),
                    'fecha_nacimiento': request.form.get('fecha_nacimiento'),
                    'cedula': request.form.get('cedula'),
                    'telefono': request.form.get('telefono'),
                    'email': request.form.get('email'),
                     
                }
                
        
                
                
                


                cliente_actualizado = Clientes.actualizar_cliente(id, datos)
                if cliente_actualizado:
                    flash('Cliente actualizado exitosamente', 'success')
                else:
                    flash('Error al actualizar cliente', 'error')

                return redirect(url_for('gestion_clientes', id=id))

            fecha_formateada = cliente.fecha_nacimiento.strftime('%Y-%m-%d') if cliente.fecha_nacimiento else ''
            
            return render_template('editar_cliente.html', 
                                 titulo='Editar cliente', 
                                 cliente=cliente,
                                 fecha_formateada=fecha_formateada)
        
        except Exception as e:
            db_session.rollback()
            flash(f'Error al editar cliente: {str(e)}', 'error')
            return redirect(url_for('/clientes.html'))

    @app.route('/eliminar_cliente/<int:id>', methods=['POST'])
    def eliminar_cliente(id):
        try:
            if Clientes.eliminar_cliente(id):
                flash('Cliente eliminado exitosamente', 'success')
            else:
                flash('Cliente no encontrado', 'error')
        except Exception as e:
            db_session.rollback()
            flash(f'Error al eliminar cliente: {str(e)}', 'error')

        return redirect(url_for('clientes'))
=======
from flask import render_template, request
from flask_controller import FlaskController
from src.models.clientes import Clientes
from src.app import app

class ClientesController(FlaskController):
    @app.route('/formulario_clientes.html')
    def gestion_clientes():
     return render_template('formulario_clientes.html',titulo='Ver productos')
    
>>>>>>> 19a1a418060f82a1bd470b87b9e26a74659bebf1
