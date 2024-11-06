from fastapi import FastAPI
from . import models, database
from .routers import router as product_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.7:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(product_router, prefix="/api/v1")


# .\venv\Scripts\Activate

# .\venv\Scripts\uvicorn.exe app.main:app --reload
