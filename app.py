from flask import Flask, render_template
 
 app = Flask(__name__)
 
 if __name__ == '__main__':
     app.run(debug=True)
 
 @app.route('/')
 def index():
     return render_template('index.html',titulo='Bienvenido a la aplicación de facturación')
 
 @app.route('/lista_productos')
 def lista_productos():
     return render_template('lista_productos.html',titulo='Ver productos')
 
 @app.route('/formulario_producto')
 def formulario_producto():
     return render_template('formulario_producto.html',titulo='Crear un productos')
 
 @app.route('/lista_clientes')
 def lista_clientes():
     return render_template('lista_clientes.html',titulo='ver clientes')
 
 @app.route('/formulario_cliente')
 def formulario_cliente():
     return render_template('formulario_cliente.html',titulo='Crear cliente')
 
 @app.route('/lista_facturas')
 def lista_facturas():
     return render_template('lista_facturas.html',titulo='ver facturas')
 
 @app.route('/formulario_factura')
 def formulario_factura():
     return render_template('formulario_factura.html',titulo='Crear factura')
 
 @app.route('/lista_usuarios')
 def lista_usuarios():
     return render_template('lista_usuarios.html',titulo='ver usuarios')
 
 @app.route('/formulario_usuario')
 def formulario_usuario():
     return render_template('formulario_usuario.html',titulo='Crear usuario')