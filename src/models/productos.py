from sqlalchemy import Column, Integer, String, Float, ForeignKey  
from src.models import session, Base, engine
from src.models.categorias import Categorias
from werkzeug.security import generate_password_hash, check_password_hash

class Productos(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    codigo = Column(String(9), unique=True, nullable=False)
    descripcion = Column(String(300), unique=True, nullable=False)
    unidad_medida = Column(String(3), nullable=False)
    cantidad_stock = Column(Integer)
    categoria = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    valor_unitario = Column(Float)

    def __init__(self,codigo,descripcion,unidad_medida,cantidad_stock,categoria,valor_unitario,):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad_medida = unidad_medida
        self.cantidad_stock = cantidad_stock
        self.categoria = categoria
        self.valor_unitario = valor_unitario

    
    @classmethod
    def crear_producto(cls, producto):
        session.add(producto)
        session.commit()
        return producto

    @classmethod
    def traer_productos(cls):
        productos = session.query(Productos).all()
        return productos
    
    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)
    
    @classmethod
    def traer_producto_id(cls, id):
        producto = session.query(Productos).filter(Productos.id == id).first()
        return producto

    @classmethod
    def actualizar_producto(cls, id, datos):
        producto = session.query(Productos).get(id)
        if producto:
            for key, value in datos.items():
                if hasattr(producto, key) and value is not None:
                    if key == 'contraseña' and value:  
                        producto.set_password(value)
                    elif key != 'contraseña':  
                        setattr(producto, key, value)
            session.commit()
            return producto
        return None
    
    @classmethod
    def eliminar_producto(cls, id):
        producto = session.query(Productos).get(id)
        if producto:
            session.delete(producto)
            session.commit()
            return True
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}