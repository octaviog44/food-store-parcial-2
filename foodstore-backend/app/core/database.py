import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "Falta la variable DATABASE_URL. Copiá .env.example a .env y configurala."
    )

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    """Crea las tablas si no existen. Se llama al arrancar la app."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependencia de FastAPI: entrega una Session por request."""
    with Session(engine) as session:
        yield session