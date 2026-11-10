from datetime import datetime
from typing import Annotated

from pydantic import Field
from sqlmodel import SQLModel


class CategoriaBase(SQLModel):
    nombre: Annotated[str, Field(min_length=3, max_length=100)]
    descripcion: str | None = Field(default=None, max_length=500)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaPublic(SQLModel):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
    anulado_at: datetime | None