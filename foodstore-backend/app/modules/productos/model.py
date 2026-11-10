from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel

from app.modules.categorias.model import Categoria
from app.modules.productos.link_model import ProductoCategoria
from app.modules.unidades_medida.model import UnidadMedida


class Producto(SQLModel, table=True):
    __tablename__ = "producto"

    id: int | None = Field(default=None, primary_key=True)
    unidad_venta_id: int = Field(foreign_key="unidad_medida.id", nullable=False)
    nombre: str = Field(max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    precio_base: Decimal = Field(max_digits=10, decimal_places=2, ge=0)
    stock_cantidad: Decimal = Field(
        default=Decimal("0"), max_digits=10, decimal_places=3, ge=0
    )
    disponible: bool = Field(default=True, nullable=False)
    activo: bool = Field(default=True, nullable=False)
    anulado_at: datetime | None = Field(default=None, nullable=True)

    unidad_venta: UnidadMedida = Relationship(back_populates="productos")
    categorias: list[Categoria] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoria,
    )