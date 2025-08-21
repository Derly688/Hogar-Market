from flask import render_template, request, redirect, url_for, flash
from flask_controller import FlaskController
from src.models.usuarios import Usuarios
from src.app import app
from src.models import Session,Base
from src.models import session

class UsuariosController(FlaskController):
    
    @app.route('/usuarios.html', methods=['GET', 'POST'])
    def usuarios():
        usuarios = Usuarios.traer_usuarios()
        return render_template('usuarios.html',titulo='Usuarios', usuarios = usuarios)

    @app.route('/crearnuevousuario.html' ,methods=['GET','POST'])
    def crearnuevousuario():
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            fecha_nacimiento = request.form.get('fecha_nacimiento')
            cedula = request.form.get('cedula')
            telefono = request.form.get('telefono')        
            email = request.form.get('email')
            area = request.form.get('area')
            contraseña = request.form.get('contraseña')
            usuario = Usuarios(nombre,fecha_nacimiento,cedula,telefono,email,area,contraseña)
            Usuarios.crear_usuario(usuario)    
            
        return render_template('crearnuevousuario.html', titulo='ver usuarios')
    
    @app.route('/editar_usuarios/<id>', methods=['GET', 'POST'])
    def editar_usuarios(id):
     usuario = session.query(Usuarios).filter_by(id=id).first()

     if not usuario:
        return "Usuario no encontrado", 404

     if request.method == 'POST':
        usuario.nombre = request.form.get('nombre')
        usuario.fecha_nacimiento = request.form.get('fecha_nacimiento')
        usuario.cedula = request.form.get('cedula')
        usuario.telefono = request.form.get('telefono')
        usuario.email = request.form.get('email')
        usuario.area = request.form.get('area')
        contraseña = request.form.get('contraseña')

        if contraseña:  # solo actualizar si escribió algo nuevo
            usuario.set_password(contraseña)

        session.commit()
        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for('usuarios'))

     return render_template('editar_usuario.html', titulo='Editar Usuario', usuario = usuario)


    @app.route('/usuarios/eliminar/<id>', methods=['POST', 'GET'])
    def eliminar_usuario(id):
     usuario = session.query(Usuarios).filter_by(id=id).first()

     if usuario:
        session.delete(usuario)
        session.commit()
        print("Usuario eliminado correctamente", "success")
     else:
        print("Usuario no encontrado", "danger")

     return redirect(url_for('usuarios'))