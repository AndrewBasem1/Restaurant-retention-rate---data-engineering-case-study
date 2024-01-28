from sqlmodel import SQLModel
from sqlmodel import Field
from uuid import UUID
from datetime import date
from db_engine import DB_ENGINE


class OrderRecord(SQLModel, table=True):
    order_uuid: UUID = Field(primary_key=True, unique=True)
    order_date: date = Field(index=True)
    user_uuid: UUID = Field(index=True)
    restaurant_uuid: UUID = Field(index=True)
    is_group_order: bool


def recreate_db_tables_from_scratch():
    """Drops all tables if they exist and recreates them from scratch according to our predefined sqlmodel Models."""
    SQLModel.metadata.drop_all(bind=DB_ENGINE)
    SQLModel.metadata.create_all(bind=DB_ENGINE)


if __name__ == "__main__":
    recreate_db_tables_from_scratch()
