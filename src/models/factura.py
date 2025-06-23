from sqlalchemy import Column, Integer, String 
from src.models import session, Base

class Factura(Base):
    __tablename__ = 'factura'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(String(100))
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Float)

    def __init__(id,cliente,fecha,total):
        self.id = id
        self.cliente = cliente
        self.fecha = fecha
        self.total = total
        
    def crear_factura(factura):
        factura = session.add(factura)
        session.commit()
        return factura
    
    def traer_factura():
        factura = session.query(factura).all()
        return factura
    # Cambio para forzar commit
