# Food Store — Frontend

Interfaz web de administración del catálogo de productos de Food Store, construida con **React**, **TypeScript**, **Vite** y **Tailwind CSS 4**.

## Requisitos

- Node.js 18 o superior
- npm 9 o superior
- El backend de Food Store corriendo en `http://127.0.0.1:8000`

## Instalación

```powershell
npm install
```

## Ejecución

```powershell
npm run dev
```

- Aplicación: http://localhost:5173

La aplicación consume la API del backend en `http://127.0.0.1:8000/api/v1`. Si el backend no está corriendo, la interfaz muestra un mensaje de error.

## Estructura

```
src/
├── components/
│   ├── Navbar.tsx
│   ├── ProductoList.tsx
│   ├── ProductoCard.tsx
│   └── ProductoModal.tsx
├── types/
│   ├── categoria.ts
│   ├── producto.ts
│   ├── unidadMedida.ts
│   └── index.ts
├── App.tsx              
├── main.tsx
└── index.css             
```

## Funcionalidad

- Listado de productos con precio y stock formateados con el símbolo de su unidad.
- Indicadores visuales de `disponible` y `hay_stock`.
- Alta y edición mediante un modal con selector de unidad cargado desde la API.
- Cambio de disponibilidad (pausar / reanudar) y anulación lógica.
- Manejo de errores: un 409 del backend se muestra dentro del modal sin cerrarlo.
- Estados de carga, error y lista vacía.