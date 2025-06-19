from .celery_worker import celery_app
from app.database import SessionLocal
from app.models.notes_model import Notes
from app.models.user_model import User
from datetime import datetime, timedelta, timezone
from app.utils.emails_utils import send_reminder_email
from app.config.logger_config import func_logger

@celery_app.task
def check_and_notify_expiring_notes():
    func_logger.info(f"Check if note is expiring function started!!")
    
    db = SessionLocal()
    now = datetime.now(timezone.utc)
    reminder_window = now + timedelta(minutes=1)
    notes = db.query(Notes).filter(
        Notes.expires_at <= reminder_window,
        Notes.expires_at > now,
        Notes.is_expired == False
    ).all()
    
    for note in notes:
        user = db.query(User).filter(User.id == note.user_id).first()
        if user:
            func_logger.info(f"User Email: {user.email} Fetched!!")
            send_reminder_email(user.email, note.id)
    db.close()

@celery_app.task
def delete_expired_notes():
    db = SessionLocal()
    now = datetime.now(timezone.utc)
    
    expired_notes = db.query(Notes).filter(
        Notes.expires_at <= now,
        Notes.is_expired == False
    ).all()
    
    for note in expired_notes:
        db.delete(note)
    
    db.commit()
    db.close()