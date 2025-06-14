import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import dbsettings
from app.database import Base, get_db
from app.fapi import fapi
from app.models import user_model

DB_USER = dbsettings.DB_USER
DB_PASS = dbsettings.DB_PASSWORD
DB_HOST = dbsettings.DB_HOST
DB_PORT = dbsettings.DB_PORT
DB_NAME = dbsettings.TEST_DB_NAME


TEST_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    conn = engine.connect()
    transaction = conn.begin()

    db = TestingSessionLocal(bind=conn)
    try:
        yield db

    finally:
        transaction.rollback()
        conn.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    fapi.dependency_overrides[get_db] = override_get_db
    with TestClient(fapi) as c:
        yield c
