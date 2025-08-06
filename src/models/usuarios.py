from sqlalchemy import Column, Integer, String, Date
from src.models import session, Base, engine

class Usuarios(Base):  
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100) )
    fecha_nacimiento = Column(Date())
    cedula = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(15))
    email = Column(String(20))
    area = Column(String(20))
    contraseña = Column(String(30), nullable=False)


    def __init__(self, id ,nombre,fecha_nacimiento,cedula,telefono,email,area,contraseña): 
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.cedula = cedula
        self.telefono = telefono
        self.email = email
        self.area = area
        self.contraseña = contraseña

    def crear_usuario(usuario):
        usuario = session.add(usuario)
        session.commit()
        return usuario

    def traer_usuarios():
        usuarios = session.query(Usuarios).all()
        return usuarios
    
