# WoS Celery PoC Changelog

## 2025-06-17
- Initialized PoC branch.
- Created CHANGELOG.md.
- Added celery[librabbitmq] to requirements.txt (pyproject.toml not found).
- Created directory structure for WoS Celery PoC (poc/wos_celery/).
- Created initial Python files: __init__.py, celery_app.py, tasks.py, config.py.
- Populated initial content for WoS Celery PoC files:
  - poc/wos_celery/config.py (broker settings)
  - poc/wos_celery/celery_app.py (Celery app instance)
  - poc/wos_celery/tasks.py (placeholder processing task)
- Created poc/wos_celery/README.md with instructions for running the PoC.

## 2025-06-17 - RabbitMQ Setup
- Confirmed RabbitMQ setup instructions (using Docker) are documented in `poc/wos_celery/README.md`.

## 2025-06-17 - Celery App Configuration
- Reviewed existing Celery application setup in `poc/wos_celery/celery_app.py` and `poc/wos_celery/config.py`.
- Configuration for broker (RabbitMQ), result backend (RPC), task discovery, and a dedicated 'wos_tasks' queue are correctly in place.
- No changes needed to the Celery app configuration for the PoC.

## 2025-06-17 - Develop WoS ZIP Processing Celery Task
- Defined `process_wos_zip_task` in `poc/wos_celery/tasks.py`, replacing the placeholder.
- Task logic adapted from `libbiblio/sources/wos/wos_ingestor.py` (`wos_ingest_zip`).
- Handles loading of WoS product type map within the task by calling `get_wos_product_type_map` which should populate the global `wos_product_type_map_global` in `wos_parser.py`.
- Processes a single WoS ZIP file passed as `zip_filepath`.
- Extracts `.xml.gz` or `.xml` files from the ZIP.
- For `.xml.gz` files, it unzips them.
- XML content is temporarily written to disk in a task-specific sub-directory under `bcp_dir/temp_xml_for_poc/<task_id>/` before parsing, as `wos_parser` currently expects a file path. This temporary directory is cleaned up after processing or if an error occurs.
- Calls `wos_parser` for each XML file to generate BCP data into multiple .bcp files.
- BCP files are named using the ZIP basename and stored in the provided `bcp_dir`.
- Creates `.ready` files upon completion for all BCP types.
- Includes error handling and ensures file handles are closed and temporary files/directories are cleaned up.
- Kept `example_task_add` for basic Celery testing.
- Added `sys.path.append` in tasks.py to aid module discovery during PoC development; this might need refinement for a production setup.

## 2025-06-17 - Create Task Dispatcher Script
- Created `poc/wos_celery/dispatch_wos_poc_task.py`.
- This script takes a WoS ZIP file path and a BCP output directory as command-line arguments.
- It dispatches the `process_wos_zip_task` to the Celery queue.
- Includes basic validation for file existence and BCP directory creation.
- Made the script executable.
