from fastapi import APIRouter, Depends, Path, Query, Response, status
from sqlmodel import Session

from app.core.database import get_session
from app.modules.productos.schema import (
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)
from app.modules.productos import service

router = APIRouter(prefix="/api/v1/productos", tags=["productos"])


@router.post("", response_model=ProductoPublic, status_code=status.HTTP_201_CREATED)
def crear_producto(
    data: ProductoCreate,
    session: Session = Depends(get_session),
):
    return service.crear_producto(session, data)


@router.get("", response_model=list[ProductoPublic])
def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    activo: bool | None = Query(None),
    disponible: bool | None = Query(None),
    categoria_id: int | None = Query(None),
    search: str | None = Query(None),
    session: Session = Depends(get_session),
):
    return service.listar_productos(
        session,
        skip=skip,
        limit=limit,
        activo=activo,
        disponible=disponible,
        categoria_id=categoria_id,
        search=search,
    )


@router.get("/{producto_id}", response_model=ProductoPublic)
def obtener_producto(
    producto_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
):
    return service.obtener_producto(session, producto_id)


@router.put("/{producto_id}", response_model=ProductoPublic)
def actualizar_producto(
    data: ProductoUpdate,
    producto_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
):
    return service.actualizar_producto(session, producto_id, data)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def anular_producto(
    producto_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
):
    service.anular_producto(session, producto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)