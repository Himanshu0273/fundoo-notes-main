from app.models import user_model

from ..database import Base, engine


class DbInitialize:

    # Function to load the DB
    @staticmethod
    def create_tables():
        Base.metadata.create_all(bind=engine)
