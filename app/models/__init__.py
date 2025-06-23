from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Date
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

engine = create_engine("mysql+pymysql://root@localhost/merkalogic?charset=utf8mb4")

connection = engine.connect()

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()
Base.metadata.bind = engine


Base.metadata.create_all(engine)