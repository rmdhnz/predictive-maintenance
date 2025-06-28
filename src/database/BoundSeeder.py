from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migration import BoundModel
import json
from config.config import DATABASE_URL

class BoundSeeder:
    def run(self):
        print("Menjalankan seeder data bounds...")

        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        bounds = [
            {
                "jenis": "normal",
                "range_0": json.dumps({"start": 25124 - 2, "end": 86282 - 1}),
                "range_50": json.dumps({"start": 86283 - 2, "end": 194493 - 1}),
                "range_100": json.dumps({"start": 319413 - 2, "end": 395785 - 1}),
                "nama": "coba",
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
