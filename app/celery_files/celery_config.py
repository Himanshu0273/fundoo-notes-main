from celery.schedules import crontab

beat_schedule={
    "check-expiring-notes": {
        "task": "app.celery_files.tasks.check_and_notify_expiring_notes",
        "schedule": crontab(minute="*/1"),
    },
    "delete-expired-notes": {
        "task": "app.celery_files.tasks.delete_expired_notes",
        "schedule": crontab(minute="*/2"),
    },
    "refresh-redis-cache-every-10-mins": {
        "task": "app.utils.tasks.refresh_recent_notes_cache",
        "schedule": crontab(minute="*/10"),
    }
}