from fastapi import FastAPI
from app.routers.prefab import router as prefabs

app = FastAPI(title="Prefab Resource Hub API")

app.include_router(prefabs)
