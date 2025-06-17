import json
from typing import Any, Optional
import pandas as pd
from ast import literal_eval

from db.db_importer import dump_table
from constants import CONTRIBUTOR_LABELS_SET, LEITZHAL_TABLE, OUT_BCP_PATH, LEITZAHL_COLUMNS

def formatted_print(obj):
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

def extract_metadata(raw_metadata: dict):
	metadata: list = raw_metadata.get("metadata")
	metadata.append({"key": "rc.item.id", "value": raw_metadata.get("id"), "language": None})
	return metadata

def clean_csv_value(value: Optional[Any]) -> str:
	if value is None:
		return r'\\N'
	return str(value).replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').encode('utf-8').decode('ascii',errors='ignore')

def reduce_metadata(metadata: list):
	list_pub = []
	for pub in metadata:
		pub_dict = {}
		for key_obj in pub:
			key = key_obj.get('key').lower().replace(".", "_")
			value = clean_csv_value(key_obj.get('value'))
			if key in pub_dict:
				if isinstance(pub_dict[key], list):
					pub_dict[key].append(value)
				else:
					pub_dict[key] = [pub_dict[key], value] 
			else:
				pub_dict[key] = value
		list_pub.append(pub_dict)
	return list_pub

def parse_contributors(dataFrame: pd.DataFrame):
	contributors_set = set()
	#local_authors_df = pd.DataFrame(columns=['rc_id', 'full_name', 'type'])
	local_authors_list = []
	contributors_rows = dataFrame[dataFrame.columns.intersection(CONTRIBUTOR_LABELS_SET)].values.tolist()
	columns = dataFrame.columns.intersection(CONTRIBUTOR_LABELS_SET).values.tolist()
	for row in contributors_rows:
		for idx, col in enumerate(row):
			if idx != columns.index('handle_id') and idx != columns.index('rc_item_id') and not pd.isna(col):
				if '[' in col:
					inner_contrib_list = literal_eval(col)
					for inner_name in inner_contrib_list:
						#local_authors_df.loc[len(local_authors_df)] = [row[columns.index('rc_item_id')], inner_name, columns[idx].split('.')[-1]]
						local_authors_list.append([row[columns.index('handle_id')], row[columns.index('rc_item_id')], clean_csv_value(inner_name.replace('"', '')), columns[idx].split('_')[-1]])
						#contributors_set.add(inner_name)
				else:
					#local_authors_df.loc[len(local_authors_df)] = [row[columns.index('rc_item_id')], col, columns[idx].split('.')[-1]]
					local_authors_list.append([row[columns.index('handle_id')], row[columns.index('rc_item_id')], clean_csv_value(col.replace('"', '')), columns[idx].split('_')[-1]])
					#contributors_set.add(col) 
	return contributors_set, local_authors_list

# ------------------------- CKONSORG ----------------------------------------------------------------------------

from datetime import datetime

def get_latest_ckonsorg_filename():
	#yearmonth running script
	current_month = datetime.now().strftime('%m')
	current_year = datetime.now().strftime('%Y')

	ckonsorg_file_name = f'ckonsorg_{current_year}{current_month}.csv'
	return ckonsorg_file_name

# ------------------------- LEITZAHL ----------------------------------------------------------------------------

def extract_leitzahl(handle_id, rc_item_id, ethz_lz_s, ethz_ls_ids_certified):
    ethz_ou_list = []
    if type(ethz_lz_s) == str:
        ethz_lz_arr = [x.strip() for x in ethz_lz_s.split('::')]
        ethz_lz_leaf = ethz_lz_arr[-1]
        for ethz_ou in ethz_lz_arr:
            ethz_ou_tuple = [x.strip() for x in ethz_ou.split('-')]
            if len(ethz_ou_tuple) > 1:
                is_leaf = ethz_ou == ethz_lz_leaf
                is_cert = None
                try:
                    ethz_ls_ids_certified_eval = literal_eval(ethz_ls_ids_certified)
                except (ValueError, SyntaxError) as e:
                    ethz_ls_ids_certified_eval = ethz_ls_ids_certified                
                if is_leaf and not isinstance(ethz_ls_ids_certified_eval, float):
                    is_cert = ethz_ou_tuple[0] in ethz_ls_ids_certified
                ethz_ou_list.append([handle_id, rc_item_id, ethz_ou_tuple[0], ethz_ou_tuple[1], is_leaf, is_cert])
    return ethz_ou_list 

def parse_leitzahl(leitzhal_df: pd.DataFrame):
	ethz_ou_rows_list = []
	for index, row in leitzhal_df.iterrows():
		rc_item_id = row['rc_item_id']
		handle_id = row['handle_id']
		ethz_leitzahlidentifiers_certified = row['ethz_leitzahlidentifiers_certified']
		try:
			ethz_leitzahl = literal_eval(row['ethz_leitzahl'])
		except (ValueError, SyntaxError) as e:
			ethz_leitzahl = row['ethz_leitzahl']
		if isinstance(ethz_leitzahl, list):
			for ethz_lz in ethz_leitzahl:
				ethz_ou_rows_list += extract_leitzahl(handle_id, rc_item_id, ethz_lz, ethz_leitzahlidentifiers_certified)
		elif isinstance(ethz_leitzahl, str):
			ethz_ou_rows_list += extract_leitzahl(handle_id, rc_item_id, ethz_leitzahl, ethz_leitzahlidentifiers_certified)
		else:
			print("ethz_leitzahl is neither a list nor a string.")
	BCP_FILE = 'leitzhal.bcp'
	bcp_file_path = OUT_BCP_PATH+BCP_FILE
	ethz_ou_rows_df = pd.DataFrame(ethz_ou_rows_list, columns=LEITZAHL_COLUMNS)
	ethz_ou_rows_df.to_csv(bcp_file_path, sep='\t', index=False, index_label='\t', header=False)
	dump_table(LEITZHAL_TABLE, bcp_file_path, LEITZAHL_COLUMNS)


CK_LV_COLUMNS = {'lz90':'na90','lz80':'na80','lz70':'na70','lz60':'na60','lz50':'na50','lz40':'na40','lz30':'na30','lz20':'na20'}


def get_missing_leitzahls(ckonsorg_df: pd.DataFrame, full_stored_leitzhal_df: pd.DataFrame):
	# Identify the 'lz' columns in ckonsorg_df
	lz_columns = [col for col in ckonsorg_df.columns if col.startswith('lz')]

	# Flatten the ckonsorg_df: Create a DataFrame with 'ou_code', 'lz_match', and 'source_index' columns
	flat_df = pd.DataFrame()

	for lz_col in lz_columns:
		temp_df = ckonsorg_df[[lz_col]].copy()
		temp_df['lz_match'] = lz_col
		#temp_df['source_index'] = temp_df.index  # Capture the source index
		temp_df = temp_df.rename(columns={lz_col: 'ou_code'})
		flat_df = pd.concat([flat_df, temp_df])

	# Drop duplicates to avoid redundant merges
	flat_df = flat_df.drop_duplicates(subset=['ou_code'])

	# Merge leitzahl_df with flat_df on 'ou_code'
	leitzahl_df = full_stored_leitzhal_df.merge(flat_df, on='ou_code', how='left')

	leitzahl_row_to_add = []

	# Set-based lookup for faster membership checking
	existing_ou_codes = set(zip(leitzahl_df['handle_id'], leitzahl_df['rc_item_id'], leitzahl_df['ou_code']))

	filtered_leitzahl_df = leitzahl_df[leitzahl_df.is_leaf == True]

	for idx, leitzahl_row in filtered_leitzahl_df.iterrows():
		ckonsorg_row = ckonsorg_df[ckonsorg_df[leitzahl_row.lz_match].str.contains(leitzahl_row.ou_code)]
		lz_match_idx = list(CK_LV_COLUMNS).index(leitzahl_row.lz_match)
		for i in range(1, lz_match_idx+1):
			ck_parent_key = list(CK_LV_COLUMNS)[lz_match_idx-i]
			ck_parent_value = ckonsorg_row[ck_parent_key].values[0]
			if (leitzahl_row.handle_id, leitzahl_row.rc_item_id, ck_parent_value) not in existing_ou_codes:
				leitzahl_row_to_add.append({
					'handle_id':leitzahl_row.handle_id, 
					'rc_item_id': leitzahl_row.rc_item_id, 
					'ou_code': ck_parent_value,
					'ou_name': ckonsorg_row[CK_LV_COLUMNS.get(ck_parent_key)].values[0],
					'is_leaf':	False,
					'is_certified': None,
					'lz_match':	ck_parent_key})
				existing_ou_codes.add((leitzahl_row.handle_id, leitzahl_row.rc_item_id, ck_parent_value))

	lz_df_w_missing_lz = pd.concat([pd.DataFrame(leitzahl_row_to_add), leitzahl_df], ignore_index=True)
	return lz_df_w_missing_lz