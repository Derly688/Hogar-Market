from flask import render_template, request, session, redirect, url_for
from flask_controller import FlaskController
from src.models.productos import Productos
from src.models.categorias import Categorias
from src.app import app 
from src.models import session, Base


class ProductosController(FlaskController):
    
    
  @app.route ('/inventarios.html', methods=['GET','POST'])
  def lista_productos():
    productos = Productos.traer_productos()
    return render_template('inventarios.html',titulo='Ver productos', productos = productos)

  @app.route('/formulario_producto.html', methods=['GET','POST'])
  def formulario_producto():
        if request.method == 'POST':
            codigo = request.form.get('codigo')
            descripcion = request.form.get('descripcion')
            valor_unitario = request.form.get('valor_unitario')
            cantidad_inventario = request.form.get('cantidad_inventario')        
            unidad_medida = request.form.get('unidad_medida')
            categoria = request.form.get('categoria')
            producto = Productos(codigo,descripcion,valor_unitario,unidad_medida,cantidad_inventario,categoria)
            Productos.crear_producto(producto)
             
        return render_template('formulario_producto.html',titulo='Crear un producto')
