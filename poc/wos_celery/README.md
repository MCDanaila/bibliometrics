# Web of Science (WoS) Celery PoC - README

This directory contains a Proof-of-Concept (PoC) implementation for processing Web of Science data using Celery distributed task queues.

## Prerequisites

1.  **Python Environment**: Ensure you have a Python environment with `celery` and `librabbitmq` installed. These should be in your main `requirements.txt` if you followed the setup.
    ```bash
    pip install -r ../../requirements.txt
    # or specifically:
    # pip install celery[librabbitmq]
    ```

2.  **RabbitMQ Broker**: This PoC is configured to use a RabbitMQ broker running locally with default guest credentials.
    *   **URL**: `amqp://guest:guest@localhost:5672//` (as defined in `config.py`).
    *   Ensure RabbitMQ server is installed and running. If using Docker, you can run:
        ```bash
        docker run -d -p 5672:5672 -p 15672:15672 --name rabbitmq_poc rabbitmq:3-management
        ```
        The port `15672` is for the RabbitMQ management interface, accessible at `http://localhost:15672`.

## Running the PoC

### 1. Start the Celery Worker

Open a terminal, navigate to the root directory of this repository (the one containing the `poc` directory), and run the following command to start a Celery worker:

```bash
celery -A poc.wos_celery.celery_app worker -l info -Q wos_tasks
```

Explanation:
*   `-A poc.wos_celery.celery_app`: Specifies the Celery application instance.
*   `worker`: Command to start a worker.
*   `-l info`: Sets the logging level to INFO.
*   `-Q wos_tasks`: (Optional, but good practice) Makes this worker consume tasks only from the `wos_tasks` queue, as defined in `config.py`.

You should see the worker start up and display messages indicating it's connected to the broker and ready to receive tasks. It will list the registered tasks, including `poc.wos_celery.tasks.process_wos_file_placeholder` and `poc.wos_celery.tasks.example_task_add`.

### 2. Dispatch a Test Task

Open another terminal (or a Python interpreter) from the root directory of the repository.

Create a small Python script (e.g., `run_test_task.py` in the root or `poc/wos_celery/` directory) with the following content:

```python
from poc.wos_celery.tasks import process_wos_file_placeholder, example_task_add

if __name__ == "__main__":
    print("Dispatching placeholder WoS file processing task...")
    # Send the placeholder task
    result_placeholder = process_wos_file_placeholder.delay(
        filepath="/path/to/dummy/wos_file.xml",
        bcp_dir="/tmp/poc_bcp_output"
    )
    print(f"Placeholder task dispatched. Task ID: {result_placeholder.id}")

    print("\nDispatching example addition task...")
    # Send the example addition task
    result_add = example_task_add.delay(5, 7)
    print(f"Example task dispatched. Task ID: {result_add.id}")

    # You can optionally wait for results if needed (requires result backend to be fully configured and accessible)
    # print(f"Result of addition: {result_add.get(timeout=10)}")
    # print(f"Result of placeholder: {result_placeholder.get(timeout=30)}") # Placeholder task takes ~10s
```

Run this script:
```bash
python path/to/your/run_test_task.py
```
(Adjust path to where you saved `run_test_task.py`)


### 3. Observe Output

*   **In the Celery Worker Terminal**: You should see log messages indicating that the worker received and executed the tasks (e.g., `process_wos_file_placeholder` and `example_task_add`). The placeholder task will print messages about processing and then succeeding.
*   **In the `run_test_task.py` Terminal**: You will see the task IDs printed when the tasks are dispatched. If you uncomment the `.get()` lines, it will wait for and print the results.

## Next Steps / Full Implementation Ideas

*   **Real File Processing**: Replace the `time.sleep(10)` in `process_wos_file_placeholder` with actual WoS XML parsing logic (potentially reusing/adapting code from `libbiblio/sources/wos/wos_parser.py`).
*   **BCP Generation**: Implement logic to generate BCP files from the parsed data.
*   **Error Handling**: Enhance error handling within the task.
*   **Database Interaction**: The task might need to interact with `BibliometricsFileStatus` (e.g., to get the next file or update status). This would require careful consideration of database connection management within tasks.
*   **Dynamic Task Dispatch**: The main pipeline script (`controller/process.sh` or its Python equivalent) would be modified to dispatch tasks to Celery instead of running `ingest_data.py` directly.
*   **Configuration**: Make broker URLs, queue names, etc., more configurable (e.g., via environment variables or a central config file loaded by `poc.wos_celery.config`).

This PoC provides the basic scaffolding for a Celery-based distributed task processing system.
