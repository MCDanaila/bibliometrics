from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from hashlib import md5

import xmltodict
import json       # for debug

#>>>> cnv

def cnv( in_string: str, replace = ""):
  return in_string if in_string else replace

#<<<< cnv

#<<<<

def list_to_string( details):
  # Alchemy takes a list and converts into a string like 
  # {"Diffuse uptake",FDG-PET,"Focal uptake","Thyroid cancer"}

  if not details:
    return ""

  if isinstance( details, str):
    details = [ details]

  details = ",".join( [ '"' + d  +'"' if " " in d else d for d in details])

  return "{" + details + "}"

#>>>> get

def get(data, keys):
  element = data
  for key in keys:
    if isinstance(element, dict) and (key in element):
      element = element[key]
    else:
      return None

  return element

#<<<< get

#>>>> get_source_details

def format_issn( issn):
  return issn.get( "@type", "") + ":" + issn.get( "#text", "")

def get_source_details( source, value_status, handles: Dict): # source guaranteed non null
  # ISSN needs special handling
  issn = source.get( "issn", None)
  issn_list = []
  if issn:
    if isinstance( issn, dict):
      issn_list.append( format_issn( issn))
    elif isinstance( issn, list):
      issn_list = [ format_issn( i) for i in issn ]
    else:
      issn_list.append( "general:" + issn) 
    issn = list_to_string( issn_list)
  else:
    issn = ""
      
  sourcetitle = source.get( "sourcetitle", "")
  if isinstance( sourcetitle, dict): # Sometimes happens
    sourcetitle = sourcetitle.get( '#text', "")

  print( source.get( "@srcid", "") + "\t" + sourcetitle + "\t" + \
          source.get( "sourcetitle-abbrev", "") +  "\t" + issn + "\t" + \
            source.get( "codencode", "") + "\t" + \
              cnv( get( source, [ "publisher", "publishername"])) + "\t" + value_status, \
                file=handles[ "source"])

#<<<< get_source_details

#>>>> get_citations

def get_citations( references, pub_id, value_status, handles):
  # References will be a list. Unfortunately the referenced paper can 
  # appear many times if seperate pages are referenced

  refset = set()

  for ref in references:
    item = get(ref, ["ref-info", "refd-itemidlist", "itemid"])
    itemid = None
    if item:
      if isinstance( item, dict):
        if item.get( "@idtype", "") == "SGR":
          itemid = item.get( "#text", "")
      else: # It'll be a list
        for x in item:
          if isinstance (x, dict) and x.get( "@idtype", "") == "SGR":
            itemid = x.get( "#text", "")

      if itemid:
        refset.add( itemid)

  for ref in refset:
    print( pub_id + "\t" + ref + "\t" + value_status, file=handles[ "citation"])
    
#<<<< get_citations

#<<<< get_author_details

def get_author_details( groups, pub_id: int, value_status: str, handles: Dict):
  # There's a known "feature" in scopus data where authorships and  affiliations are duplicated

  affiliation_set = set()
  authorship_set  = set()
  author_set     = set()

  # These could be done with enums but I can't see the point

  aff_afid         = 0
  aff_dptid        = 1
  aff_organisation = 2
  aff_country      = 3
  aff_address      = 4
  aff_city         = 5

  aut_id             = 0
  aut_degrees        = 1
  aut_given_name     = 2
  aut_surname        = 3
  aut_indexed_name   = 4
  aut_preferred_name = 5
  aut_e_address      = 6

  # Literal values allow indices for resolving post staging

  empty_aff = [ ""] * (aff_city      + 1)
  empty_aut = [ ""] * (aut_e_address + 1)
  aut_string = "\t".join( empty_aut)
  empty_aut_hash = md5( aut_string.encode()).hexdigest()[:16] 
  aff_string = "\t".join( empty_aff)
  empty_aff_hash = md5( aff_string.encode()).hexdigest()[:16] 

  if groups:
    if isinstance( groups, dict):  # Only one - convert into List
      groups = [groups]

    # Go through all the groups

    for group in groups:
      aff = empty_aff.copy()
      affiliation = get( group, ["affiliation"]) 
      # This will be a single item
      if affiliation:
        details_found = 1 
        aff[ aff_afid   ] = cnv( get( affiliation, [ "@afid"       ]))
        aff[ aff_dptid  ] = cnv( get( affiliation, [ "@dptid"      ]))
        aff[ aff_country] = cnv( get( affiliation, [ "@country"    ]))
        aff[ aff_address] = cnv( get( affiliation, [ "address-part"]))
        aff[ aff_city   ] = cnv( get( affiliation, [ "city-group"  ]))

        # Apparently organistion can be a list

        org = get( affiliation, [ "organization"])
        if org:
          if isinstance( org, str):
            aff[ aff_organisation] = org
          else:
            # Sometimes the elements of the list are directories. It might be a scopus bug
            # but just in case.
            orglist = []
            for orgelem in org:
              if isinstance( orgelem, dict):
                orgelem = cnv( get( orgelem, ["#text"]))
              if orgelem:                               # And sometimes it completely empty
                orglist.append( orgelem)
            aff[ aff_organisation] = ",".join( orglist)

      aff_string = "\t".join( aff)
      aff_hash = md5( aff_string.encode()).hexdigest()[:16]
      affiliation_set.add( "\t".join( [aff_string] + [aff_hash] + [value_status]))

      author_found = 0

      authors = get( group, ["author"])

      if not isinstance( authors, List):
        authors = [authors]

      for author in authors:
        author_found = 1
        aut = empty_aut.copy()

        if author: # Why do I test for this? AMB 19.12.23
          author_id = cnv( get( author, ["@auid"]))
          seq       = cnv( get( author, ["@seq" ]))

          # if not auid:
            # Do something defensive. But I think would be paranoid

          # aut_preferred_name formatting is still being discussed AMB 210723

          aut[ aut_id          ] = author_id
          aut[ aut_degrees     ] = cnv( get( author, ["ce:degrees"]           ))
          aut[ aut_given_name  ] = cnv( get( author, ["ce:given-name"]        ))
          aut[ aut_surname     ] = cnv( get( author, ["ce:surname"]           ))
          aut[ aut_indexed_name] = cnv( get( author, ["ce:indexed-name"]      ))
          aut[ aut_e_address   ] = cnv( get( author, ["ce:e-address", "#text"]))

          aut_string = "\t".join( aut)
          aut_hash = md5( aut_string.encode()).hexdigest()[:16] 
          author_set.add( "\t".join( [aut_string] + [aut_hash] + [value_status]))

          authorship_set.add( "\t".join( [pub_id, seq] + aut + aff + [aut_hash] + [aff_hash] + [value_status]))

      if author_found == 0:
        authorship_set.add( "\t".join( [ pub_id, ""] + empty_aut + aff + [empty_aut_hash] + [aff_hash] + [value_status]))
        author_set.add( "\t".join( empty_aut + [empty_aut_hash] + [value_status]))

  if len( authorship_set) == 0:
    authorship_set.add( "\t".join( [ pub_id, ""] + empty_aut + empty_aff + [empty_aut_hash] + [empty_aff_hash] + [value_status]))
    author_set.add( "\t".join( empty_aut + [empty_aut_hash] + [value_status]))

  for author in author_set:
    print( author, file=handles[ "author"])
  for authorship in authorship_set:
    print( authorship, file=handles[ "authorship"])
  for affiliation in affiliation_set:
    print( affiliation, file=handles[ "affiliation"])

#<<<< get_author_details

#>>>> get_id

def get_id( bib_record: Dict, type:str):
  itemid = get( bib_record, [ "item-info", "itemidlist", "itemid"])

  for x in itemid:
    if x["@idtype"] == type:
      return x["#text"]
  raise Exception( type + " ID not found")   # AMB - handle these!! AMB 150723

#<<<< get_id

#>>>> get_pii

def get_pii( data: Dict):
  pii = get( data, ["xocs:doc", "xocs:meta", "xocs:pii"])
  if pii:
    return pii

  # Fallback value

  return get( data, [ "xocs:doc", "xocs:item", "item", "bibrecord",
                        "item-info", "itemidlist", "ce:pii"]) 

#<<<< get_pii

#>>>> get_title_details

def get_title_details( title_details: Dict):
  title_dict = {}

  title_dict[ "title"           ] = "" 
  title_dict[ "english_title"   ] = "" 
  title_dict[ "alternate_titles"] = ""

  if isinstance( title_details, Dict):
    title_dict[ "title"] = cnv( get(title_details, ["#text"]))
    if get(title_details, ["@xml:lang"]) == "eng":
      title_dict[ "english_title"] = title_dict[ "title"]
    return title_dict

  if not isinstance( title_details, List):
    title_dict[ "title"] = "NO TITLE DETAILS SUPPLIED BY SCOPUS"
    return title_dict
    
  alternates = []
  for title in title_details:
    this_text = cnv(get(title, ["#text"]))
    this_lang = get(title, ["@language"])
    if get(title, ["@original"]) == "y":
      title_dict[ "title"] = this_text
    else:
      alternates.append( this_lang + ":" + this_text)
    if get(title, ["@xml:lang"]) == "eng": 
      title_dict[ "english_title"] = this_text

  if len( alternates) > 0:
    title_dict[ "alternate_titles"] = list_to_string( alternates)

  return title_dict

#<<<< get_title_details

#>>>> get_abstract

def get_abstract( head:Dict):
  abstract = get( head, [ "abstracts", "abstract", "ce:para"])

  if not abstract:
    return ""

  # Sometimes the abstract contains line feeds we have to defend against this

  ourText = ""
  if isinstance( abstract, str):
    ourText =  abstract
  elif isinstance( abstract, list):
    ourText = " ".join( abstract)
  else:
    ourText = get( abstract, [ "#text"]) 

  return ourText

#<<<< get_abstract

#>>>> get_author_keywords

def get_author_keywords( citation_info: Dict, pub_id, value_status, file_handle):
  keywords = get( citation_info, [ "author-keywords", "author-keyword"])

  if isinstance( keywords, Dict):
    print( "\t".join( [ pub_id, cnv( get( keywords, ["#text"])), value_status]), file=file_handle)
    
  if isinstance( keywords, List):
    for keyword in keywords:
      if keyword:
        if isinstance( keyword, dict):
          keyword = cnv( get( keyword, ["#text"]))
        else:
          keyword = cnv( keyword)
      print( "\t".join( [ pub_id, keyword, value_status]), file=file_handle)
          
#<<<< get_author_keywords 

#>>>> get_descriptions

def get_descriptions( descriptor_group, pub_id, value_status, file_handle):
  descriptors = descriptor_group.get( "descriptors")

  if isinstance( descriptors, dict): # Only for dev
    descriptors = [descriptors]
    ## a = [] ; 
    ## a.append( None)
    ## print( "\t".join( a))

  for item in descriptors:
    if isinstance( item, dict):
      controlled = item.get( "@controlled", "")
      type       = item.get( "@type"      , "")
      desc_list  = item.get( "descriptor"     )
      if desc_list:
        if isinstance( desc_list, dict):
          desc_list = [ desc_list]
        for desc in desc_list:
          mainterm = desc.get( "mainterm") ;
          if mainterm:
            print( "\t".join( [ pub_id, type, mainterm.get( "#text", ""), mainterm.get( "@weight", ""),
                                 controlled,  mainterm.get( "@candidate", ""), value_status]),
                                   file=file_handle) ;
    else: # For dev
      a = [] ; 
      a.append( None)
      print( "\t".join( a))

#<<<< get_descriptions

#>>>> scopus_parser

def scopus_parser( datastr :str, xml_name: str, zip_name: str, handles:dict):

  value_status = "S"    # Eventually this will be either S(table) or U(pdate)

  # remove <inf> and <sub> delimiters

  data = xmltodict.parse( datastr.replace( "<inf>", "") .replace( "</inf>", ""    ). \
                                  replace( "<sup>", "") .replace( "</sup>", ""    ). \
                                  replace( "\n"   , " ").replace( "\\"    , "\\\\"))

  bib_record = get( data, [ "xocs:doc", "xocs:item", "item", "bibrecord"])

  head   = bib_record.get( "head"  , None) # Paranoia
  source = head.get      ( "source", None) # Paranoia

  pub = []

  pub_id = get_id( bib_record, "SCP")
  pub.append( pub_id) 

  pub.append( get_id( bib_record, "SGR")) # sgrid

  pub.append( cnv( source.get( "@srcid", None))) # source_id

  pub.append( cnv( get( bib_record, [ "item-info", "itemidlist", "ce:doi"])))

  pub.append( cnv( get_pii( data))) # ce-ern - Needs all data 

  citation_info = head.get( "citation-info", None)

  pub.append( cnv( get( citation_info, [ "citation-type"    , "@code"    ]))) # pub_type
  pub.append( cnv( get( citation_info, [ "citation-language", "@xml:lang"]))) # pub_lang Maybe revisit AMB 17071131

  title_dict = get_title_details( get( head, [ "citation-title", "titletext"]))

  pub.append( title_dict[ "title"           ])
  pub.append( title_dict[ "english_title"   ])
  pub.append( title_dict[ "alternate_titles"])

  pub_date_dets = get( head, [ "source", "publicationdate"])

  if isinstance( pub_date_dets, Dict):
    pub.append( cnv( get( pub_date_dets, ["year" ])))
    pub.append( cnv( get( pub_date_dets, ["month"])))
    pub.append( cnv( get( pub_date_dets, ["day"  ])))
  else:
    pub.append( "")
    pub.append( "")
    pub.append( "")

  get_author_keywords( citation_info, pub_id, value_status, handles[ "authorkeyword"])

  meta = get( data, [ "xocs:doc", "xocs:meta"])

  pub.append( cnv( meta[ "xocs:volume"   ]))
  pub.append( cnv( meta[ "xocs:issue"    ]))
  pub.append( cnv( meta[ "xocs:firstpage"]))
  pub.append( cnv( meta[ "xocs:lastpage" ]))

  pub.append( cnv( get( bib_record, [ "item-info", "copyright", "#text"])))

  pub.append( cnv(get_abstract( head)))

  """
  Remove these comments. Maybe.
  Need
        "xocs:open-access": {
        "xocs:oa-access-effective-date": "2020-09-26",
        "xocs:oa-article-status": {
          "@is-open-access": "1",
          "@free-to-read-status": "all publisherhybridgold",
          "#text": "Full"
        },
  """
  
  open_access = meta.get( "xocs:open-access", None)
  if( open_access):
    open_status = open_access.get( "xocs:oa-article-status", None)

  if( open_access and open_status ):
    pub.append(  open_status.get( "@is-open-access"     , ""))
    pub.append(  open_status.get( "@free-to-read-status", ""))
    pub.append(  open_status.get( "#text"               , ""))
  else:
    pub += ([""] * 3)

  # That's a complete publication record

  print( "\t".join( pub + [xml_name, zip_name, value_status]), file=handles[ "publication"])

  author_groups = head.get( "author-group", None)

  get_author_details( head.get( "author-group", None), pub_id, value_status, handles)  # Even null is valid to process

  if source:
    get_source_details( source, value_status, handles)

  descriptor_group = get( head, [ "enhancement", "descriptorgroup"])

  if descriptor_group:
    get_descriptions( descriptor_group, pub_id, value_status, handles[ "descriptor"])

  references = get( bib_record, [ "tail", "bibliography", "reference"])
  if references:
    get_citations( references, pub_id, value_status, handles)
 

#<<<< scopus_parser
