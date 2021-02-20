from sqlalchemy.engine import create_engine

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
            f'mysql://{username}{db_pass}@{hostname}:{port}/{database}')

    @classmethod
    def can_handle(cls, context_type) -> bool:
        return context_type == 'mysql'

    def get_session_maker(self):
        """Returns a Session factory object for connecting to the database"""
        session_factory.configure(bind=self.engine)
        return session_factory