from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.prefab import router as prefabs
from app.routers.auth import router as auth
from app.routers.user import router as users

app = FastAPI(title="Prefab Resource Hub API")

app.include_router(prefabs)
app.include_router(auth)
app.include_router(users)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
