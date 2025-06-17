from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import os
import sys
import re
import xmltodict
from devtools import debug
from lxml import etree
from hashlib import md5

TAG = "{http://clarivate.com/schema/wok5.30/public/FullRecord}REC"

# bigint_limit = 2**64

def cnv_str_md5_int( in_str):
  global bigint_limit

  if not in_str:
    in_str = ""

  # The int call to be able to ensure fit in bigint postgres 

  return str( int( md5( in_str.encode()).hexdigest()[:15], 16))
  # return str( int( md5( in_str.encode()).hexdigest()[:16], 16) % ( bigint_limit))

#Global tags

# Publication

pub_id_hash_idx       =  0    # having this first helps with updating process
pub_id_idx            =  1
pub_doi_idx           =  2
pub_pmid_idx          =  3
pub_type_idx          =  4
pub_lang_idx          =  5
pub_title_idx         =  6
pub_first_page_idx    =  7
pub_last_page_idx     =  8
pub_pub_date_idx      =  9
pub_pub_year_idx      = 10
pub_pub_month_idx     = 11
pub_volume_idx        = 12
pub_copyright_idx     = 13
pub_wuid_idx          = 14
pub_headings_idx      = 15
pub_subheadings_idx   = 16
pub_subjects_idx      = 17
pub_abstract_idx      = 18
pub_fund_text_idx     = 19
pub_grant_idx         = 20
pub_oa_state_idx      = 21
pub_keywords_idx      = 22
pub_authors_idx       = 23
pub_ref_count_idx     = 24
pub_countries_idx     = 25
pub_unified_names_idx = 26
pub_is_retracted_idx  = 27
pub_mapped_type_idx   = 28
pub_idx_ct            = 29

# Source

src_name_idx          = 0
src_issn_idx          = 1
src_abbrev_idx        = 2
src_publisher_idx     = 3
src_source_abbrev_idx = 4
src_abbrev_iso_idx    = 5
src_abbrev_11_idx     = 6
src_abbrev_29_idx     = 7
src_idx_ct            = 8

# Authors 

aut_wos_standard_idx = 0
aut_name_idx         = 1
aut_given_name_idx   = 2
aut_surname_idx      = 3
aut_suffix_idx       = 4
aut_e_address_idx    = 5
aut_display_name_idx = 6
aut_idx_ct           = 7

empty_aut_str  =  "\t".join( [""] * (aut_idx_ct + 2)) # extra 2 for orcid_id and r_id
empty_aut_hash =  cnv_str_md5_int( empty_aut_str)
empty_aut_str  += "\t" + empty_aut_hash

# Affiliation

aff_org_idx         = 0
aff_org_uni_idx     = 1
aff_sub_orgs_idx    = 2
aff_address_idx     = 3
aff_country_idx     = 4
aff_state_idx       = 5
aff_city_idx        = 6
aff_street_idx      = 7
aff_postal_code_idx = 8
aff_ror_id_idx      = 9
aff_org_id_idx      = 10
aff_idx_ct          = 11


empty_aff_str  = "\t".join( [""] * aff_idx_ct)
empty_aff_str += "\t" + cnv_str_md5_int( empty_aff_str)

# Grants

grant_agency_idx = 0
grant_id_idx     = 1
grant_idx_ct     = 2

empty_grant_str  = "\t".join( [""] * grant_idx_ct)
empty_grant_hash = cnv_str_md5_int( empty_grant_str)
empty_grant_str  += "\t" + empty_grant_hash

oa_hierarchy = {
  "closed" : 0,
  "bronze" : 1,
  "green"  : 2,
  "hybrid" : 3,
  "gold"   : 4
}

pub_aut_hashes    = set()
pub_countries     = set()
pub_unified_names = set()

#>>>> cnv

def cnv( in_string: str, replace = ""):
  return in_string if in_string else replace

#<<<< cnv

#<<<<

def remove_para_xml( text):
  text = re.sub(  r'<p.*?>', '', text)
  return re.sub( r'<\\p>', '', text)

def list_to_string( details):
  # Alchemy takes a list (or makes one) and converts into a string like 
  # {"Diffuse uptake",FDG-PET,"Focal uptake","Thyroid cancer"}

  if not details:
    return "{}"

  if isinstance( details, str):
    details = [ details]

  # The None test looks paranoid, but it's not - I've seen it happen AMB 05-07-24
  # Postgresql HATES " in array elements
  # Quote everything - items with no spaces can have commas, which confuses array AMB 12-07-24
  # Backslashes confuse things too AMB 12-07-24

  # details = ",".join( [ '"' + d  +'"' if " " in d else d for d in [x.replace( '"', '\'') for x in details if x is not None]])
  details = ",".join( [ '"' + d  +'"' for d in [x.replace( '"', '\'').replace( '\\', '') for x in details if x is not None]])

  return "{" + details + "}"

def list_or_string( item, joiner = " "):
  if not item:
    return ""

  return joiner.join( [ remove_para_xml( i) for i in item if i is not None]) if isinstance(item, list) else \
                remove_para_xml( item)

#>>>> get

def get(data, keys, fallback = None):
  try:
    for key in keys:
      data = data[key]
  except ( KeyError, TypeError):
    return fallback

  return data

#<<<< get

def process_open_access( dynamic_data):
  oa_holder = get( dynamic_data, [ "ic_related", "oases"])
  if not oa_holder:
    return "closed"

  if oa_holder[ "@is_OA"] != "Yes" :
    return oa_holder[ "@is_OA"]
  
  oa_dets = oa_holder[ "oas"]

  if isinstance( oa_dets, dict):
    # Simplest case
    type = oa_dets[ "@type"]
    if "green" in type:
      type = "green"
    return type

  oa_state = "closed"
  hier     = 0

  for oa_det in oa_dets:
    type = oa_det[ "@type"]
    if "green" in type:
      type = "green"
    if oa_hierarchy[ type] > hier:
      os_state = type
      hier     = oa_hierarchy[ type]

  return os_state

def process_ids( dynamic_data, pub, src):
  ids = get( dynamic_data, [ "cluster_related", "identifiers", "identifier"])
  if not ids:
    return # Should this be logged? AMB 22.12.23 Nope. 20.08.24 AMB

  if isinstance( ids, dict):
    ids = [ids]

  regular_doi_found = False

  for id in ids:
    this_type = id.get( "@type", "")
    if this_type == "doi":
      pub[ pub_doi_idx] = id.get( "@value", "")
      regular_doi_found = True
    elif this_type == "xref_doi":
      if not regular_doi_found:
        pub[ pub_doi_idx] = id.get( "@value", "")
    elif this_type == "issn":
      src[ src_issn_idx] = id.get( "@value", "")
    elif this_type == "pmid":
      pub[ pub_pmid_idx] = id.get( "@value", "")

def get_pub_lang( language):
  # Maybe make this nicer

  if not language:
    return ""

  if language.get( "@count", "") == "1":
    return list_to_string( get(language, ["language", "#text"]))

  return list_to_string( list( {get(lang, ["#text"]) for lang in language.get( "language")})) # Prevent duplicates

def get_title( static_data):
  source_title = ""
  for title in get( static_data, ["summary", "titles", "title"]):
    if title["@type"] == "source":
      source_title = title["#text"]
    if title["@type"] == "item":
      return title["#text"]

  # Fallback to source title or an empty string

  return source_title

def get_author_keywords( pub_hash, fr_metadata, fh):
  # Note that WoS documentation doesn't reference keywords, so this is guessing

  kwds = get( fr_metadata, ["keywords", "keyword"])
  if not kwds: return ""  # Empty  is for keywords column test

  keywords = []

  if isinstance( kwds, str):
    kwds = [kwds]

  for kwd in kwds:
    # Sometimes WoS has a keyword of a single backslash, which confuses
    # postgresql COPY, so don't store these AMB 24.01.24
    if kwd != "\\" :
      keywords.append( kwd)
      print( "\t".join( [pub_hash, kwd]), file=fh)

  return list_to_string( keywords) # keywords test

def get_wuid( summary):
  edition = get( summary, ["EWUID", "edition"])
  if not edition:
    return ""

  ret = []
  if isinstance(edition, dict):
    edition = [edition]
  for wuid in edition:
    ret.append(get(wuid, ["@value"]))
  return list_to_string( ret)

def get_subjects( catinfo):
  subjects = get( catinfo, [ "subjects", "subject"])

  if subjects:
    if isinstance( subjects, dict):
      return subjects.get( "#text", "")
  
    return list( {s.get( "#text", "") for s in subjects}) # Avoid duplicates

  return None

def get_affiliation_details( address_spec):
  aff = [""] * aff_idx_ct

  # Handle the organization details

  orgs         = address_spec.get( "organizations")
  unified_orgs = None
  main_org     = ""

  if orgs:
    org = orgs.get( "organization")

    if isinstance( org, list):  # Most common
      for org_dets in org:
        if isinstance( org_dets, dict):
          if org_dets.get( "@pref", "") == "Y":
            if unified_orgs:
              unified_orgs.append( org_dets[ "#text"])
            else:
              unified_orgs = [ org_dets[ "#text"]]
          else:
            if main_org == "" :
              main_org = org_dets[ "#name"]
          aff[ aff_ror_id_idx ] = org_dets.get("@ROR_ID", "")
          aff[ aff_org_id_idx ] = org_dets.get("@org_id", "")
        else:
          if main_org == "" :
            main_org = org_dets
    else:
      if isinstance( org, str):
        main_org = org
      else:            # A dict, which is REALLY unlikely
        main_org = org[ "#name"]

  if not main_org and unified_orgs:
    main_org = unified_orgs[ 0]   # A bit dodgy I know. AMB 04.01.24
          
  sub_orgs = address_spec.get( "suborganizations")
  if sub_orgs:
    sub_org = sub_orgs.get( "suborganization")
    if isinstance( sub_org, list):
      aff[ aff_sub_orgs_idx] = list_to_string( [item for item in sub_org])
    else:
      aff[ aff_sub_orgs_idx] = list_to_string( sub_org)

  aff[ aff_org_idx    ] = main_org
  aff[ aff_org_uni_idx] = list_to_string( unified_orgs)

  if unified_orgs:
    pub_unified_names.update( unified_orgs)

  aff[ aff_address_idx    ] = address_spec.get( "full_address")
  aff[ aff_state_idx      ] = address_spec.get( "state"       )
  aff[ aff_city_idx       ] = address_spec.get( "city"        )
  aff[ aff_street_idx     ] = address_spec.get( "street"      )

  country = address_spec.get( "country")
  if country:
    aff[ aff_country_idx] = country
    pub_countries.add( country.upper()) # Should make searching quicker

  zip = address_spec.get( "zip")
  if zip:
    # Only until a reply is given from WoS about relevance of location,
    # use the first found if more than one AMB 04.01.24
    if isinstance( zip, list):
      zip = zip[ 0]
    aff[ aff_postal_code_idx] = zip[ "#text"]

  # Sometimes wos specifies a dictionary entry but doesn't give details

  aff_str = "\t".join( [ i if i else "" for i in aff])
  aff_str += "\t" + cnv_str_md5_int( aff_str)

  return [ address_spec[ "@addr_no"], aff_str]

def get_source_details( summary, handles: Dict): # summary guaranteed non null.
  src = [""] * src_idx_ct

  name = get( summary, [ "publishers", "publisher", "names", "name"])

  # This may coma back to bite - I have a feeling name may be a list sometimes

  if name:
    src[ src_abbrev_idx] = name.get( "display_name", "")

    this_name = name.get( "unified_name", "")

    if not this_name or this_name == "" :    # not this_name should do the same thing, no?
      this_name = name.get( "full_name", "")
      if not this_name or this_name == "" :
        this_name = src[ src_abbrev_idx]
        if not this_name:
          this_name = ""

    src[ src_publisher_idx] = this_name

  titles = get( summary, ["titles", "title"])

  # The "list of titles" is actual a list of identifiers, not actual titles
  if titles:
    for title in titles:
      # No match in python 9.8
      title_type = title.get( "@type", "")

      if title_type == "source":
       src[ src_name_idx] = title.get( "#text", "")
      elif title_type == "issn":
       src[ src_issn_idx] = title.get( "#text", "")
      elif title_type == "source_abbrev":
       src[ src_source_abbrev_idx] = title.get( "#text", "")
      elif title_type == "abbrev_iso":
       src[ src_abbrev_iso_idx] = title.get( "#text", "")
      elif title_type == "abbrev_11":
       src[ src_abbrev_11_idx] = title.get( "#text", "")
      elif title_type == "abbrev_29":
       src[ src_abbrev_29_idx] = title.get( "#text", "")

  return src

def get_author_tsv( aut_rec, contribs):
  aut = [""] * aut_idx_ct   # Why? All values expilitly set AMB 16/6/24

  aut[ aut_wos_standard_idx] = aut_rec.get( "wos_standard")
  aut[ aut_name_idx        ] = aut_rec.get( "full_name"   )
  aut[ aut_given_name_idx  ] = aut_rec.get( "first_name"  )
  aut[ aut_surname_idx     ] = aut_rec.get( "last_name"   )
  aut[ aut_suffix_idx      ] = aut_rec.get( "suffix"      )
  aut[ aut_e_address_idx   ] = aut_rec.get( "email_addr"  )
  aut[ aut_display_name_idx] = aut_rec.get( "display_name")

  # For older pubs, there is either no display name or wos_standard. 
  # Default the one with the other

  if not aut[ aut_wos_standard_idx]:
    aut[ aut_wos_standard_idx] = aut[ aut_display_name_idx]
  elif not aut[ aut_display_name_idx]:
    aut[ aut_display_name_idx] = aut[ aut_wos_standard_idx]

  if contribs:
    contribs = contribs.get( aut[ aut_display_name_idx], [""] * 2)
  else:
    contribs = [""] * 2

  aut += contribs   # index 0 orcid, 1 r_id

  # Need to be defensive here - WoS sometimes specifies empty details

  aut_str = "\t".join( [ i if i else "" for i in aut])

  aut_hash = cnv_str_md5_int( aut_str)

  return [ aut_str + "\t" + aut_hash, aut_hash] # Need aut_hash seperate for authorship

def merge_authorship_details( pub_hash, names, contribs, aff_dets, handles):
  namelist = names[ "name"]
  if isinstance( namelist, dict):
    namelist = [namelist]
  for name in namelist:
    role = name[ "@role"]
    # There are a few roles which don't make too much sense. Anon can be seen as an author. 
    # Not sure about corp though. For the meantime I'm gonna put as author, but
    # this needs discussion.
    # Waiting for a reply from WoS wrt "book"
    # AMB 07.01.24

    if( role == "anon" or role == "corp" or role == "book"):
      role = "author"

    if( role == "author" or role == "book_editor" ):
      [ aut_tsv, aut_hash] = get_author_tsv( name, contribs)
      print( aut_tsv, file=handles[ "author"])
      pub_aut_hashes.add( aut_hash)
        
      header = [ pub_hash, name[ "@seq_no"], role]
      if isinstance( aff_dets, dict):
        addr_no = name.get( "addr_no")
        if not addr_no:
          addr_no = "1"
        aff_dets = aff_dets.get( addr_no)
        if not aff_dets:
          aff_dets = empty_aff_str

      print( "\t".join( header) + "\t" + aut_hash + "\t" + aff_dets, file=handles[ "authorship"])

  # When doing affiliation joins, must allow for no addresses in dict

def get_authorship_details( pub_hash, fr_metadata, summary, contribs, handles):

  contrib_dict = {}

  if contribs:
    if contribs[ "@count"] == "1" :
      contribs = [ contribs[ 'contributor']]
    else:
      contribs = contribs[ 'contributor']
    
    for contrib in contribs:
      dets = contrib[ 'name']
      contrib_dict[ dets[ 'display_name']] = [ dets.get( '@orcid_id'),
                                                 dets.get( '@r_id'    )]

  # Get the address details for the publication. If there are any

  addresses = fr_metadata.get("addresses")

  if( addresses and addresses[ "@count"] != "0"):
    # We have some addresses

    address_name = addresses.get( "address_name")

    # Need to know if the address contains names - if so then we don't
    # need the dictionary approach to addresses

    if isinstance( address_name, dict):
      address_name = [ address_name]

    aff_dict_needed = False
    aff_dict        = {}    # Just in case

    for address in address_name:
      [ addr_id, aff_tsv] = get_affiliation_details( address.get( "address_spec"))
      print( aff_tsv, file=handles[ "affiliation"])

      names = address.get( "names")
      if names:
        merge_authorship_details( pub_hash, names, contrib_dict, aff_tsv, handles)
      else:
        # There may be a reference in the summary section
        aff_dict[ addr_id] = aff_tsv

      # Have any locations but no authors been found - if not need to get them from summary

    if aff_dict:
      merge_authorship_details( pub_hash, summary.get( "names"), contrib_dict, aff_dict, handles)

  else:
    # No locations found
    merge_authorship_details( pub_hash, summary.get( "names"), contrib_dict, empty_aff_str, handles)

def l_d_as_list( list_or_dict): # Maybe have utility functions like this as a module AMB 09.01.24
  if not list_or_dict or isinstance( list_or_dict, list):
    return list_or_dict
  return [ list_or_dict]

def get_grants( pub_hash, grants, handles):
  if not grants or grants[ "@count"] == 0:
    print( pub_hash + "\t" + empty_grant_hash, file=handles[ "publicationgrant"])  # To avoid outer joins
    return

  for grant in l_d_as_list( grants[ "grant"]):
    if grant is None: # I've seen this AMB 05-07-24
      continue

    grant_arr = [""] * grant_idx_ct

    grant_agencies = l_d_as_list( grant.get( "grant_agency"))
    if grant_agencies:
      grant_arr[ grant_agency_idx] = list_to_string( [item if isinstance( item, str) else item[ "#text"] \
                                       for item in grant_agencies])
    grant_ids = grant.get( "grant_ids")
    if grant_ids and grant_ids[ "@count"] != 0:
      grant_arr[ grant_id_idx] = list_to_string( l_d_as_list( grant_ids[ "grant_id"]))

    grant_str = "\t".join( grant_arr)
    hashval   = cnv_str_md5_int( grant_str)

    print( grant_str + "\t" + hashval, file=handles[ "grant"           ])
    print( pub_hash  + "\t" + hashval, file=handles[ "publicationgrant"])

def get_citations( pub_hash, fr_metadata, handle):
  refs = fr_metadata.get( "references")
  if not refs or refs[ "@count"] == "0":
    return 0
  citation_count=0
  ref_list = refs[ "reference"]
  if isinstance( ref_list, dict):
    ref_list = [ ref_list]
  for ref in ref_list:
    uid = ref.get( "uid")
    if uid:
      citation_count += 1
      print( pub_hash + "\t" + cnv_str_md5_int( uid), file=handle)
  return citation_count

def process_pub_types( pub_types, product_type_map, pub):
  if not pub_types:
    return
  if isinstance( pub_types, list):
    try:
      pub_types.remove( "Retracted Publication")
      pub[ pub_is_retracted_idx] = "1"
    except ValueError:
      pub[ pub_is_retracted_idx] = "0"
    pub_types.sort()
    lookup_key = "\t".join( pub_types)
    if pub[ pub_is_retracted_idx] == "1":
      pub_types.append( "Retracted Publication")   # Mahmoud request
  else:
    if pub_types == "Retracted Publication":
      pub[ pub_is_retracted_idx] = "1"
      pub_types  = None
      lookup_key = "ABCXYZ" # This has never been observed 
    else:
      pub[ pub_is_retracted_idx] = "0"
      lookup_key = pub_types

  pub[ pub_type_idx]        = list_to_string( pub_types)
  pub[ pub_mapped_type_idx] = product_type_map.get( lookup_key, "Unknown mapping")

def wos_parse_record( data, xml_name, already_processed_pubs, product_type_map, handles):
  pub = [""] * pub_idx_ct
  pub_aut_hashes.clear()
  pub_countries.clear()
  pub_unified_names.clear()
  
  pub_id = data.get( "UID", "")   # Maybe should complainif no UID?? AMB 22.12.23

  if pub_id in already_processed_pubs:
    return # No need to do anything

  pub[ pub_id_idx     ] = pub_id
  pub_hash              = cnv_str_md5_int( pub_id)
  pub[ pub_id_hash_idx] = pub_hash

  already_processed_pubs.add( pub_id)

  # churn through the identifiers

  static_data  = data       [ "static_data"        ]
  dynamic_data = data       [ "dynamic_data"       ]
  pub_summary  = static_data[ "summary"            ]
  fr_metadata  = static_data[ "fullrecord_metadata"]

  src = get_source_details( pub_summary, handles)

  process_ids( dynamic_data, pub, src)

  pub[ pub_oa_state_idx] = process_open_access( dynamic_data)

  process_pub_types( get( fr_metadata, [ "normalized_doctypes", "doctype"]), product_type_map, pub)

  pub[ pub_lang_idx]     = get_pub_lang( fr_metadata.get( "languages", None))
  pub[ pub_title_idx]    = get_title( static_data)

  pub_info = pub_summary[ "pub_info"]

  page = pub_info.get( "page", None)
  if page:
    pub[ pub_first_page_idx] = page.get( "@begin", "")
    pub[ pub_last_page_idx ] = page.get( "@end"  , "")

  pub[ pub_pub_year_idx]  = pub_info.get( "@pubyear" , "")
  pub[ pub_pub_month_idx] = pub_info.get( "@pubmonth", "")
  pub[ pub_pub_date_idx]  = pub_info.get( "@sortdate", "")
  pub[ pub_volume_idx]    = pub_info.get( "@vol"     , "")

  pub[ pub_copyright_idx] = data.get( "@r_id_disclaimer", "")   # Why show this?? AMB 22.12.23

  pub[ pub_wuid_idx] = get_wuid( pub_summary) 

  catinfo = fr_metadata.get( "category_info")

  if catinfo:
    pub[ pub_headings_idx   ] = list_to_string( get( catinfo, [ "headings"   , "heading"   ]))
    pub[ pub_subheadings_idx] = list_to_string( get( catinfo, [ "subheadings", "subheading"]))
    # Store subjects as an array AND lookup table - should probably rationalise this AMB 25.11.24
    pub_subjects = get_subjects( catinfo) 
    if pub_subjects:
      pub[ pub_subjects_idx] = list_to_string( pub_subjects)
      for subject in pub_subjects:
        print( f"{pub_hash}\t{subject}", file=handles[ "pubsubject"])
    else:
      pub[ pub_subjects_idx] = None
  else:
    # This is really just for regresion testing. These should be removed later AMB 22,12,23
    pub[ pub_headings_idx] = pub[ pub_subheadings_idx] = pub[ pub_subjects_idx] = list_to_string( None)

  pub[ pub_abstract_idx ] = list_or_string( get( fr_metadata, [ "abstracts", "abstract", "abstract_text", "p"]))

  fund_ack = fr_metadata.get( "fund_ack")
  if fund_ack:
    pub[ pub_fund_text_idx] = list_or_string( get( fund_ack, ["fund_text", "p"]))
    get_grants( pub_hash, fund_ack.get( "grants"), handles)
  else:
    get_grants( pub_hash, None, handles) # Create dummy grant

  pub[ pub_keywords_idx] = get_author_keywords( pub_hash, fr_metadata, handles[ "authorkeyword"])

  src_str  = "\t".join( src)
  src_hash = cnv_str_md5_int( src_str)

  get_authorship_details( pub_hash, fr_metadata, pub_summary, static_data.get( "contributors"), handles)

  if len( pub_aut_hashes) == 0 :
    # Paranoia
    pub_aut_hashes.add( empty_aut_hash)
    print( empty_aut_str, file=handles[ "author"])

  pub[ pub_authors_idx] = list_to_string( list( pub_aut_hashes))

  if len( pub_countries):
    pub[ pub_countries_idx] = list_to_string( list( pub_countries))
    
  if len( pub_unified_names):
    pub[ pub_unified_names_idx] = list_to_string( list( pub_unified_names))
    
  pub[ pub_ref_count_idx] = str( get_citations( pub_hash, fr_metadata, handles[ "citation"]))

  print( "\t".join( pub + [xml_name, src_hash]), file=handles[ "publication"])
  print( src_str + "\t" + src_hash, file=handles[ "source"])

  for country in pub_countries:
    print( f"{pub_hash}\t{country}", file=handles[ "pubcountry"])
  for p_u_n in pub_unified_names:
    print( f"{pub_hash}\t{p_u_n}", file=handles[ "puborg"])

#<<<< wos_parse_record

def wos_parser( xml_file              : str ,
                alread_processed_pubs : set ,
                product_type_map      : dict,
                handles               : dict):
  xml_name = os.path.basename( xml_file)

  print( empty_aff_str  , file=handles[ "affiliation"])
  print( empty_grant_str, file=handles[ "grant"      ])

  # Exact lab used etree code to decode WoS data. They seem to know what they are doing with xml, so_
  # Using lxml will reduce memory footprint

  rec_iter = etree.iterparse( xml_file, tag=TAG)
  for _, record in rec_iter:
    data = etree.tostring( record).decode().replace( "<inf>", "") .replace( "</inf>", ""    ). \
                                            replace( "<sup>", "") .replace( "</sup>", ""    ). \
                                            replace( "\n"   , " ").replace( "\\"    , "\\\\")
    wos_parse_record( xmltodict.parse( data)["REC"], xml_name, alread_processed_pubs, product_type_map, handles)
    record.clear()
  # Why - grbage collector will do this del rec_iter
