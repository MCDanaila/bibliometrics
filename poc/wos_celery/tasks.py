import os
import sys
import shutil
import subprocess
import gzip
import time
from zipfile import ZipFile
from glob import glob
from celery import current_task

# Ensure libbiblio is discoverable. If poc is run from root, this might be needed.
# Or adjust PYTHONPATH when running worker/dispatcher.
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from libbiblio.sources.wos.wos_parser import wos_parser, get_product_type_map as get_wos_product_type_map, product_type_map as wos_product_type_map_global
from .celery_app import app

# Helper function from wos_ingestor.py, can be made local to the task or imported if moved to a shared utils
def set_ready_files(bcp_path):
    with open(bcp_path + ".publication.ready", "w"), \
         open(bcp_path + ".author.ready", "w"), \
         open(bcp_path + ".authorship.ready", "w"), \
         open(bcp_path + ".source.ready", "w"), \
         open(bcp_path + ".citation.ready", "w"), \
         open(bcp_path + ".affiliation.ready", "w"), \
         open(bcp_path + ".authorkeyword.ready", "w"), \
         open(bcp_path + ".grant.ready", "w"), \
         open(bcp_path + ".publicationgrant.ready", "w"), \
         open(bcp_path + ".puborg.ready", "w"), \
         open(bcp_path + ".pubcountry.ready", "w"), \
         open(bcp_path + ".pubsubject.ready", "w"):
        pass

@app.task(bind=True, name="poc.wos_celery.tasks.process_wos_zip_task")
def process_wos_zip_task(self, zip_filepath: str, bcp_dir: str):
    task_id = self.request.id
    print(f"[{task_id}] Received task to process WoS ZIP file: {zip_filepath}")
    print(f"[{task_id}] BCP output directory: {bcp_dir}")

    # Ensure product_type_map is loaded for the wos_parser
    current_product_type_map = None
    if wos_product_type_map_global is None:
        print(f"[{task_id}] Global wos_product_type_map is None, calling get_wos_product_type_map()")
        get_wos_product_type_map() # This should populate the global wos_product_type_map_global

    current_product_type_map = wos_product_type_map_global

    if current_product_type_map is None:
        print(f"[{task_id}] ERROR: WoS Product type map could not be loaded even after calling get_wos_product_type_map.")
        raise ValueError("WoS Product type map failed to load")


    zip_basename = os.path.basename(zip_filepath).replace(".zip", "")
    zip_basename = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in zip_basename)

    bcp_file_base = os.path.join(bcp_dir, zip_basename)

    os.makedirs(bcp_dir, exist_ok=True)
    # Temporary directory for XML files extracted for parsing for this specific task run
    temp_xml_extract_dir = os.path.join(bcp_dir, "temp_xml_for_poc", task_id)
    os.makedirs(temp_xml_extract_dir, exist_ok=True)


    handles = {}
    bcp_files_to_create = [
        "publication", "author", "authorship", "source", "citation",
        "affiliation", "authorkeyword", "grant", "publicationgrant",
        "puborg", "pubcountry", "pubsubject"
    ]

    try:
        for bcp_type in bcp_files_to_create:
            handles[bcp_type] = open(f"{bcp_file_base}.{bcp_type}.bcp", "w", encoding='utf-8')

        print(f"[{task_id}] Processing ZIP file: {zip_filepath}")
        already_processed_pubs_in_zip = set()

        with ZipFile(zip_filepath, 'r') as zip_ref:
            for member_name in zip_ref.namelist():
                temp_xml_path = None # Define here to ensure it's available for cleanup if error occurs mid-loop
                if member_name.endswith(".xml.gz"):
                    print(f"[{task_id}] Processing gzipped member: {member_name}")
                    with zip_ref.open(member_name) as gz_file_stream:
                        with gzip.GzipFile(fileobj=gz_file_stream) as xml_stream:
                            temp_xml_path = os.path.join(temp_xml_extract_dir, os.path.basename(member_name)[:-3]) # remove .gz
                            with open(temp_xml_path, 'wb') as temp_xml_file:
                                shutil.copyfileobj(xml_stream, temp_xml_file)

                            print(f"[{task_id}] Parsing XML file: {temp_xml_path}")
                            wos_parser(temp_xml_path, already_processed_pubs_in_zip, current_product_type_map, handles)
                            os.remove(temp_xml_path)

                elif member_name.endswith(".xml"):
                    print(f"[{task_id}] Processing plain XML member: {member_name}")
                    with zip_ref.open(member_name) as xml_stream:
                        temp_xml_path = os.path.join(temp_xml_extract_dir, os.path.basename(member_name))
                        with open(temp_xml_path, 'wb') as temp_xml_file:
                            shutil.copyfileobj(xml_stream, temp_xml_file)

                        print(f"[{task_id}] Parsing XML file: {temp_xml_path}")
                        wos_parser(temp_xml_path, already_processed_pubs_in_zip, current_product_type_map, handles)
                        os.remove(temp_xml_path)

        # Clean up the task-specific temporary extraction directory
        if os.path.exists(temp_xml_extract_dir):
            shutil.rmtree(temp_xml_extract_dir)

        set_ready_files(bcp_file_base)
        result_message = f"Successfully processed {zip_filepath}. BCP files generated in {bcp_dir} prefixed with {zip_basename}."
        print(f"[{task_id}] {result_message}")
        return {"status": "SUCCESS", "message": result_message, "input_file": zip_filepath, "bcp_prefix": zip_basename}

    except Exception as e:
        error_message = f"Failed to process {zip_filepath}. Error: {type(e).__name__} - {str(e)}"
        import traceback
        print(f"[{task_id}] {error_message}\n{traceback.format_exc()}")
        raise
    finally:
        for bcp_type in bcp_files_to_create:
            if bcp_type in handles and handles.get(bcp_type) and not handles[bcp_type].closed:
                handles[bcp_type].close()
        print(f"[{task_id}] Closed all BCP file handles for {zip_filepath}")
        # Clean up task-specific temp dir again in case of error during processing loop
        if os.path.exists(temp_xml_extract_dir):
            try:
                shutil.rmtree(temp_xml_extract_dir)
            except Exception as cleanup_e:
                print(f"[{task_id}] Error during final cleanup of {temp_xml_extract_dir}: {str(cleanup_e)}")


@app.task(name="poc.wos_celery.tasks.example_task_add")
def example_task_add(x, y):
    return x + y

if __name__ == '__main__':
    print("This module defines Celery tasks. Run workers to execute them.")
