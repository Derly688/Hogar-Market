from flask import render_template, request, redirect, url_for, flash, session
from flask_controller import FlaskController
from src.models.productos import Productos
from src.app import app
from src.models import session as db_session
from datetime import datetime


class ProductosController(FlaskController):
    
    @app.route('/inventarios.html', methods=['GET','POST'])
    def inventarios():
        productos = Productos.traer_productos()
        return render_template('inventarios.html', titulo='Inventario', productos=productos)

    @app.route('/formulario_producto.html', methods=['GET','POST'])
    def formulario_producto():
        if request.method == 'POST':
            codigo = request.form.get('codigo')
            descripcion = request.form.get('descripcion')
            unidad_medida = request.form.get('unidad_medida')
            cantidad_inventario = request.form.get('cantidad_inventario')        
            categoria = request.form.get('categoria')
            valor_unitario = request.form.get('valor_unitario')
            producto = Productos(codigo, descripcion, unidad_medida, cantidad_inventario, categoria, valor_unitario)
            Productos.crear_producto(producto)
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('inventarios'))
             
        return render_template('formulario_producto.html', titulo='Crear un producto')

    @app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
    def editar_producto(id):
        try:
            producto = Productos.traer_producto_id(id)
            
            if not producto:
                flash('Producto no encontrado', 'error')
                return redirect(url_for('inventarios'))
            
            if request.method == 'POST':
                datos = {
                    'codigo': request.form.get('codigo'),
                    'descripcion': request.form.get('descripcion'),
                    'unidad_medida': request.form.get('unidad_medida'),
                    'cantidad_inventario': request.form.get('cantidad_inventario'),
                    'categoria': request.form.get('categoria'),
                    'valor_unitario': request.form.get('valor_unitario'),
                }
                
                producto_actualizado = Productos.actualizar_producto(id, datos)
                if producto_actualizado:
                    flash('Producto actualizado exitosamente', 'success')
                else:
                    flash('Error al actualizar producto', 'error')
                
                return redirect(url_for('inventarios', id = id))
            
            return render_template('editar_producto.html', 
                                titulo='Editar producto', 
                                producto=producto)
        
        except Exception as e:
            db_session.rollback()
            flash(f'Error al editar producto: {str(e)}', 'error')
            return redirect(url_for('/inventarios.html', id=id))

    @app.route('/eliminar_producto/<int:id>', methods=['POST'])
    def eliminar_producto(id):
        try:
            if Productos.eliminar_producto(id):
                flash('Producto eliminado exitosamente', 'success')
            else:
                flash('Producto no encontrado', 'error')
        except Exception as e:
            db_session.rollback()
            flash(f'Error al eliminar producto: {str(e)}', 'error')

        return redirect(url_for('inventarios'))