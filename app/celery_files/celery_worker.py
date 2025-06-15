from celery import Celery


celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.config_from_object("app.celery_files.celery_config")
