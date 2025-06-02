from fastapi import FastAPI
from server import models
from server.database import engine
from server.routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Club Server")

app.include_router(router)
