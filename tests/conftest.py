import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from cloudwalk.db.engine import get_session
from cloudwalk.db.models import Base, Client
from cloudwalk.app import app


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    with Session() as session:
        yield session
        session.rollback()

    Base.metadata.drop_all(engine)


@pytest.fixture
def approved_client(session):
    client = Client(
        status='approved', batch=1, credit_limit=20000, interest_rate=20
    )
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@pytest.fixture
def test_client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()
