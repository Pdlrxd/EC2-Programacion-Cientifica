from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from sqlmodel import SQLModel, Session, create_engine

BASE_DIR = Path(__file__).parent
sqlite_url = f"sqlite:///{BASE_DIR / 'pokedex.db'}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables() -> None:
    """Crea todas las tablas en la base de datos."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Provee una sesión de base de datos como context manager."""
    with Session(engine) as session:
        yield session
