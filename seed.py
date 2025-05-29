#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migration import Base, MotorCurrent
from datetime import datetime
import pandas as pd

DATABASE_URL = f"mysql+pymysql://root:$Aviasi380@localhost/predictive_maintenance"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
df = pd.read_csv("data/simulated_motor_data.csv")

for id,row in df.iterrows() :
  data = MotorCurrent(
    time=row['current_normal'],
    current_normal = row['current_normal'],
    current_fault=row['current_fault']
  )
  session.add(data)

session.commit()
session.close()
print("Import dari CSV selesai.")