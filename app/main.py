from fastapi import FastAPI
from . import models, database
from .routers import router as product_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import uvicorn

app = FastAPI()

# Mount the Frontend folder to serve static files
app.mount("/static", StaticFiles(directory="Frontend"), name="static")

# Serve the main HTML file at the root
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

load_dotenv()

Port = int(os.get('PORT',8000))
Host = '0.0.0.0'

if __name__ == '__main__':
    uvicorn.run('app.main:app' , host = Host ,port = Port ,reload = True)

