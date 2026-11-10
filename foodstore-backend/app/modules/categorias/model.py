from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.modules.productos.link_model import ProductoCategoria

if TYPE_CHECKING:
    from app.modules.productos.model import Producto


class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    activo: bool = Field(default=True, nullable=False)
    anulado_at: datetime | None = Field(default=None, nullable=True)

    productos: list["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria,
    )