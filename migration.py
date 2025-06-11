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
    time = Column(String(20))
    current = Column(Float)
    load = Column(Integer)


class MotorBRBCurrent3mm(Base):
    __tablename__ = "motor_brb_current_3mm"
    id = Column(Integer, primary_key=True)
    time = Column(String(20))
    current = Column(Float)
    load = Column(Integer)


class MotorBRBCurrent7mm(Base):
    __tablename__ = "motor_brb_current_7mm"
    id = Column(Integer, primary_key=True)
    time = Column(String(20))
    current = Column(Float)
    load = Column(Integer)


class MotorBRB3_7_mm(Base):
    __tablename__ = "motor_2_brb_current_3_7_mm"
    id = Column(Integer, primary_key=True)
    time = Column(String(20))
    current = Column(Float)
    load = Column(Integer)


class MotorDB(Base):
    __tablename__ = "motor_db"
    id = Column(Integer, primary_key=True)
    frequency = Column(Float)
    current_magnitude = Column(Float)
    load = Column(Integer)


class BoundModel(Base):
    __tablename__ = "bounds"
    id = Column(Integer, primary_key=True)
    jenis = Column(String(255))
    range_0 = Column(String(255))
    range_50 = Column(String(255))
    range_100 = Column(String(255))
    nama = Column(String(255))
