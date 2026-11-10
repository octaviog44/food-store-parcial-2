from decimal import Decimal

from fastapi import HTTPException
from sqlmodel import Session, select

from app.modules.productos.model import Producto
from app.modules.productos.schema import (
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)
from app.modules.unidades_medida.model import TipoUnidad, UnidadMedida




def _validar_unidad_existe(session: Session, unidad_id: int) -> UnidadMedida:
    """RN-03: la unidad de venta referenciada debe existir."""
    unidad = session.get(UnidadMedida, unidad_id)
    if unidad is None:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    return unidad


def _validar_nombre_unico_activo(
    session: Session, nombre: str, excluir_id: int | None = None
) -> None:
    """RN-02: nombre único entre productos activos."""
    query = select(Producto).where(
        Producto.nombre == nombre, Producto.activo == True  # noqa: E712
    )
    if excluir_id is not None:
        query = query.where(Producto.id != excluir_id)
    existente = session.exec(query).first()
    if existente is not None:
        raise HTTPException(
            status_code=409, detail="Ya existe un producto activo con ese nombre"
        )


def _validar_stock_entero_si_contable(
    unidad: UnidadMedida, stock: Decimal
) -> None:
    """RN-10: si la unidad es contable, stock debe ser entero."""
    if unidad.tipo == TipoUnidad.contable and stock != stock.to_integral_value():
        raise HTTPException(
            status_code=422,
            detail="El stock debe ser un número entero para unidades contables",
        )




def _producto_a_public(producto: Producto) -> ProductoPublic:
    """Arma el schema de respuesta e inyecta hay_stock (RN-11)."""
    return ProductoPublic(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio_base=producto.precio_base,
        stock_cantidad=producto.stock_cantidad,
        disponible=producto.disponible,
        activo=producto.activo,
        anulado_at=producto.anulado_at,
        unidad_venta=producto.unidad_venta,
        categorias=producto.categorias,
        hay_stock=producto.stock_cantidad > 0,
    )




def listar_productos(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    activo: bool | None = None,
    disponible: bool | None = None,
    categoria_id: int | None = None,
    search: str | None = None,
) -> list[ProductoPublic]:
    query = select(Producto)

    
    if activo is None or activo is True:
        query = query.where(Producto.activo == True)  # noqa: E712
    else:
        query = query.where(Producto.activo == False)  # noqa: E712

    if disponible is not None:
        query = query.where(Producto.disponible == disponible)

    if categoria_id is not None:
        from app.modules.productos.link_model import ProductoCategoria

        query = query.join(
            ProductoCategoria,
            ProductoCategoria.producto_id == Producto.id,  
        ).where(ProductoCategoria.categoria_id == categoria_id)

    if search:
        query = query.where(Producto.nombre.ilike(f"%{search}%"))  

    query = query.offset(skip).limit(limit)
    productos = session.exec(query).all()
    return [_producto_a_public(p) for p in productos]


def obtener_producto(session: Session, producto_id: int) -> ProductoPublic:
    producto = session.get(Producto, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return _producto_a_public(producto)


def crear_producto(session: Session, data: ProductoCreate) -> ProductoPublic:
    unidad = _validar_unidad_existe(session, data.unidad_venta_id)
    _validar_nombre_unico_activo(session, data.nombre)
    _validar_stock_entero_si_contable(unidad, data.stock_cantidad)

    producto = Producto(**data.model_dump())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return _producto_a_public(producto)


def actualizar_producto(
    session: Session, producto_id: int, data: ProductoUpdate
) -> ProductoPublic:
    producto = session.get(Producto, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if not producto.activo:
        raise HTTPException(
            status_code=409, detail="No se puede modificar un producto anulado"
        )

    unidad = _validar_unidad_existe(session, data.unidad_venta_id)
    _validar_nombre_unico_activo(session, data.nombre, excluir_id=producto_id)
    _validar_stock_entero_si_contable(unidad, data.stock_cantidad)

    for campo, valor in data.model_dump().items():
        setattr(producto, campo, valor)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return _producto_a_public(producto)


def anular_producto(session: Session, producto_id: int) -> None:
    producto = session.get(Producto, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if not producto.activo:
        raise HTTPException(
            status_code=409, detail="El producto ya está anulado"
        )

    from datetime import datetime, timezone

    producto.activo = False
    producto.anulado_at = datetime.now(timezone.utc)
    session.add(producto)
    session.commit()