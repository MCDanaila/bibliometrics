import os
import time
import sys
import glob

from file_status_handler import get_next_file
from file_status_handler import set_as_processed

from sources.scopus.scopus_ingestor import scopus_ingest_zip
from sources.scopus.scopus_ingestor import scopus_ingest_xml
from sources.scopus.scopus_ingestor import scopus_ingest_dir
from sources.wos.wos_ingestor       import wos_ingest_xml
from sources.wos.wos_ingestor       import wos_ingest_zip

zip_ingestor = None
xml_ingestor = None
dir_ingestor = None

def process_dir_zip_or_xml( path, bcp_dir):
  print( f"Processing path {path}")
  sys.stdout.flush()

  if path.endswith("/"):  # Remove trailing slash for directories
    path = path[:-1]

  if not os.path.exists(path) and not glob.glob(path):
    print(f"The path '{path}' does not exist.")
    return

  if os.path.isdir( path):
    if dir_ingestor:
      return dir_ingestor( path, bcp_dir)
    print( "Specified data provider does not have an associated directory processor")
    print( f"Path {path} rejected")
    return 

  # if not os.path.isfile(path): # Not too helpful with wildcards - maye limit it to wos?
    # print(f"The path '{path}' is not a file")
    # return

  dir, file = os.path.split( path)

  if path.endswith(".zip"):
    return zip_ingestor( file, dir, bcp_dir)
  elif path.endswith(".xml"):
    xml_ingestor( file, dir, bcp_dir)
  else:
    print( f"The path '{path}' does not correspond to a valid file type")

def process_files_from_source( provider, bcp_dir, input_paths):
  if zip_ingestor == None:
    print( "ZIP ingestor is None in process files")

  for path in input_paths.split( ':'):
    print( f"Processing from source - path {path}")
    sys.stdout.flush()
    process_dir_zip_or_xml( path, bcp_dir)
    sys.stdout.flush()
    print( f"Processed path {path}")

def process_files_from_db_def( provider, bcp_dir):
  # Note that this method can produce huge runs and python 
  # slows down after a while. So limit the run time. 

  max_process_time = 1800 # 0.5 hour
  
  start_time = time.process_time()

  more_data = True

  while more_data:
    # Don't run for too long

    if (time.process_time() - start_time) > max_process_time:
      exit( 1) ;

    next_file = get_next_file( provider)
    if next_file != None:
      if next_file[ 0] == "Done":
        more_data = False
      else:
        path_to_process = next_file[ 1]
        process_dir_zip_or_xml( path_to_process, bcp_dir)
        set_as_processed( provider, path_to_process)
    else:
      print( "Nothing")
      time.sleep( 10)

    sys.stdout.flush()

  exit( 0) ;

def main():
  args_len = len( sys.argv)

  if args_len < 3 :
    print( "Need at least provider and bcp directory")
    exit( -1)

  provider = sys.argv[ 1]
  bcp_dir  = sys.argv[ 2]

  print( f"Provider is {provider} and bcp directory is {bcp_dir}")
  sys.stdout.flush()
  if not os.path.isdir( bcp_dir):
    print( f"[{bcp_dir}] is not a directory for bcp files")
    exit( -1)

  global zip_ingestor
  global xml_ingestor
  global dir_ingestor

  if provider == "scopus":
    zip_ingestor = scopus_ingest_zip
    xml_ingestor = scopus_ingest_xml
    dir_ingestor = scopus_ingest_dir
  elif provider == "wos":
    zip_ingestor = wos_ingest_zip
    xml_ingestor = wos_ingest_xml
    dir_ingestor = None
  else:
    print( f"[{provider}] is not a recognised data provider")
    exit( -1)

  if zip_ingestor == None:
    print( "ZIP ingestor is None")

  if args_len > 3:
    process_files_from_source( provider, bcp_dir, sys.argv[ 3])
  else:
    process_files_from_db_def( provider, bcp_dir)
    exit( 0) ;

if __name__ == "__main__":
  main()
