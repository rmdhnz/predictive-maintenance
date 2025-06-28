from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from model.BoundModel import BoundModel
from model.MotorModel import MotorModel
from migration import MotorCurrent
from config.config import DATABASE_URL


class MotorCurrentSeeder:
    def run(self):
        bound_model = BoundModel()

        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        nama, jenis, folder = "coba_5", "normal", "data"
        bounder = bound_model.where(nama=nama, jenis=jenis).first()
        ranges = bound_model.make_range(bounder)
        ranges_merge = bound_model.make_range(bounder, merge=True)
        df = pd.read_csv(f"{folder}/{nama}.csv")
        df = df[df.index.isin(ranges_merge)].copy()
        for id, row in df.iterrows():
            data = MotorCurrent(
                time=row["Time"],
                current=row["current"],
                percent_load=(
                    0
                    if id in ranges["range_0"]
                    else 50 if id in ranges["range_50"] else 100
                ),
                label_id=0,
            )
            print("Data ke : ", id)
            session.add(data)
        session.commit()
        session.close()
        print("Import dari CSV selesai.")
