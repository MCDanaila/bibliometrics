from dotenv import load_dotenv
from db.db_config import PSQL_DB
import re, os
from typing import List, Optional

load_dotenv()
""" 
DB_CONN = PSQL_DB(host=os.environ.get("DEV_HOST"), 
				  port=5432, 
				  initial_db=os.environ.get("DEV_DB"), 
				  username=os.environ.get("DEV_USERNAME"), 
				  password=os.environ.get("DEV_PASSWORD")) """

DB_CONN = PSQL_DB(host=os.environ.get("PROD_HOST"), 
				  port=5432, 
				  initial_db=os.environ.get("PROD_DB"), 
				  username=os.environ.get("PROD_USERNAME"), 
				  password=os.environ.get("PROD_PASSWORD"))

def create_table(cursor, table_name: str, columns: List[str], typed_columns: Optional[List[str]] = None) -> None:
    db_columns = typed_columns if typed_columns else [f"{col} VARCHAR NULL" for col in columns]
    statement = f"""DROP TABLE IF EXISTS "{table_name}"; 
    CREATE TABLE "{table_name}" (id SERIAL, {", ".join(db_columns)});
    """
    try:
        cursor.execute(statement)
        print(f'== INFO - Executed table creation for {table_name}')
    except Exception as error:
        print(f'ERROR - create_table({table_name=}, {db_columns=}) - {error}')

def dump_table(table_name: str, bcp_file: str, columns: List[str], typed_columns: Optional[List[str]] = None, drop_table: bool = True, sep: str = '\t') -> int:
    try:
        with DB_CONN.cursor() as cursor:
            if drop_table:
                create_table(cursor, table_name, columns, typed_columns)
            with open(bcp_file, encoding="utf-8", errors='replace') as f:
                cursor.copy_from(file=f, sep=sep, table=table_name, null='', columns=columns)
        return 0
    except Exception as error:
        """ res = re.search(r"line \d+", error.diag.context)
		line = res.group(0).split(' ')[1]
		#print(f'{line=}') """
        res = re.search(r"line \d+", str(error))
        if res:
            line = int(res.group(0).split(' ')[1])
            print(f'ERROR - Failed to copy from line {line}: {error}')
            return line
        print(f'ERROR - Failed to dump table {table_name}: {error}')
        return -1

""" def dumpTable(table_name: str = None, bcp_file: str = None, columns: list = None, typed_columns: list = None):
	with DB_CONN.cursor() as cursor:
		create_table(cursor, table_name, columns, typed_columns)
		with open(bcp_file, encoding="utf-8", errors='replace') as f:
			cursor.copy_from(file=f, table=table_name, null='', columns=columns) """

def change_column_type_to_int(table_name: str, col_name: str):  
    try:
        with DB_CONN.cursor() as cursor:
            query = f"""ALTER TABLE "{table_name}" ALTER COLUMN {col_name} TYPE INT USING (cast ( coalesce( nullif( trim({col_name}), '' ), '0' ) as integer ))"""
            cursor.execute(query)
    except Exception as error:
        print(f'ERROR - Failed to convert {col_name=} from {table_name=}: {error}')