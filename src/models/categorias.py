from sqlalchemy import Column, Integer, String 
from src.models import session, Base, engine


class Categorias(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(300), unique=True, nullable=False)
    
    def __init__(self, nombre_categoria):
        self.nombre_categoria = nombre_categoria
        
    def traer_categorias():
        categorias = session.query(categorias).all()
        return categorias


