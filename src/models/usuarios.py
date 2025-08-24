from sqlalchemy import Column, Integer, String, Date
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import session, Base, engine

class Usuarios(Base):  
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    fecha_nacimiento = Column(Date())
    cedula = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(15))
    email = Column(String(50))  
    area = Column(String(20))
    contraseña = Column(String(255), nullable=False)  

    def __init__(self, nombre, fecha_nacimiento, cedula, telefono, email, area, contraseña): 
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.cedula = cedula
        self.telefono = telefono
        self.email = email
        self.area = area
        self.set_password(contraseña)

    @classmethod
    def crear_usuario(cls, usuario):
        session.add(usuario)
        session.commit()
        return usuario

    @classmethod
    def traer_usuarios(cls):
        usuarios = session.query(Usuarios).all()
        return usuarios
    
    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)
    
    @classmethod
    def traer_usuario_id(cls, id):
        usuario = session.query(Usuarios).filter(Usuarios.id == id).first()
        return usuario
    
    @classmethod
    def actualizar_usuario(cls, id, datos):
        usuario = session.query(Usuarios).get(id)
        if usuario:
            for key, value in datos.items():
                if hasattr(usuario, key) and value is not None:
                    if key == 'contraseña' and value:  
                        usuario.set_password(value)
                    elif key != 'contraseña':  
                        setattr(usuario, key, value)
            session.commit()
            return usuario
        return None
    
    @classmethod
    def eliminar_usuario(cls, id):
        usuario = session.query(Usuarios).get(id)
        if usuario:
            session.delete(usuario)
            session.commit()
            return True
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}