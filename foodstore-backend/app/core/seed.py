from sqlmodel import Session, select

from app.core.database import engine
from app.modules.unidades_medida.model import TipoUnidad, UnidadMedida

_UNIDADES_INICIALES = [
    {"nombre": "kilogramo", "simbolo": "kg", "tipo": TipoUnidad.peso},
    {"nombre": "gramo", "simbolo": "g", "tipo": TipoUnidad.peso},
    {"nombre": "litro", "simbolo": "L", "tipo": TipoUnidad.volumen},
    {"nombre": "mililitro", "simbolo": "mL", "tipo": TipoUnidad.volumen},
    {"nombre": "pieza", "simbolo": "u", "tipo": TipoUnidad.contable},
    {"nombre": "docena", "simbolo": "doc", "tipo": TipoUnidad.contable},
]


def seed_unidades_medida() -> None:
    """Inserta las unidades iniciales solo si la tabla está vacía."""
    with Session(engine) as session:
        ya_hay = session.exec(select(UnidadMedida)).first()
        if ya_hay is not None:
            return
        for datos in _UNIDADES_INICIALES:
            session.add(UnidadMedida(**datos))
        session.commit()