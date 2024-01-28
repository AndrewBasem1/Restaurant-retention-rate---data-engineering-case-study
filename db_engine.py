from sqlmodel import create_engine

db_name = "sqlite:///sqlite_db.db"

DB_ENGINE = create_engine(db_name, echo=True)
