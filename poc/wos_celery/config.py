# PoC Celery Configuration for WoS processing

# RabbitMQ Broker URL
# Replace with your actual RabbitMQ instance if different
# Format: amqp://user:password@host:port/vhost
# For a local RabbitMQ with default user/pass:
BROKER_URL = "amqp://guest:guest@localhost:5672//"

# Backend for storing task results (optional, can be RabbitMQ or Redis, or disabled)
# For this PoC, we'll use RabbitMQ as the result backend as well.
RESULT_BACKEND = "rpc://"

# Task settings
TASK_SERIALIZER = "json"
RESULT_SERIALIZER = "json"
ACCEPT_CONTENT = ["json"]
TIMEZONE = "UTC"
ENABLE_UTC = True

# Example: Define a queue for WoS tasks (optional, but good practice)
CELERY_QUEUES = {
    "wos_tasks": {"exchange": "wos_tasks", "binding_key": "wos_tasks"},
}
CELERY_DEFAULT_QUEUE = "wos_tasks"
