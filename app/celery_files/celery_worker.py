from celery import Celery


celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["app.celery_files.tasks"]
)

celery_app.config_from_object("app.celery_files.celery_config")
celery_app.conf.timezone="UTC"