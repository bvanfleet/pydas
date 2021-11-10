from contextlib import contextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from pydas_metadata.contexts.base import BaseContext, session_factory


class DatabaseContext(BaseContext):
    """Database connection context, handles database session setup and object insertion"""

    def __init__(self,
                 database: str,
                 username: str,
                 password: str = None,
                 hostname: str = 'localhost',
                 port: int = 3306):
        db_pass = f':{password}' if password is not None else ''
        self.engine = create_engine(
            f'mariadb+mariadbconnector://{username}{db_pass}@{hostname}:{port}/{database}')
        session_factory.configure(bind=self.engine)

    @classmethod
    def can_handle(cls, context_type) -> bool:
        return context_type == 'mariadb'

    @contextmanager
    def get_session(self):
        """Returns a Session factory object for connecting to the database"""
        try:
            session: Session = session_factory()
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
