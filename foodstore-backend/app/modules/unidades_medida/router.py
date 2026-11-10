from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.modules.unidades_medida.model import UnidadMedida
from app.modules.unidades_medida.schema import UnidadMedidaPublic

router = APIRouter(prefix="/api/v1/unidades-medida", tags=["unidades-medida"])


@router.get("", response_model=list[UnidadMedidaPublic])
def listar_unidades(session: Session = Depends(get_session)):
    return session.exec(select(UnidadMedida).order_by(UnidadMedida.id)).all()