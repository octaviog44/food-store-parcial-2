import type { Producto } from '../types'

interface ProductoCardProps {
  producto: Producto
  onEditar: (producto: Producto) => void
  onCambiarDisponibilidad: (producto: Producto) => void
  onAnular: (producto: Producto) => void
}

function formatearPrecio(precio: string, simbolo: string): string {
  const numero = Number(precio)
  return `$ ${numero.toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })} / ${simbolo}`
}

function formatearStock(stock: string, simbolo: string): string {
  const numero = Number(stock)
  return `stock: ${numero.toLocaleString('es-AR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 3,
  })} ${simbolo}`
}

export function ProductoCard({
  producto,
  onEditar,
  onCambiarDisponibilidad,
  onAnular,
}: ProductoCardProps) {
  return (
    <article className="flex flex-col gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            {producto.nombre}
          </h2>
          {producto.descripcion && (
            <p className="text-sm text-slate-500">{producto.descripcion}</p>
          )}
        </div>
        <div className="flex flex-col items-end gap-1">
          <span
            className={`rounded-full px-2 py-0.5 text-xs font-medium ${
              producto.disponible
                ? 'bg-emerald-100 text-emerald-700'
                : 'bg-amber-100 text-amber-700'
            }`}
          >
            {producto.disponible ? 'Disponible' : 'Pausado'}
          </span>
          <span
            className={`rounded-full px-2 py-0.5 text-xs font-medium ${
              producto.hay_stock
                ? 'bg-sky-100 text-sky-700'
                : 'bg-rose-100 text-rose-700'
            }`}
          >
            {producto.hay_stock ? 'Con stock' : 'Sin stock'}
          </span>
        </div>
      </div>

      <dl className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <dt className="text-slate-500">Precio</dt>
          <dd className="font-medium text-slate-900">
            {formatearPrecio(
              producto.precio_base,
              producto.unidad_venta.simbolo,
            )}
          </dd>
        </div>
        <div>
          <dt className="text-slate-500">Stock</dt>
          <dd className="font-medium text-slate-900">
            {formatearStock(
              producto.stock_cantidad,
              producto.unidad_venta.simbolo,
            )}
          </dd>
        </div>
      </dl>

      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => onEditar(producto)}
          className="rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onCambiarDisponibilidad(producto)}
          className="rounded-md border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-100 disabled:opacity-50"
        >
          {producto.disponible ? 'Pausar' : 'Reanudar'}
        </button>
        <button
          type="button"
          onClick={() => onAnular(producto)}
          className="rounded-md border border-rose-300 px-3 py-1.5 text-sm font-medium text-rose-600 hover:bg-rose-50 disabled:opacity-50"
        >
          Anular
        </button>
      </div>
    </article>
  )
}