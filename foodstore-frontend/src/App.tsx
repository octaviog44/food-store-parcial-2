import { useCallback, useEffect, useState } from 'react'
import { Navbar } from './components/Navbar'
import { ProductoList } from './components/ProductoList'
import { ProductoModal } from './components/ProductoModal'
import type {
  Producto,
  ProductoCreate,
  UnidadMedida,
} from './types'

const API_URL = 'http://127.0.0.1:8000/api/v1'

async function leerError(response: Response): Promise<string> {
  try {
    const data = (await response.json()) as { detail?: unknown }
    if (typeof data.detail === 'string') return data.detail
    if (Array.isArray(data.detail) && data.detail.length > 0) {
      const primero = data.detail[0] as { msg?: string }
      if (typeof primero.msg === 'string') return primero.msg
    }
  } catch {
    // si el body no es JSON, caemos al mensaje genérico
  }
  return `Error ${response.status}`
}

function App() {
  const [productos, setProductos] = useState<Producto[]>([])
  const [unidades, setUnidades] = useState<UnidadMedida[]>([])
  const [cargando, setCargando] = useState<boolean>(true)
  const [errorListado, setErrorListado] = useState<string | null>(null)

  const [modalAbierto, setModalAbierto] = useState<boolean>(false)
  const [productoSeleccionado, setProductoSeleccionado] =
    useState<Producto | null>(null)
  const [guardando, setGuardando] = useState<boolean>(false)
  const [errorModal, setErrorModal] = useState<string | null>(null)

  const cargarProductos = useCallback(async () => {
    setCargando(true)
    setErrorListado(null)
    try {
      const response = await fetch(`${API_URL}/productos?limit=50`)
      if (!response.ok) throw new Error(await leerError(response))
      const data = (await response.json()) as Producto[]
      setProductos(data)
    } catch (e) {
      setErrorListado(e instanceof Error ? e.message : 'Error al cargar')
    } finally {
      setCargando(false)
    }
  }, [])

  const cargarUnidades = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/unidades-medida`)
      if (!response.ok) throw new Error(await leerError(response))
      const data = (await response.json()) as UnidadMedida[]
      setUnidades(data)
    } catch (e) {
      setErrorListado(e instanceof Error ? e.message : 'Error al cargar unidades')
    }
  }, [])

  useEffect(() => {
    void cargarProductos()
    void cargarUnidades()
  }, [cargarProductos, cargarUnidades])

  function abrirCrear() {
    setProductoSeleccionado(null)
    setErrorModal(null)
    setModalAbierto(true)
  }

  function abrirEditar(producto: Producto) {
    setProductoSeleccionado(producto)
    setErrorModal(null)
    setModalAbierto(true)
  }

  function cerrarModal() {
    setModalAbierto(false)
    setProductoSeleccionado(null)
    setErrorModal(null)
  }

  async function guardarProducto(data: ProductoCreate) {
    setGuardando(true)
    setErrorModal(null)
    try {
      const editando = productoSeleccionado !== null
      const url = editando
        ? `${API_URL}/productos/${productoSeleccionado.id}`
        : `${API_URL}/productos`
      const method = editando ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        const mensaje = await leerError(response)
        setErrorModal(mensaje)
        return
      }

      await cargarProductos()
      cerrarModal()
    } catch (e) {
      setErrorModal(e instanceof Error ? e.message : 'Error al guardar')
    } finally {
      setGuardando(false)
    }
  }

  async function cambiarDisponibilidad(producto: Producto) {
    const body: ProductoCreate = {
      nombre: producto.nombre,
      descripcion: producto.descripcion,
      precio_base: Number(producto.precio_base),
      unidad_venta_id: producto.unidad_venta.id,
      stock_cantidad: Number(producto.stock_cantidad),
      disponible: !producto.disponible,
    }
    const response = await fetch(`${API_URL}/productos/${producto.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!response.ok) {
      const mensaje = await leerError(response)
      setErrorListado(mensaje)
      return
    }
    await cargarProductos()
  }

  async function anularProducto(producto: Producto) {
    if (!window.confirm(`¿Anular "${producto.nombre}"?`)) return
    const response = await fetch(`${API_URL}/productos/${producto.id}`, {
      method: 'DELETE',
    })
    if (!response.ok && response.status !== 204) {
      const mensaje = await leerError(response)
      setErrorListado(mensaje)
      return
    }
    await cargarProductos()
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <Navbar titulo="Food Store — Catálogo" />

      <main className="mx-auto max-w-6xl px-4 py-6">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-800">
            Productos del catálogo
          </h2>
          <button
            type="button"
            onClick={abrirCrear}
            className="rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700 disabled:opacity-50"
          >
            + Nuevo producto
          </button>
        </div>

        {errorListado && (
          <div className="mb-4 rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700">
            {errorListado}
          </div>
        )}

        {cargando ? (
          <p className="py-12 text-center text-slate-500">Cargando productos...</p>
        ) : productos.length === 0 ? (
          <p className="py-12 text-center text-slate-500">
            Todavía no hay productos cargados.
          </p>
        ) : (
          <ProductoList
            productos={productos}
            onEditar={abrirEditar}
            onCambiarDisponibilidad={(p) => void cambiarDisponibilidad(p)}
            onAnular={(p) => void anularProducto(p)}
          />
        )}
      </main>

      <ProductoModal
        abierto={modalAbierto}
        producto={productoSeleccionado}
        unidades={unidades}
        guardando={guardando}
        errorApi={errorModal}
        onGuardar={(data) => void guardarProducto(data)}
        onCerrar={cerrarModal}
      />
    </div>
  )
}

export default App