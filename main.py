from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.database import create_tables, engine
from app.api.router import router as schedule_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(schedule_router)