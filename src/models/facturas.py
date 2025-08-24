from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models import session, Base, engine

# Tabla intermedia para los items de la factura
factura_items = Table('factura_items', Base.metadata,
    Column('factura_id', Integer, ForeignKey('facturas.id'), primary_key=True),
    Column('producto_id', Integer, ForeignKey('productos.id'), primary_key=True),
    Column('cantidad', Integer, nullable=False),
    Column('precio_unitario', Float, nullable=False),
    Column('subtotal', Float, nullable=False)
)

class Facturas(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True)
    numero_factura = Column(String(20), unique=True, nullable=False)
    fecha_emision = Column(DateTime, default=datetime.utcnow)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    subtotal = Column(Float, default=0.0)
    iva = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    estado = Column(String(20), default='Pendiente')  # Pendiente, Pagada, Anulada
    
    # Relaciones
    cliente = relationship('Clientes', backref='facturas')
    items = relationship('Productos', secondary=factura_items, 
                        backref='facturas', lazy='dynamic')
    
    def __init__(self, numero_factura, cliente_id, items=None):
        self.numero_factura = numero_factura
        self.cliente_id = cliente_id
        if items:
            self.agregar_items(items)
    
    def agregar_items(self, items):
        """Agrega items a la factura y calcula totales"""
        from src.models.productos import Productos
        
        for item in items:
            producto = session.query(Productos).get(item['producto_id'])
            if producto:
                cantidad = item['cantidad']
                precio_unitario = producto.valor_unitario
                subtotal_item = cantidad * precio_unitario
                
                # Agregar item a la factura
                self.items.append(producto)
                # Actualizar cantidades en la tabla intermedia
                association = session.query(factura_items).filter(
                    factura_items.c.factura_id == self.id,
                    factura_items.c.producto_id == producto.id
                ).first()
                if association:
                    session.execute(
                        factura_items.update().where(
                            factura_items.c.factura_id == self.id,
                            factura_items.c.producto_id == producto.id
                        ).values(
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            subtotal=subtotal_item
                        )
                    )
                else:
                    session.execute(
                        factura_items.insert().values(
                            factura_id=self.id,
                            producto_id=producto.id,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            subtotal=subtotal_item
                        )
                    )
                
                # Actualizar stock
                producto.cantidad_stock -= cantidad
                
                # Actualizar totales
                self.subtotal += subtotal_item
        
        # Calcular IVA (19%) y total
        self.iva = self.subtotal * 0.19
        self.total = self.subtotal + self.iva
    
    @classmethod
    def crear_factura(cls, datos_factura):
        factura = cls(
            numero_factura=datos_factura['numero_factura'],
            cliente_id=datos_factura['cliente_id']
        )
        
        session.add(factura)
        session.flush()  # Para obtener el ID
        
        if 'items' in datos_factura:
            factura.agregar_items(datos_factura['items'])
        
        session.commit()
        return factura
    
    @classmethod
    def traer_facturas(cls):
        return session.query(Facturas).all()
    
    @classmethod
    def traer_factura_id(cls, id):
        return session.query(Facturas).filter(Facturas.id == id).first()
    
    @classmethod
    def traer_facturas_cliente(cls, cliente_id):
        return session.query(Facturas).filter(Facturas.cliente_id == cliente_id).all()
    
    @classmethod
    def actualizar_estado(cls, id, nuevo_estado):
        factura = session.query(Facturas).get(id)
        if factura:
            factura.estado = nuevo_estado
            session.commit()
            return factura
        return None
    
    @classmethod
    def eliminar_factura(cls, id):
        factura = session.query(Facturas).get(id)
        if factura:
            # Restaurar stock de productos
            for producto in factura.items:
                association = session.query(factura_items).filter(
                    factura_items.c.factura_id == factura.id,
                    factura_items.c.producto_id == producto.id
                ).first()
                if association:
                    producto.cantidad_stock += association.cantidad
            
            session.delete(factura)
            session.commit()
            return True
        return False
    
    def as_dict(self):
        return {
            'id': self.id,
            'numero_factura': self.numero_factura,
            'fecha_emision': self.fecha_emision.isoformat(),
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre if self.cliente else '',
            'subtotal': self.subtotal,
            'iva': self.iva,
            'total': self.total,
            'estado': self.estado,
            'items': self.obtener_items_detalle()
        }
    
    def obtener_items_detalle(self):
        items = []
        for producto in self.items:
            association = session.query(factura_items).filter(
                factura_items.c.factura_id == self.id,
                factura_items.c.producto_id == producto.id
            ).first()
            if association:
                items.append({
                    'producto_id': producto.id,
                    'codigo': producto.codigo,
                    'descripcion': producto.descripcion,
                    'cantidad': association.cantidad,
                    'precio_unitario': association.precio_unitario,
                    'subtotal': association.subtotal
                })
        return items