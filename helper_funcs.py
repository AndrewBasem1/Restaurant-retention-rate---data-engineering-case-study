import csv
import io
import zipfile
from pathlib import Path
from typing import Iterator, List


def _extract_csv_file_names(zipped_dir: zipfile.ZipFile):
    """
    This function extracts all filenames for ".csv" files in a zipped directory
    """
    zipped_files_names = [zipped_file.filename for zipped_file in zipped_dir.filelist]
    csv_files_names = []
    for zipped_file_name in zipped_files_names:
        if zipped_file_name.endswith(".csv") and not (
            zipped_file_name.startswith("__MACOSX")
        ):
            csv_files_names.append(zipped_file_name)
    return csv_files_names


def _strip_strings_and_replace_empty_strings_with_none(input_str: str) -> str:
    input_str = input_str.strip()
    return input_str if input_str != "" else None


def _rename_column_headers(original_col_headers: List[str]) -> List[str]:
    column_naming_mapping = {
        "orderdate": "order_date",
        "restuuid": "rest_uuid",
        "grouporder": "is_group_order",
    }
    new_col_headers = []
    for original_col_header in original_col_headers:
        new_col_header = column_naming_mapping.get(
            original_col_header, original_col_header
        )
        new_col_headers.append(new_col_header)
    return new_col_headers


def create_record_iterator_from_csvs_in_zip_file(
    zip_file_path: Path,
) -> Iterator[dict[str, str]]:
    """
    This function will be used to iterate over all records in all ".csv" files within a ".zip" file returning one row each time the `next()` method is called on its returned object.

    ## Parameters:
    - zip_file_path: `pathlib.Path`

    ## Returns:
    - Iterator[dict[str,str]]
        an iterator that returns a dict each time the `next()` function is called on it, giving each time the next row from the same file or the first row from the next file
    """
    with zipfile.ZipFile(zip_file_path) as zip_dir:
        for csv_file_name in _extract_csv_file_names(zip_dir):
            with zip_dir.open(csv_file_name) as csv_file:
                decoded_csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
                csv_reader = csv.reader(decoded_csv_file)
                original_csv_headers = next(csv_reader)
                csv_headers = _rename_column_headers(original_csv_headers)
                for line in csv_reader:
                    line = map(_strip_strings_and_replace_empty_strings_with_none, line)
                    line_record_dict = dict(zip(csv_headers, line))
                    yield line_record_dict


if __name__ == "__main__":
    zip_file_path = Path(__file__).parent / "dummy_order_data_6_months.zip"
    csv_iterator = create_record_iterator_from_csvs_in_zip_file(zip_file_path)
    for i in range(4):
        print(next(csv_iterator))
