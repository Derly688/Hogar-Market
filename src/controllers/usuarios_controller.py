from flask import render_template, request, redirect, url_for, flash
from flask_controller import FlaskController
from src.models.usuarios import Usuarios
from src.app import app
from src.models import session as db_session
from datetime import datetime

class UsuariosController(FlaskController):
    
    @app.route('/formulario_usuario.html', methods=['GET','POST'])
    def crear_usuarios():
        if request.method == 'POST':
            try:
                nombre = request.form.get('nombre')
                fecha_nacimiento = request.form.get('fecha_nacimiento')
                cedula = request.form.get('cedula')
                telefono = request.form.get('telefono')        
                email = request.form.get('email')
                area = request.form.get('area')
                contraseña = request.form.get('contraseña')
                
            
                
                usuario = Usuarios(nombre, fecha_nacimiento, cedula, telefono, email, area, contraseña)
                Usuarios.crear_usuario(usuario)
                flash('Usuario creado exitosamente', 'success')
                return redirect(url_for('usuarios'))
                
            except Exception as e:
                db_session.rollback()
                flash(f'Error al crear usuario: {str(e)}', 'error')
        
        return render_template('formulario_usuario.html', titulo='Crear Usuario')
    
    @app.route('/usuarios.html')
    def usuarios():
        try:
            usuarios = Usuarios.traer_usuarios()
            return render_template('usuarios.html', titulo='Lista de Usuarios', usuarios=usuarios)
        except Exception as e:
            flash(f'Error al cargar usuarios: {str(e)}', 'error')
            return render_template('usuarios.html', titulo='Lista de Usuarios', usuarios=[])
    

    @app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
    def editar_usuario(id):
        try:
            usuario = Usuarios.traer_usuario_id(id)
            
            if not usuario:
                flash('Usuario no encontrado', 'error')
                return redirect(url_for('usuarios'))
            
            if request.method == 'POST':
                
                datos = {
                    'nombre': request.form.get('nombre'),
                    'fecha_nacimiento': request.form.get('fecha_nacimiento'),
                    'cedula': request.form.get('cedula'),
                    'telefono': request.form.get('telefono'),
                    'email': request.form.get('email'),
                    'area': request.form.get('area'),
                    'contraseña': request.form.get('contraseña')  
                }
                
        
                
                
                
                
               
                usuario_actualizado = Usuarios.actualizar_usuario(id, datos)
                if usuario_actualizado:
                    flash('Usuario actualizado exitosamente', 'success')
                else:
                    flash('Error al actualizar usuario', 'error')
                
                return redirect(url_for('usuarios', id = id))
            
            
            fecha_formateada = usuario.fecha_nacimiento.strftime('%Y-%m-%d') if usuario.fecha_nacimiento else ''
            
            return render_template('editar_usuario.html', 
                                 titulo='Editar usuario', 
                                 usuario=usuario,
                                 fecha_formateada=fecha_formateada)
        
        except Exception as e:
            db_session.rollback()
            flash(f'Error al editar usuario: {str(e)}', 'error')
            return redirect(url_for('usuarios'))

    @app.route('/eliminar_usuario/<int:id>', methods=['POST'])
    def eliminar_usuario(id):
        try:
            if Usuarios.eliminar_usuario(id):
                flash('Usuario eliminado exitosamente', 'success')
            else:
                flash('Usuario no encontrado', 'error')
        except Exception as e:
            db_session.rollback()
            flash(f'Error al eliminar usuario: {str(e)}', 'error')
        
        return redirect(url_for('usuarios'))