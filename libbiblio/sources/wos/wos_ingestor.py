import os
import sys
import shutil
import subprocess
import gzip

from zipfile import ZipFile
from glob    import glob

from libbiblio.sources.wos.wos_parser import wos_parser

product_type_map = None

def get_product_type_map():
  global product_type_map

  product_type_map = {}

  # This assumes that the product is in the same directory as the python script and is called
  # wos_pub_type_map.tsv

  map_file = os.path.dirname( os.path.abspath(__file__)) + "/wos_pub_type_map.tsv"

  with open( map_file) as pt_map:
    for map_line in pt_map:
      map_line = map_line.strip().replace('\ufeff', '') 
      # The last emelent in the tab seperated array is the value
      # The first are the key which shouldbe joined by tab
      elems = map_line.split( '\t')
      val    = elems.pop()
      # Now sort the rest of the elements, rejoin the elements
      # and populate the map
      elems.sort()
      product_type_map[ "\t".join( elems)] = val

  sys.stdout.flush()

# Pretty sure that some of these can be made wos/wos common with some tweeks

def set_ready_files( bcp_path):
  with open( bcp_path + ".publication.ready"     , "w") , \
       open( bcp_path + ".author.ready"          , "w") , \
       open( bcp_path + ".authorship.ready"      , "w") , \
       open( bcp_path + ".source.ready"          , "w") , \
       open( bcp_path + ".citation.ready"        , "w") , \
       open( bcp_path + ".affiliation.ready"     , "w") , \
       open( bcp_path + ".authorkeyword.ready"   , "w") , \
       open( bcp_path + ".grant.ready"           , "w") , \
       open( bcp_path + ".publicationgrant.ready", "w") , \
       open( bcp_path + ".puborg.ready"          , "w") , \
       open( bcp_path + ".pubcountry.ready"      , "w") , \
       open( bcp_path + ".pubsubject.ready"      , "w") :
    pass

def wos_ingest_xml( xml_path: str,
                    bcp_dir : str):

  print( f"In python ingest with {xml_path}")

  [dir_path, xml_name] = os.path.split( xml_path)
  handles = {}

  bcp_path = (bcp_dir + "/" + xml_name).replace( ".xml", "") 

  with open( bcp_path + ".publication.bcp"     , "w") as handles[ "publication"     ], \
       open( bcp_path + ".author.bcp"          , "w") as handles[ "author"          ], \
       open( bcp_path + ".authorship.bcp"      , "w") as handles[ "authorship"      ], \
       open( bcp_path + ".source.bcp"          , "w") as handles[ "source"          ], \
       open( bcp_path + ".citation.bcp"        , "w") as handles[ "citation"        ], \
       open( bcp_path + ".affiliation.bcp"     , "w") as handles[ "affiliation"     ], \
       open( bcp_path + ".authorkeyword.bcp"   , "w") as handles[ "authorkeyword"   ], \
       open( bcp_path + ".grant.bcp"           , "w") as handles[ "grant"           ], \
       open( bcp_path + ".publicationgrant.bcp", "w") as handles[ "publicationgrant"], \
       open( bcp_path + ".puborg.bcp"          , "w") as handles[ "puborg"          ], \
       open( bcp_path + ".pubcountry.bcp"      , "w") as handles[ "pubcountry"      ], \
       open( bcp_path + ".pubsubject.bcp"      , "w") as handles[ "pubsubject"      ]:
    wos_parser( xml_path, handles)

def wos_ingest_zip( zip_name : str,
                    zip_dir  : str,
                    bcp_dir  : str):  # wos zips contain several gz files

  global product_type_map

  handles = {}

  zip_base = zip_name.replace( ".zip", "").replace( "*", "WILD")
  bcp_path = f"{bcp_dir}/{zip_base}"
  xml_dir  = bcp_dir.replace( "bcp", "xml") + "/" + zip_base

  # Need to use glob because the file might be wildcarded

  for content_file in glob( f"{zip_dir}/{zip_name}"):
    with ZipFile( content_file, 'r') as zip_ref:
      # Extract all the contents into the specified directory
      for zip_content in zip_ref.namelist():
        if zip_content.endswith( ".gz"):
          zip_ref.extract( zip_content, xml_dir)
          # Need better error handling subprocess.call( f"gunzip {xml_dir}/{zip_content}") -- web suggests that shell = True is unsafe, shell = True)
          gzip_file = f"{xml_dir}/{zip_content}"
          try:
            subprocess.run(["gunzip", gzip_file], check=True)
          except subprocess.CalledProcessError as e:
            print(f"gunzip failed on {gzip_file} with exit code: {e.returncode}")
          except FileNotFoundError:
            print("gunzip command not found. Please install it and try again.")
          except Exception as e:
            print(f"An error occurred gunzipping {gzip_file} : {e}")

  already_processed_pubs = set()   # To handle ESCI

  # Need to get a product type map

  if not product_type_map:
    get_product_type_map()

  # Now need to go to the directory we just created

  with open( bcp_path + ".publication.bcp"     , "w") as handles[ "publication"     ], \
       open( bcp_path + ".author.bcp"          , "w") as handles[ "author"          ], \
       open( bcp_path + ".authorship.bcp"      , "w") as handles[ "authorship"      ], \
       open( bcp_path + ".source.bcp"          , "w") as handles[ "source"          ], \
       open( bcp_path + ".citation.bcp"        , "w") as handles[ "citation"        ], \
       open( bcp_path + ".affiliation.bcp"     , "w") as handles[ "affiliation"     ], \
       open( bcp_path + ".authorkeyword.bcp"   , "w") as handles[ "authorkeyword"   ], \
       open( bcp_path + ".grant.bcp"           , "w") as handles[ "grant"           ], \
       open( bcp_path + ".publicationgrant.bcp", "w") as handles[ "publicationgrant"], \
       open( bcp_path + ".puborg.bcp"          , "w") as handles[ "puborg"          ], \
       open( bcp_path + ".pubcountry.bcp"      , "w") as handles[ "pubcountry"      ], \
       open( bcp_path + ".pubsubject.bcp"      , "w") as handles[ "pubsubject"      ]:
    for xml_path in glob( f"{xml_dir}/*xml"):
      wos_parser( xml_path, already_processed_pubs, product_type_map, handles)
      os.remove( xml_path)
    os.rmdir(xml_dir)

  set_ready_files( bcp_path)
  
  return 0
