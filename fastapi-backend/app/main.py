from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import the router from the tutorial.routes module
from .routers.tutorial.routes import router as tutorial_router

# Import the Tutorial model from the models module
from .models.tutorial import Tutorial

# Import database configuration and initialization
from .database import engine, Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Register the tutorial router
app.include_router(tutorial_router, prefix="/tutorials", tags=["tutorials"])

# Create the database tables
Base.metadata.create_all(bind=engine)
