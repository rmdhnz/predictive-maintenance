from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migration import MotorBRB3_7_mm
import json


class Motor2BRB_3_7_mmSeeder:
    def run(self):
        print("Menjalankan seeder data bounds...")
        DATABASE_URL = (
            "mysql+pymysql://root:$Aviasi380@localhost/predictive_maintenance"
        )
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        datas = []

        for data in datas:
            pass

        session.commit()
        session.close()
        print("✅ Seeder Data selesai.")
