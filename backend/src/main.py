from fastapi import FastAPI, HTTPException, Depends

from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from .router import router as mongo_router
app = FastAPI(debug=settings.DEBUG)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=mongo_router)

