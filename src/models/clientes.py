from sqlalchemy import Column, Integer, String, Float, ForeignKey,Date,engine
from src.models import session, Base, engine

class Clientes(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, )
    fecha_nacimiento = Column(Date())
    cedula = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(15))
    email = Column(String(20))

    def __init__(self, nombre,fecha_nacimiento,cedula,telefono,email):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.cedula = cedula
        self.telefono = telefono
        self.email = email
        
    def crear_cliente(cliente):
        cliente = session.add(cliente)
        session.commit()
        return cliente
    
    def traer_clientes():
        clientes = session.query(Clientes).all()
        return clientes
    
    def traer_cliente_id(id):
        cliente = session.query(Clientes).filter(Clientes.id_cliente == id).first()
        print(cliente)
        return cliente.as_dict()
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
