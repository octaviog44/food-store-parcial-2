from fastapi import APIRouter, Depends, Path, Query, Response, status
from sqlmodel import Session

from app.core.database import get_session
from app.modules.categorias.schema import (
    CategoriaCreate,
    CategoriaPublic,
    CategoriaUpdate,
)
from app.modules.categorias import service

router = APIRouter(prefix="/api/v1/categorias", tags=["categorias"])


@router.post("", response_model=CategoriaPublic, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    data: CategoriaCreate,
    session: Session = Depends(get_session),
):
    return service.crear_categoria(session, data)


@router.get("", response_model=list[CategoriaPublic])
def listar_categorias(
    activo: bool | None = Query(None),
    search: str | None = Query(None),
    session: Session = Depends(get_session),
):
    return service.listar_categorias(session, activo=activo, search=search)


@router.get("/{categoria_id}", response_model=CategoriaPublic)
def obtener_categoria(
    categoria_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
):
    return service.obtener_categoria(session, categoria_id)


@router.put("/{categoria_id}", response_model=CategoriaPublic)
def actualizar_categoria(
    data: CategoriaUpdate,
    categoria_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
):
    return service.actualizar_categoria(session, categoria_id, data)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def anular_categoria(
    categoria_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
):
    service.anular_categoria(session, categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)