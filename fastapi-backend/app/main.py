from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import user
from app.database import engine
from app.models import Base
from app.routers import created_route_file  # Import the new route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(created_route_file.router)  # Register the new route
