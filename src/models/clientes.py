from sqlalchemy import Column, Integer, String, Float, ForeignKey,Date,engine
<<<<<<< HEAD
from src.models import session, Base, engine
from werkzeug.security import generate_password_hash, check_password_hash

class Clientes(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
=======
from src.models import session, Base

class Clientes(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True)
>>>>>>> 19a1a418060f82a1bd470b87b9e26a74659bebf1
    nombre = Column(String(100), nullable=False, )
    fecha_nacimiento = Column(Date())
    cedula = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(15))
    email = Column(String(20))

<<<<<<< HEAD
    def __init__(self, nombre,fecha_nacimiento,cedula,telefono,email):
=======
    def __init__(self,nombre,fecha_nacimiento,cedula,telefono,email):
>>>>>>> 19a1a418060f82a1bd470b87b9e26a74659bebf1
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.cedula = cedula
        self.telefono = telefono
        self.email = email
        
<<<<<<< HEAD
    @classmethod
    def crear_cliente(cls, cliente):
        session.add(cliente)
        session.commit()
        return cliente

    @classmethod
    def traer_clientes(cls):
        clientes = session.query(Clientes).all()
        return clientes
    
    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)
    
    @classmethod
    def traer_cliente_id(cls, id):
        cliente = session.query(Clientes).filter(Clientes.id == id).first()
        return cliente

    @classmethod
    def actualizar_cliente(cls, id, datos):
        cliente = session.query(Clientes).get(id)
        if cliente:
            for key, value in datos.items():
                if hasattr(cliente, key) and value is not None:
                    if key == 'contraseña' and value:  
                        cliente.set_password(value)
                    elif key != 'contraseña':  
                        setattr(cliente, key, value)
            session.commit()
            return cliente
        return None
    
    @classmethod
    def eliminar_cliente(cls, id):
        cliente = session.query(Clientes).get(id)
        if cliente:
            session.delete(cliente)
            session.commit()
            return True
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
=======
    def crear_cliente(cliente):
        cliente = session.add(cliente)
        session.commit()
        return cliente
    
    def traer_clientes():
        clientes = session.query(Clientes).all()
        return clientes



>>>>>>> 19a1a418060f82a1bd470b87b9e26a74659bebf1
