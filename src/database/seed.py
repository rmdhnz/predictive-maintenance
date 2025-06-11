#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migration import MotorCurrent
from datetime import datetime
import pandas as pd

DATABASE_URL = f"mysql+pymysql://root:$Aviasi380@localhost/predictive_maintenance"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
df = pd.read_csv("data/coba.csv")
