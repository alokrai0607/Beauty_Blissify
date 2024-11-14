from fastapi import FastAPI
from . import models, database
from .routers import router as product_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def read_root():
    return FileResponse("Frontend/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)
app.include_router(product_router, prefix="/api/v1")

# .\venv\Scripts\Activate

# .\venv\Scripts\uvicorn.exe app.main:app --reload

#  pytest

# Rebuild the Docker Image
# docker build --no-cache -t fastapi-app .

# run the container normally:
# docker run -d -p 8000:8000 fastapi-app

# for stop container 
# docker stop 32c741b4270e
