import psycopg2
from psycopg2 import sql
import os
import time


connection = None
cursor     = None

def set_connection():
  global connection, cursor
  db_params = {
    'host'     : os.environ[ "POSTGRES_SERVER"],
    'database' : os.environ[ "POSTGRES_DB"    ],
    'user'     : os.environ[ "POSTGRES_USER"  ],
    'password' : os.environ[ "POSTGRES_PASSWD"]
  }

  connection = psycopg2.connect(**db_params)

  cursor = connection.cursor()

def get_next_file( provider:str):
  global connection, cursor

  if( connection == None ):
    try:
      set_connection()
    except (Exception, psycopg2.Error) as error:
      return "Unknown state - connection refused"

  # The order by is to get the big jobs doen first. 1900 is pretty big too, but...

  cursor.execute( sql.SQL(f"BEGIN"))
  cursor.execute( sql.SQL(f"SELECT file_name, file_path FROM \"BibliometricsFileStatus\" WHERE provider = '{provider}' AND status = 'unprocessed' ORDER BY file_name DESC FOR UPDATE;"))

  result = cursor.fetchone()

  if( result != None ):
    file_name = result[ 0]
    file_path = result[ 1]

    cursor.execute( sql.SQL(f"UPDATE \"BibliometricsFileStatus\" SET status = 'processing', started = NOW() WHERE file_name = '{file_name}' and file_path = '{file_path}'"))
  else:
    cursor.execute( sql.SQL(f"SELECT 'Done' FROM \"BibliometricsFileStatus\" WHERE provider = '{provider}' AND file_name = 'all_files_done';"))
    result = cursor.fetchone()

  cursor.execute( sql.SQL(f"COMMIT"))
  return result

def set_as_processed( provider:str, file_path:str):
  global connection, cursor

  if( connection == None ):
    try:
      set_connection()
    except (Exception, psycopg2.Error) as error:
      return "Unknown state - connection refused"

  cursor.execute( sql.SQL(f"BEGIN"))
  cursor.execute( sql.SQL(f"UPDATE \"BibliometricsFileStatus\" SET status = 'processed', finished = NOW() WHERE file_path = '{file_path}'"))
  cursor.execute( sql.SQL(f"COMMIT"))
