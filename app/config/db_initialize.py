from app.database import Base, engine


class DbInitialize:
    @staticmethod
    def create_tables():
        from app.models import user_model  
        Base.metadata.create_all(bind=engine)
