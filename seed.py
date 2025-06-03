#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migration import Base, MotorCurrent, MotorBRBCurrent3mm
from datetime import datetime
import pandas as pd

DATABASE_URL = f"mysql+pymysql://root:$Aviasi380@localhost/predictive_maintenance"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
df = pd.read_csv("data-brb-3mm/coba.csv")

range_0 = list(range(37531, 117066))
range_50 = list(range(412199, 446361))
range_100 = list(range(448556, 495125))
range_loads = range_0 + range_50 + range_100
df = df[df.index.isin(range_loads)].copy()
for id, row in df.iterrows():
    data = MotorBRBCurrent3mm(
        time=row["Time"],
        current=row["current"],
        load=(0 if id in range_0 else 50 if id in range_50 else 100),
    )
    print("Data ke : ", id)
    session.add(data)

session.commit()
session.close()
print("Import dari CSV selesai.")
