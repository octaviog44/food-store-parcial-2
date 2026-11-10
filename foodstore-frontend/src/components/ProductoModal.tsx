import { useEffect, useState } from 'react'
import type { Producto, ProductoCreate, UnidadMedida } from '../types'

interface ProductoModalProps {
  abierto: boolean
  producto: Producto | null
  unidades: UnidadMedida[]
  guardando: boolean
  errorApi: string | null
  onGuardar: (data: ProductoCreate) => void
  onCerrar: () => void
}

interface FormState {
  nombre: string
  descripcion: string
  precio_base: string
  unidad_venta_id: string
  stock_cantidad: string
  disponible: boolean
}

const FORM_VACIO: FormState = {
  nombre: '',
  descripcion: '',
  precio_base: '',
  unidad_venta_id: '',
  stock_cantidad: '0',
  disponible: true,
}

export function ProductoModal({
  abierto,
  producto,
  unidades,
  guardando,
  errorApi,
  onGuardar,
  onCerrar,
}: ProductoModalProps) {
  const [form, setForm] = useState<FormState>(FORM_VACIO)
  const [errorLocal, setErrorLocal] = useState<string | null>(null)

  useEffect(() => {
    if (!abierto) return
    if (producto) {
      setForm({
        nombre: producto.nombre,
        descripcion: producto.descripcion ?? '',
        precio_base: producto.precio_base,
        unidad_venta_id: String(producto.unidad_venta.id),
        stock_cantidad: producto.stock_cantidad,
        disponible: producto.disponible,
      })
    } else {
      setForm(FORM_VACIO)
    }
    setErrorLocal(null)
  }, [abierto, producto])

  if (!abierto) return null

  function actualizar<K extends keyof FormState>(campo: K, valor: FormState[K]) {
    setForm((prev) => ({ ...prev, [campo]: valor }))
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (form.nombre.trim().length < 3) {
      setErrorLocal('El nombre debe tener al menos 3 caracteres')
      return
    }
    if (!form.unidad_venta_id) {
      setErrorLocal('Tenés que elegir una unidad de venta')
      return
    }
    if (Number(form.precio_base) < 0 || Number.isNaN(Number(form.precio_base))) {
      setErrorLocal('El precio debe ser un número mayor o igual a 0')
      return
    }
    if (
      Number(form.stock_cantidad) < 0 ||
      Number.isNaN(Number(form.stock_cantidad))
    ) {
      setErrorLocal('El stock debe ser un número mayor o igual a 0')
      return
    }

    setErrorLocal(null)
    onGuardar({
      nombre: form.nombre.trim(),
      descripcion: form.descripcion.trim() || null,
      precio_base: Number(form.precio_base),
      unidad_venta_id: Number(form.unidad_venta_id),
      stock_cantidad: Number(form.stock_cantidad),
      disponible: form.disponible,
    })
  }

  const mensajeError = errorLocal ?? errorApi

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4">
      <div className="w-full max-w-lg rounded-lg bg-white shadow-xl">
        <div className="border-b border-slate-200 px-6 py-4">
          <h2 className="text-lg font-semibold text-slate-900">
            {producto ? 'Editar producto' : 'Nuevo producto'}
          </h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 px-6 py-4">
          {mensajeError && (
            <div className="rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700">
              {mensajeError}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700">
              Nombre *
            </label>
            <input
              type="text"
              value={form.nombre}
              onChange={(e) => actualizar('nombre', e.target.value)}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">
              Descripción
            </label>
            <textarea
              value={form.descripcion}
              onChange={(e) => actualizar('descripcion', e.target.value)}
              rows={2}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-slate-700">
                Precio base *
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={form.precio_base}
                onChange={(e) => actualizar('precio_base', e.target.value)}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">
                Stock *
              </label>
              <input
                type="number"
                step="0.001"
                min="0"
                value={form.stock_cantidad}
                onChange={(e) => actualizar('stock_cantidad', e.target.value)}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">
              Unidad de venta *
            </label>
            <select
              value={form.unidad_venta_id}
              onChange={(e) => actualizar('unidad_venta_id', e.target.value)}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
            >
              <option value="">Seleccioná una unidad</option>
              {unidades.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.nombre} ({u.simbolo}) — {u.tipo}
                </option>
              ))}
            </select>
          </div>

          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input
              type="checkbox"
              checked={form.disponible}
              onChange={(e) => actualizar('disponible', e.target.checked)}
              className="h-4 w-4 rounded border-slate-300"
            />
            Disponible para la venta
          </label>

          <div className="flex justify-end gap-2 border-t border-slate-200 pt-4">
            <button
              type="button"
              onClick={onCerrar}
              disabled={guardando}
              className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={guardando}
              className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
            >
              {guardando ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}