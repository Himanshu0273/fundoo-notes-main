from celery.schedules import crontab

beat_schedule={
    "check-expiring-notes": {
        "task": "app.celery_files.tasks.check_and_notify_expiring_notes",
        "schedule": crontab(hour=0, minute=0),
    },
    "delete-expired-notes": {
        "task": "app.celery_files.tasks.delete_expired_notes",
        "schedule": crontab(hour=1, minute=0),
    }
}