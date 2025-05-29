from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

DATABASE_URL = f"mysql+pymysql://root:$Aviasi380@localhost/predictive_maintenance"

engine = create_engine(DATABASE_URL)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))


class MotorCurrent(Base):
    __tablename__ = "motor_current"

    id = Column(Integer, primary_key=True)
    time = Column(Float)
    current_normal = Column(Float)
    current_fault = Column(Float)
