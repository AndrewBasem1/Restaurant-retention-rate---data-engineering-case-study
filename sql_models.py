from sqlmodel import SQLModel
from sqlmodel import Field
from uuid import UUID
from datetime import date
from db_engine import DB_ENGINE


class OrderRecord(SQLModel, table=True):
    order_uuid: UUID = Field(primary_key=True, unique=True)
    is_group_order: bool
    # defining the next rows as indexed before migration will slow down the insertion process a bit, but it's not an issue to tackle now
    order_date: date = Field(index=True)
    user_uuid: UUID = Field(index=True)
    restaurant_uuid: UUID = Field(index=True)


def recreate_db_tables_from_scratch():
    """Drops all tables if they exist and recreates them from scratch according to our predefined sqlmodel Models."""
    SQLModel.metadata.drop_all(bind=DB_ENGINE)
    SQLModel.metadata.create_all(bind=DB_ENGINE)


if __name__ == "__main__":
    recreate_db_tables_from_scratch()
