from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migration import BoundModel
import json


class BoundSeeder:
    def run(self):
        print("Menjalankan seeder data bounds...")

        # Koneksi ke database
        DATABASE_URL = (
            "mysql+pymysql://root:$Aviasi380@localhost/predictive_maintenance"
        )
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        bounds = [
            {
                "jenis": "2_brb_7_7_mm",
                "range_0": json.dumps({"start": 2, "end": 67866}),
                "range_50": json.dumps({"start": 67867, "end": 128354}),
                "range_100": json.dumps({"start": 128355, "end": 193392}),
                "nama": "coba_3",
            }
        ]

        for bound in bounds:
            print(f"Menambahkan bound: {bound['jenis']} | ({bound['nama']})")

            data = BoundModel(
                jenis=bound["jenis"],
                range_0=bound["range_0"],
                range_50=bound["range_50"],
                range_100=bound["range_100"],
                nama=bound["nama"],
            )

            session.add(data)

        session.commit()
        session.close()
        print("✅ Seeder bounds selesai.")
