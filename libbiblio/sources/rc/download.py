#!/usr/bin/env python3

import argparse
from utils import extract_metadata, reduce_metadata
from service import RC_Api
import json
from io import StringIO
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(filename='./logs/download.log', 
					filemode='w',
					level=logging.DEBUG,
					format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

LIMIT = 250

def queryAPI(year: int):
	query = f'dc.date.issued:"{year}" AND ethz.eth:"yes"'
	page = 0
	total_records = 0
	metadata = list()
	logging.info(f'START - Retriving {page=} {year=} ...')
	while (page*LIMIT <= total_records):
		if page > 0:
			logging.info(f'Retriving {page=} {year=} ...')
		offset = page * LIMIT
		parameters_search = {
			"limit": LIMIT,
			"offset": offset,
			"expand": "metadata",
			"query": query
		}
		res_obj = RC_Api.search(parameters = parameters_search)
		total_records += len(res_obj)
		page += 1
		if(total_records > 0):
			metadata += list(map(lambda x: extract_metadata(x), res_obj))
		else:
			logging.info(f'DONE - No records for {year=}')
	logging.info(f'DONE - Retrived page={page-1} {total_records=} {year=}')
	return metadata, total_records

def download_metadata(range: list, dest: str):
	for year in range:
		try:
			metadata, total_records = queryAPI(year)
			if(total_records > 0):
				reduced_metadata = reduce_metadata(metadata)
				text = json.dumps(reduced_metadata, sort_keys=True)
				df = pd.read_json(StringIO(text), dtype=str, encoding='utf-8')
				path_to_save = f'{dest}/{year}_metadata.csv'
				df.to_csv(path_to_save, mode='w', index=False, escapechar='\n', encoding='utf-8')
		except Exception as error:
			logging.error(f"An error occured while downloading {year=} with {error=}")
			continue

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Download items from Research Collection API year by year and filtered by ethz.eth:'yes'",
									formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("-a", "--all", help="all years fromm 1900 to today")
	parser.add_argument("-f", "--from", help="year from included", required=True, type=int)
	parser.add_argument("-t", "--to", help="year to excluded", required=True, type=int)
	parser.add_argument("-d", "--dest", help="download destination location", default='/home/bibliometric/data/research_collection/input')
	args = parser.parse_args()
	config = vars(args)
	logging.info('Start download with config='+str(config))
	if config['all']:
		year = datetime.now().year
		download_metadata(range(1900, year+1), config['dest'])
	else:
		download_metadata(range(config['from'], config['to']), config['dest'])
