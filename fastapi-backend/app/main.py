from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers.tutorial.routes import router as tutorial_router  # Import the route
from app.database import Base, engine  # Import the database components

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(tutorial_router, prefix="/tutorials", tags=["tutorials"])  # Register the route
