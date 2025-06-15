from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from model.BoundModel import BoundModel
from migration import MotorBRB3_7_mm as DataInput


class Motor2BRB_3_7_mmSeeder:
    def run(self):
        bound_model = BoundModel()
        DATABASE_URL = (
            f"mysql+pymysql://root:$Aviasi380@localhost/predictive_maintenance"
        )
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        nama, jenis, folder = "coba_3", "2_brb_3_7_mm", "data-brb-3-7-mm"
        bounder = bound_model.where(nama=nama, jenis=jenis).first()
        ranges = bound_model.make_range(bounder)
        ranges_merge = bound_model.make_range(bounder, merge=True)
        df = pd.read_csv(f"{folder}/{nama}.csv")
        df = df[df.index.isin(ranges_merge)].copy()
        for id, row in df.iterrows():
            data = DataInput(
                time=row["Time"],
                current=row["current"],
                percent_load=(
                    0
                    if id in ranges["range_0"]
                    else 50 if id in ranges["range_50"] else 100
                ),
                label_id=3,
            )
            print("Data ke : ", id)
            session.add(data)
        session.commit()
        session.close()
        print("Import dari CSV selesai.")
