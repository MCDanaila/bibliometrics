from celery import Celery

# Import configuration from config.py
# Assuming config.py is in the same directory
from . import config

# Create a Celery application instance
# The first argument is the name of the current module, important for task auto-discovery
# The second argument 'broker' specifies the broker URL
# The third argument 'backend' specifies the result backend URL
# 'include' is a list of modules to import when a worker starts, so tasks are registered
app = Celery(
    "wos_celery_poc",
    broker=config.BROKER_URL,
    backend=config.RESULT_BACKEND,
    include=["poc.wos_celery.tasks"],
)

# Load configuration from the config object (config.py)
# All celery configuration options can be set here, prefixed with CELERY_
app.config_from_object(config)

# Optional: Set a default queue if not already in config
if not hasattr(config, "CELERY_DEFAULT_QUEUE"):
    app.conf.task_default_queue = "default"

# Optional: Autodiscover tasks in modules listed in 'include' and also in 'tasks.py'
# This is often default behavior but can be made explicit.
# app.autodiscover_tasks()

if __name__ == "__main__":
    # This part is for direct execution of the celery app,
    # e.g., for command-line utilities, but workers are usually started
    # using 'celery -A poc.wos_celery.celery_app worker -l info'
    app.start()
