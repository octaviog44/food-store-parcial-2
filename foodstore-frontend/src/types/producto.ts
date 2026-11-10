import type { Categoria } from './categoria'
import type { UnidadMedida } from './unidadMedida'

export interface Producto {
  id: number
  nombre: string
  descripcion: string | null
  precio_base: string
  stock_cantidad: string
  disponible: boolean
  activo: boolean
  anulado_at: string | null
  unidad_venta: UnidadMedida
  categorias: Categoria[]
  hay_stock: boolean
}

export interface ProductoCreate {
  nombre: string
  descripcion: string | null
  precio_base: number
  unidad_venta_id: number
  stock_cantidad: number
  disponible: boolean
}

export type ProductoUpdate = ProductoCreate