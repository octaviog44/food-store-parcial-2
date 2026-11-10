from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import Field
from sqlmodel import SQLModel

from app.modules.categorias.schema import CategoriaPublic
from app.modules.unidades_medida.schema import UnidadMedidaPublic


class ProductoBase(SQLModel):
    nombre: Annotated[str, Field(min_length=3, max_length=100)]
    descripcion: str | None = Field(default=None, max_length=500)
    precio_base: Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]
    unidad_venta_id: int
    stock_cantidad: Annotated[
        Decimal, Field(ge=0, max_digits=10, decimal_places=3)
    ] = Decimal("0")
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoPublic(SQLModel):
    id: int
    nombre: str
    descripcion: str | None
    precio_base: Decimal
    stock_cantidad: Decimal
    disponible: bool
    activo: bool
    anulado_at: datetime | None
    unidad_venta: UnidadMedidaPublic
    categorias: list[CategoriaPublic]
    hay_stock: bool


class ProductoCategoriaCreate(SQLModel):
    categoria_id: int
    es_principal: bool = False


class ProductoCategoriaPublic(SQLModel):
    categoria_id: int
    nombre: str
    es_principal: bool