from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session, select

from app.modules.categorias.model import Categoria
from app.modules.categorias.schema import (
    CategoriaCreate,
    CategoriaPublic,
    CategoriaUpdate,
)


def _categoria_a_public(categoria: Categoria) -> CategoriaPublic:
    return CategoriaPublic(
        id=categoria.id,
        nombre=categoria.nombre,
        descripcion=categoria.descripcion,
        activo=categoria.activo,
        anulado_at=categoria.anulado_at,
    )


def _validar_nombre_unico_activo(
    session: Session, nombre: str, excluir_id: int | None = None
) -> None:
    """RN-02: nombre único entre categorías activas."""
    query = select(Categoria).where(
        Categoria.nombre == nombre, Categoria.activo == True  # noqa: E712
    )
    if excluir_id is not None:
        query = query.where(Categoria.id != excluir_id)
    if session.exec(query).first() is not None:
        raise HTTPException(
            status_code=409, detail="Ya existe una categoría activa con ese nombre"
        )


def listar_categorias(
    session: Session,
    activo: bool | None = None,
    search: str | None = None,
) -> list[CategoriaPublic]:
    query = select(Categoria)

    if activo is None or activo is True:
        query = query.where(Categoria.activo == True)  # noqa: E712
    else:
        query = query.where(Categoria.activo == False)  # noqa: E712

    if search:
        query = query.where(Categoria.nombre.ilike(f"%{search}%"))  # type: ignore[attr-defined]

    categorias = session.exec(query.order_by(Categoria.id)).all()
    return [_categoria_a_public(c) for c in categorias]


def obtener_categoria(session: Session, categoria_id: int) -> CategoriaPublic:
    categoria = session.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return _categoria_a_public(categoria)


def crear_categoria(session: Session, data: CategoriaCreate) -> CategoriaPublic:
    _validar_nombre_unico_activo(session, data.nombre)
    categoria = Categoria(**data.model_dump())
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return _categoria_a_public(categoria)


def actualizar_categoria(
    session: Session, categoria_id: int, data: CategoriaUpdate
) -> CategoriaPublic:
    categoria = session.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if not categoria.activo:
        raise HTTPException(
            status_code=409, detail="No se puede modificar una categoría anulada"
        )

    _validar_nombre_unico_activo(session, data.nombre, excluir_id=categoria_id)

    categoria.nombre = data.nombre
    categoria.descripcion = data.descripcion
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return _categoria_a_public(categoria)


def anular_categoria(session: Session, categoria_id: int) -> None:
    categoria = session.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if not categoria.activo:
        raise HTTPException(status_code=409, detail="La categoría ya está anulada")

    categoria.activo = False
    categoria.anulado_at = datetime.now(timezone.utc)
    session.add(categoria)
    session.commit()