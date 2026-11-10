from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.core.seed import seed_unidades_medida
from app.modules.unidades_medida.router import router as unidades_router

import app.modules.unidades_medida.model  
import app.modules.categorias.model      
import app.modules.productos.model       


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_unidades_medida()
    yield


app = FastAPI(
    title="Food Store API",
    description="API REST para administrar el catálogo de productos de Food Store.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(unidades_router)


@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a Food Store API", "estado": "funcionando"}