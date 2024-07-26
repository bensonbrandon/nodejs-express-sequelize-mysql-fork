from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers.tutorial_routes import router as tutorial_router
from app.models.tutorial import Tutorial  # Import the Tutorial model
from app.database import engine, Base  # Import the database engine and Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Register the tutorial routes
app.include_router(tutorial_router, prefix="/tutorials", tags=["tutorials"])

# Create the database tables
Base.metadata.create_all(bind=engine)
