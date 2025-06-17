import psycopg2
from psycopg2 import sql
import os

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

def get_process_status( zip_file:str):
  global connection, cursor

  if( connection == None ):
    try:
      set_connection()
    except (Exception, psycopg2.Error) as error:
      return "Unknown state - connection refused"

  cursor.execute( sql.SQL(f"SELECT status FROM \"ScopusTestZipStatus\" WHERE zip_file_name = '{zip_file}';"))

  result = cursor.fetchone()

  if( result != None ):
    return result[ 0]

  set_process_status( zip_file, "PyProcessing", True)

  return None

def set_process_status( zip_file:str ,
                        status  :str ,
                        insert  :bool):
  global connection, cursor

  if( connection == None ):
    try:
      set_connection()
    except (Exception, psycopg2.Error) as error:
      print( "Unknown state - connection refused")
      return

  # if( insert ):
    # query = sql.SQL( "INSERT INTO \"ScopusTestZipStatus\" VALUES( %s, %s)")
  # else:
    # query = sql.SQL( "UPDATE \"ScopusTestZipStatus\" SET status = %s WHERE zip_file_name = %s")

  if( insert ):
    query = sql.SQL( f"INSERT INTO \"ScopusTestZipStatus\" VALUES( '{zip_file}', '{status}');")
  else:
    query = sql.SQL( f"UPDATE \"ScopusTestZipStatus\" SET status = '{status}' WHERE zip_file_name = '{zip_file}';")

  cursor.execute( query, (zip_file, status))

  connection.commit()
