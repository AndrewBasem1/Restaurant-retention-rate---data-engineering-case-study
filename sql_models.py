from sqlmodel import SQLModel
from sqlmodel import Field
from uuid import UUID
from datetime import date
from db_engine import DB_ENGINE
from typing import Optional


class OrderRecord(SQLModel, table=True):
    order_uuid: UUID = Field(primary_key=True, unique=True)
    is_group_order: bool
    order_date: date = Field(index=False)
    user_uuid: UUID = Field(index=False)
    restaurant_uuid: UUID = Field(index=False)
    order_date_year_month: Optional[int] = Field(default=None, index=False)


def recreate_db_tables_from_scratch():
    """Drops all tables if they exist and recreates them from scratch according to our predefined sqlmodel Models."""
    try:
        SQLModel.metadata.drop_all(bind=DB_ENGINE)
    except:
        pass
    finally:
        SQLModel.metadata.create_all(bind=DB_ENGINE)


if __name__ == "__main__":
    recreate_db_tables_from_scratch()
