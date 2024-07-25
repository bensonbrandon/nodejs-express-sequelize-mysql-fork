from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import user
from .database import engine
from .models import Base
from .routers import {{ created_route_file }}  # Import the new route

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

# app.include_router(user.router) # routers are added during Migration of API endpoints
app.include_router({{ created_route_file }}.router)  # Include the new router
