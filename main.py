from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from config import SECRET_KEY
from routers import auth, files


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Lab6 File Manager", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth.router)
app.include_router(files.router)
