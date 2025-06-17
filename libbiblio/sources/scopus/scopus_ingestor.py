import shutil
import datetime
import time
import zipfile as zf        

from glob import glob

import os

from .scopus_parser         import scopus_parser
from .scopus_process_status import get_process_status
from .scopus_process_status import set_process_status

# Pretty sure that some of these can be made wos/scopus common with some tweeks

def scopus_set_ready_files( bcp_path):
  with open( bcp_path + ".publication.ready"  , "w"), \
       open( bcp_path + ".author.ready"       , "w"), \
       open( bcp_path + ".authorship.ready"   , "w"), \
       open( bcp_path + ".source.ready"       , "w"), \
       open( bcp_path + ".citation.ready"     , "w"), \
       open( bcp_path + ".affiliation.ready"  , "w"), \
       open( bcp_path + ".descriptor.ready"   , "w"), \
       open( bcp_path + ".authorkeyword.ready", "w"):
    pass

def scopus_ingest_zip( zip_name : str,
                       dir_path : str,
                       bcp_dir  : str):

  handles = {}

  bcp_path = (bcp_dir + "/" + zip_name).replace( ".zip", "") 

  with zf.ZipFile(f"{dir_path}/{zip_name}", "r") as archive, \
    open( bcp_path + ".publication.bcp"  , "w") as handles[ "publication"  ], \
    open( bcp_path + ".author.bcp"       , "w") as handles[ "author"       ], \
    open( bcp_path + ".authorship.bcp"   , "w") as handles[ "authorship"   ], \
    open( bcp_path + ".source.bcp"       , "w") as handles[ "source"       ], \
    open( bcp_path + ".citation.bcp"     , "w") as handles[ "citation"     ], \
    open( bcp_path + ".affiliation.bcp"  , "w") as handles[ "affiliation"  ], \
    open( bcp_path + ".descriptor.bcp"   , "w") as handles[ "descriptor"   ], \
    open( bcp_path + ".authorkeyword.bcp", "w") as handles[ "authorkeyword"]:
    for xml_name in archive.namelist():
      if xml_name.endswith(".xml"):
        with archive.open(xml_name, mode="r") as xml_file:
          xml_str = xml_file.read().decode()
          scopus_parser( xml_str, xml_name, zip_name, handles)

  scopus_set_ready_files( bcp_path)

  return 0

def scopus_ingest_xml( xml_name : str,
                       dir_path : str,
                       bcp_dir  : str):
  handles = {}

  bcp_path = (bcp_dir + "/" + xml_name).replace( ".xml", "") 

  # process_state = get_process_status( zip_name)

  # if( process_state != None ):
    # print( f"File {zip_name} is in process state {process_state} - will not be reprocessed")
    # return -1

  with open( dir_path + "/" + xml_name      , "r") as xml_file                 , \
       open( bcp_path + ".publication.bcp"  , "w") as handles[ "publication"  ], \
       open( bcp_path + ".author.bcp"       , "w") as handles[ "author"       ], \
       open( bcp_path + ".authorship.bcp"   , "w") as handles[ "authorship"   ], \
       open( bcp_path + ".source.bcp"       , "w") as handles[ "source"       ], \
       open( bcp_path + ".citation.bcp"     , "w") as handles[ "citation"     ], \
       open( bcp_path + ".affiliation.bcp"  , "w") as handles[ "affiliation"  ], \
       open( bcp_path + ".descriptor.bcp"   , "w") as handles[ "descriptor"   ], \
       open( bcp_path + ".authorkeyword.bcp", "w") as handles[ "authorkeyword"]:
    scopus_parser( xml_file.read(), xml_name, "replace this proper zip_name", handles)

  # set_process_status( zip_name, "PyProcessed", False) # False => update record, don't insert new one

  return 0

def scopus_ingest_dir( dir     : str,
                       bcp_dir : str):
  handles = {}

  origin_zip_name = os.path.basename( dir)

  bcp_path = bcp_dir + "/" + origin_zip_name

  # process_state = get_process_status( origin_zip_name)

  # if( process_state != None ):
    # print( f"File {origin_zip_name} is in process state {process_state} - will not be reprocessed")
    # return -1

  with open( bcp_path + ".publication.bcp"  , "w") as handles[ "publication"  ], \
       open( bcp_path + ".author.bcp"       , "w") as handles[ "author"       ], \
       open( bcp_path + ".authorship.bcp"   , "w") as handles[ "authorship"   ], \
       open( bcp_path + ".source.bcp"       , "w") as handles[ "source"       ], \
       open( bcp_path + ".citation.bcp"     , "w") as handles[ "citation"     ], \
       open( bcp_path + ".affiliation.bcp"  , "w") as handles[ "affiliation"  ], \
       open( bcp_path + ".descriptor.bcp"   , "w") as handles[ "descriptor"   ], \
       open( bcp_path + ".authorkeyword.bcp", "w") as handles[ "authorkeyword"]:
    for xml_path in glob( dir + "/*xml"):
      with open( xml_path, "r") as xml_file:
        scopus_parser( xml_file.read(), os.path.basename( xml_path), origin_zip_name, handles)

  # Create ready files

  scopus_set_ready_files( bcp_path)

  # Maybe more defensive here

  shutil.rmtree( dir)

  # set_process_status( origin_zip_name, "PyProcessed", False) # False => update record, don't insert new one

  return 0

