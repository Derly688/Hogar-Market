from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models.facturas import Facturas
from src.models.clientes import Clientes
from src.models.productos import Productos
from datetime import datetime

facturas_bp = Blueprint('facturas', __name__)

@facturas_bp.route('/facturacion.html')
def lista_facturas():
    facturas = Facturas.traer_facturas()
    return render_template('facturacion.html', facturas=facturas)

@facturas_bp.route('/facturas/nueva', methods=['GET', 'POST'])
def nueva_factura():
    if request.method == 'POST':
        try:
            print("DEBUG: Datos del formulario recibidos:")
            print("DEBUG: Form data completo:", dict(request.form))
            
            # Validar datos básicos
            numero_factura = request.form.get('numero_factura')
            cliente_id = request.form.get('cliente_id')
            
            if not numero_factura or not cliente_id:
                flash('Número de factura y cliente son obligatorios', 'error')
                return redirect(url_for('facturas.nueva_factura'))
            
            # Obtener productos seleccionados (checkboxes)
            productos_seleccionados = request.form.getlist('producto_id')
            print(f"DEBUG: Productos seleccionados: {productos_seleccionados}")
            
            if not productos_seleccionados:
                flash('Debe seleccionar al menos un producto', 'error')
                return redirect(url_for('facturas.nueva_factura'))
            
            # Procesar items de la factura
            items = []
            for producto_id in productos_seleccionados:
                cantidad_key = f'cantidad_{producto_id}'
                cantidad = request.form.get(cantidad_key)
                
                print(f"DEBUG: Producto {producto_id}, buscando campo {cantidad_key}, valor: {cantidad}")
                
                if cantidad and int(cantidad) > 0:
                    items.append({
                        'producto_id': int(producto_id),
                        'cantidad': int(cantidad)
                    })
                else:
                    print(f"WARNING: Producto {producto_id} seleccionado pero sin cantidad válida")
            
            print(f"DEBUG: Items procesados: {items}")
            
            if not items:
                flash('Debe especificar cantidades válidas para los productos seleccionados', 'error')
                return redirect(url_for('facturas.nueva_factura'))
            
            # Crear datos de la factura
            datos_factura = {
                'numero_factura': numero_factura,
                'cliente_id': int(cliente_id),
                'items': items
            }
            
            print(f"DEBUG: Enviando a crear_factura: {datos_factura}")
            
            # Crear la factura
            factura = Facturas.crear_factura(datos_factura)
            
            flash(f'Factura #{factura.numero_factura} creada exitosamente', 'success')
            return redirect(url_for('facturas.detalle_factura', id=factura.id))
            
        except Exception as e:
            print(f"ERROR en nueva_factura: {e}")
            flash(f'Error al crear factura: {str(e)}', 'error')
            return redirect(url_for('facturas.nueva_factura'))
    
    # GET: Mostrar formulario
    clientes = Clientes.traer_clientes()
    productos = Productos.traer_productos()
    return render_template('nueva_factura.html', 
                         clientes=clientes, 
                         productos=productos)

@facturas_bp.route('/facturas/<int:id>')
def detalle_factura(id):
    factura = Facturas.traer_factura_id(id)
    if not factura:
        flash('Factura no encontrada', 'error')
        return redirect(url_for('facturas.lista_facturas'))
    
    return render_template('detalle_factura.html', factura=factura)

@facturas_bp.route('/facturas/cliente/<int:cliente_id>')
def facturas_cliente(cliente_id):
    facturas = Facturas.traer_facturas_cliente(cliente_id)
    cliente = Clientes.traer_cliente_id(cliente_id)
    return render_template('facturas/facturas_cliente.html', 
                         facturas=facturas, 
                         cliente=cliente)

@facturas_bp.route('/facturas/<int:id>/anular', methods=['POST'])
def anular_factura(id):
    factura = Facturas.actualizar_estado(id, 'Anulada')
    if factura:
        flash('Factura anulada exitosamente', 'success')
    else:
        flash('Error al anular factura', 'error')
    return redirect(url_for('facturas.detalle_factura', id=id))

@facturas_bp.route('/facturas/<int:id>/pagar', methods=['POST'])
def pagar_factura(id):
    factura = Facturas.actualizar_estado(id, 'Pagada')
    if factura:
        flash('Factura marcada como pagada', 'success')
    else:
        flash('Error al actualizar estado', 'error')
    return redirect(url_for('facturas.detalle_factura', id=id))

@facturas_bp.route('/facturas/<int:id>/eliminar', methods=['POST'])
def eliminar_factura(id):
    if Facturas.eliminar_factura(id):
        flash('Factura eliminada exitosamente', 'success')
    else:
        flash('Error al eliminar factura', 'error')
    return redirect(url_for('facturas.lista_facturas'))

# API endpoints
@facturas_bp.route('/api/facturas', methods=['GET'])
def api_facturas():
    facturas = Facturas.traer_facturas()
    return jsonify([factura.as_dict() for factura in facturas])

@facturas_bp.route('/api/facturas/<int:id>', methods=['GET'])
def api_factura(id):
    factura = Facturas.traer_factura_id(id)
    if factura:
        return jsonify(factura.as_dict())
    return jsonify({'error': 'Factura no encontrada'}), 404

@facturas_bp.route('/api/facturas', methods=['POST'])
def api_crear_factura():
    try:
        data = request.get_json()
        factura = Facturas.crear_factura(data)
        return jsonify(factura.as_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400