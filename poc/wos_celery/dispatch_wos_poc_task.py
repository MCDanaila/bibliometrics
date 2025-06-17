import argparse
import os
import sys

# Ensure libbiblio and poc modules are discoverable
# This might need adjustment based on how the script is run relative to the project root
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from poc.wos_celery.tasks import process_wos_zip_task

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dispatch a WoS ZIP processing task to Celery for PoC.")
    parser.add_argument("zip_filepath", help="Full path to the WoS ZIP file to process.")
    parser.add_argument("bcp_dir", help="Directory where BCP files should be generated.")

    args = parser.parse_args()

    if not os.path.isfile(args.zip_filepath):
        print(f"Error: ZIP file not found at {args.zip_filepath}")
        sys.exit(1)

    if not os.path.isdir(args.bcp_dir):
        try:
            os.makedirs(args.bcp_dir, exist_ok=True)
            print(f"BCP output directory {args.bcp_dir} created.")
        except OSError as e:
            print(f"Error: BCP directory {args.bcp_dir} does not exist and could not be created: {e}")
            sys.exit(1)

    print(f"Dispatching WoS ZIP processing task for: {args.zip_filepath}")
    print(f"BCP output will be in: {args.bcp_dir}")

    task_result = process_wos_zip_task.delay(
        zip_filepath=args.zip_filepath,
        bcp_dir=args.bcp_dir
    )

    print(f"Task dispatched successfully. Task ID: {task_result.id}")
    print("You can monitor the Celery worker logs for processing status.")
    print(f"To get results (if backend is configured and task returns a value): task_result.get(timeout=...)")
