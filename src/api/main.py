from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1 import router_v1
from src.db.database import engine
from src.db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on service start-up
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title='Idoven ECG API',
              description='Backend challenge for Idoven',
              version='1.0',
              lifespan=lifespan)

app.include_router(router_v1)
