from fastapi import FastAPI
from app.routers.prefab import router as prefabs

app = FastAPI(title="Prefab Resource Hub API")

app.include_router(prefabs)

@app.get("/")
async def index():
    return {
        "ServiceName": "Prefab API",
        "SourceCode": "https://github.com/Dyslex1k/SceneSearch"
    }

@app.get("/health")
async def get_service_health():
    return {
        "Health": "Healthy"
    }
