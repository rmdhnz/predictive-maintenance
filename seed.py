# seed.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import typer
import importlib

apps = typer.Typer()


@apps.command("db-seed")
def db_seed(
    class_name: str = typer.Option(..., "--class", "-c", help="Nama class seeder")
):
    try:
        module_path = f"src.database.{class_name}"
        module = importlib.import_module(module_path)
        seeder_class = getattr(module, class_name)
        seeder = seeder_class()
        seeder.run()
    except ModuleNotFoundError as e:
        print(f"❌ Modul '{module_path}' tidak ditemukan : ", e)
    except AttributeError as e:
        print(f"❌ Class '{class_name}' tidak ditemukan di modul '{module_path}'.", e)
    except Exception as e:
        print(f"❌ Terjadi error saat menjalankan seeder: {e}")


if __name__ == "__main__":
    apps()  # <== HARUS LANGSUNG app(), JANGAN main()
