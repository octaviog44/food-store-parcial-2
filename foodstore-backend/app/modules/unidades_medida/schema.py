from sqlmodel import SQLModel

from app.modules.unidades_medida.model import TipoUnidad


class UnidadMedidaPublic(SQLModel):
    id: int
    nombre: str
    simbolo: str
    tipo: TipoUnidad