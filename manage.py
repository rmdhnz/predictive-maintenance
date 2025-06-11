# manage.py
import typer
import importlib

apps = typer.Typer()


@apps.command("db-seed")
def db_seed(
    class_name: str = typer.Option(..., "--class", "-c", help="Nama class seeder")
):
    """
    Menjalankan seeder berdasarkan nama class
    Contoh: python manage.py db-seed --class BoundSeeder
    """
    try:
        module_path = f"src.database.{class_name}"
        module = importlib.import_module(module_path)
        seeder_class = getattr(module, class_name)
        seeder = seeder_class()
        seeder.run()
    except ModuleNotFoundError:
        print(f"❌ Modul '{module_path}' tidak ditemukan.")
    except AttributeError:
        print(f"❌ Class '{class_name}' tidak ditemukan di modul '{module_path}'.")
    except Exception as e:
        print(f"❌ Terjadi error saat menjalankan seeder: {e}")


if __name__ == "__main__":
    apps()  # <== HARUS LANGSUNG app(), JANGAN main()
