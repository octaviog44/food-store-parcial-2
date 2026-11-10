# Food Store — Backend

API REST del catálogo de productos de Food Store, construida con **FastAPI**, **SQLModel**, **Pydantic v2** y **PostgreSQL**.

## Requisitos

- Python 3.12 o superior
- PostgreSQL 15 o superior

## Instalación

1. Crear y activar un entorno virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación, ejecutar antes:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

2. Instalar dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Configurar la base de datos:

   - Crear una base en PostgreSQL llamada `foodstore_parcial2`.
   - Copiar `.env.example` a `.env` y completar la contraseña del usuario de PostgreSQL:

     ```
     DATABASE_URL=postgresql+psycopg://postgres:TU_CONTRASEÑA@localhost:5432/foodstore_parcial2
     ```

## Ejecución

```powershell
fastapi dev app/main.py
```

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

Al arrancar, la aplicación crea las tablas si no existen y ejecuta el seed de unidades de medida (solo si la tabla está vacía).

## Estructura

```
app/
├── main.py
├── core/
│   ├── database.py      # engine + get_session
│   └── seed.py          # seed idempotente de unidades de medida
└── modules/
    ├── unidades_medida/ # model, schema, router (solo lectura)
    ├── categorias/      # model, schema, service, router
    └── productos/       # model, link_model, schema, service, router
tests/
├── productos.http
└── relaciones.http
```

## Pruebas HTTP

Cada archivo `.http` de `tests/` está pensado para correrse sobre una base limpia. Antes de ejecutar `productos.http` o `relaciones.http`, ejecutar en PostgreSQL:

```sql
TRUNCATE TABLE producto_categoria, producto, categoria RESTART IDENTITY CASCADE;
```

Luego abrir el archivo en VS Code con la extensión **REST Client** y ejecutar los bloques en orden.