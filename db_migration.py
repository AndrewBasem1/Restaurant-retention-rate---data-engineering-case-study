from pathlib import Path
from typing import List

from sqlmodel import Session

from db_engine import DB_ENGINE
from sql_models import OrderRecord
from helper_funcs import create_record_iterator_from_csvs_in_zip_file
from sql_models import recreate_db_tables_from_scratch


def commit_order_records_to_db(order_records_list: List[OrderRecord]) -> None:
    """
    This function commits a group of sqlmodel objects to the database, used to insert rows in batch
    """
    print(f"\nadding {len(order_records_list)} to db")
    with Session(DB_ENGINE) as session:
        session.add_all(order_records_list)
        session.commit()


def migrate_records_to_db(zip_file_path: Path, batch_size: int = 10_000) -> None:
    """
    This function helps in migrating the exisiting records from all ".csv" files into the db with the needed indices and constraints, it also inserts values in batches to save memory
    """
    records_iterator = create_record_iterator_from_csvs_in_zip_file(
        zip_file_path=zip_file_path
    )
    records_parsed_count = 0
    records_inserted_count = 0
    records_in_batch_count = 0
    records_in_batch_list = []
    while True:
        try:
            current_record_dict = next(records_iterator)
            current_record_sqlmodel = OrderRecord.model_validate(current_record_dict)
            records_in_batch_list.append(current_record_sqlmodel)
            records_parsed_count += 1
            records_in_batch_count += 1
            print(f"records parsed: {records_parsed_count}", end="\r")
            if records_in_batch_count == batch_size:
                commit_order_records_to_db(records_in_batch_list)
                records_inserted_count += records_in_batch_count
                print(
                    f"added {records_in_batch_count} to db, total rows inserted are {records_inserted_count}"
                )
                records_in_batch_count = 0
                records_in_batch_list = []
        except StopIteration:  # no more rows to read
            # adding rows that was not a full "batch" at the end of the files
            if records_in_batch_count != 0:
                commit_order_records_to_db(records_in_batch_list)
                records_inserted_count += records_in_batch_count
                print(
                    f"added {records_in_batch_count} to db, total rows inserted are {records_inserted_count}"
                )
            print(f"total rows parsed: {records_parsed_count}")
            print(f"total rows inserted are: {records_inserted_count}")
            break
    return None


if __name__ == "__main__":
    recreate_db_tables_from_scratch()
    zip_file_path = Path(__file__).parent / "dummy_order_data_6_months.zip"
    migrate_records_to_db(zip_file_path=zip_file_path)
