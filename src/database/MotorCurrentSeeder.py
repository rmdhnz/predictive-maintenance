from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migration import Base, MotorCurrent, MotorBRBCurrent3mm
from datetime import datetime
import pandas as pd


class MotorCurrentSeeder:
    def run(self):
        DATABASE_URL = (
            f"mysql+pymysql://root:$Aviasi380@localhost/predictive_maintenance"
        )
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        df = pd.read_csv("data/coba-1.CSV")
