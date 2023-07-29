from sqlalchemy import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


def create_session(
    username: str, password: str, host: str, port: int, database: str
) -> Session:
    """
    Create a session to a MySQL database.

    Parameters
    ----------
    username : str
        Username to connect to the database.
    password : str
        Password to connect to the database.
    host : str
        Hostname of the database.
    port : int
        Port of the database.
    database : str
        Name of the database.

    Returns
    -------
    Session
        SQLAlchemy session to the database.
    """
    engine = create_engine(
        URL.create(
            drivername="mysql+pymysql",
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            query={"charset": "utf8mb4"},
        )
    )
    Base = declarative_base()
    Base.metadata.create_all(engine)
    return Session(engine)
