from flask import render_template, request
from flask_controller import FlaskController
from src.models.usuarios import Usuarios
from src.app import app
from src.models import Session,Base


class UsuariosController(FlaskController):


    @app.route('/usuarios.html', methods=['GET', 'POST'])
    def usuarios():
        usuarios = Usuarios.traer_usuarios()
        return render_template('usuarios.html',titulo='Ver productos', usuarios = usuarios)

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
            
        return render_template('crearnuevousuario.html', titulo='ver productos')
    
   