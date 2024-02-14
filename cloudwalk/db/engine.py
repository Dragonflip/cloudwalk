from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from cloudwalk.settings import Settings


engine = create_engine(Settings().DATABASE_URL)    # type: ignore


def get_session():
    with Session(engine) as session:
        return session
