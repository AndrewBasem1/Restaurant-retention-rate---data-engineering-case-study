from sqlmodel import create_engine
from pathlib import Path

db_path = Path(__file__).parent / "sqlite_db.db"
db_name = "sqlite:///" + str(db_path)

DB_ENGINE = create_engine(db_name, echo=False)


def delete_db_file(db_path: Path) -> None:
    if db_path.exists():
        print("det")
        db_path.unlink()


if __name__ == "__main__":
    delete_db_file(db_path)
