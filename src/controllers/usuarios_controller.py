from flask import render_template, request
from flask_controller import FlaskController
from src.models.usuarios import Usuarios
from src.models.usuarios import Usuarios
from app import app

class UsuariosController(FlaskController):


@app.route('/formulario_usuario.html' ,methods=['GET','POST'])
def crear_usuarios():
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')        
        email = request.form.get('email')
        area = request.form.get('area')
        contraseña = request.form.get('contraseña')
        usuario_almacenar = Usuarios(nombre,fecha_nacimiento,cedula,telefono,email,area,contraseña)
        Usuario_repetido = Usuarios.traer_usuario_por_nombre(nombre)
        if Usuario_repetido:
            return render_template('formulario_usuario.html'
                                   ,titulo='Crear un usuario'
                                   ,errorProducto = "El nombre no se puede repetir"
                                   ,usuario = usuarios
                                   ,usuario_almacenar = usuario_almacenar)
        try:
            Usuarios.crear_usuario(usuario_almacenar)
        except:
            return render_template("formulario_usuario.html",titulo="Eror al registrar en la base de datos",usuarios = usuarios)
        return render_template("formulario_usuario.html",titulo="crear un usuario",usuarios = usuarios)