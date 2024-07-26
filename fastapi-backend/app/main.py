from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers.tutorial import router as tutorial_router  # Import the tutorial router
from app.models.tutorial import Tutorial  # Import the Tutorial model
from app.database import init_db  # Import the init_db function

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

# Initialize the database
init_db()
