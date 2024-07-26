from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import the Tutorial model
from app.models.tutorial import Tutorial

# Import the router from tutorial.routes
from app.routers.tutorial.routes import router as tutorial_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the tutorial router
app.include_router(tutorial_router)
