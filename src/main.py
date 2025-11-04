from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from .core.config import settings
print("🔧 [IMPORT] Settings imported")
from .api.endpoints import orchestration
print("🔧 [IMPORT] Orchestration imported")
from .orchestration.prism_orchestrator import PrismOrchestrator

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작 시 Orchestrator를 초기화하고, 종료 시 정리합니다."""
    print("🚀 [STARTUP] Initializing Orchestrator at application startup...")
    try:
        orchestration.orchestrator = PrismOrchestrator()
        print("✅ [STARTUP] Orchestrator initialized successfully")
    except Exception as e:
        print(f"❌ [STARTUP] Failed to initialize orchestrator: {str(e)}")
        raise

    yield

    print("🛑 [SHUTDOWN] Cleaning up resources...")

app = FastAPI(
    title="PRISM Orchestration",
    description="자율 제조 구현을 위한 AI 에이전트 오케스트레이션 모듈",
    version="1.0",
    lifespan=lifespan
)

# Routers
app.include_router(orchestration.router, prefix="/api/v1/orchestrate", tags=["Orchestration"])
print("🔧 [IMPORT] Orchestration router included")


@app.get("/", tags=["Health Check"])
async def read_root():
    return {"status": "ok", "message": "Welcome to PRISM-Orch!"}

@app.post("/test", tags=["Debug"])
def test_post():  # Make it sync instead of async
    print("🚀 [DEBUG] Simple POST request received (SYNC)")
    return {"status": "ok", "message": "POST test successful", "type": "sync"}

@app.post("/test-body", tags=["Debug"])
async def test_post_with_body(data: dict):
    print(f"🚀 [DEBUG] POST with body received: {data}")
    return {"status": "ok", "received": data}

from src.api.schemas import UserQueryInput
from fastapi import Body

@app.post("/test-schema", tags=["Debug"])
async def test_post_with_schema(query: UserQueryInput = Body(...)):
    print(f"🚀 [DEBUG] POST with UserQueryInput received: {query}")
    return {"status": "ok", "received": query.dict()}


if __name__ == "__main__":
    # Test with different ASGI server
    import sys
    if "--hypercorn" in sys.argv:
        import hypercorn.asyncio
        import hypercorn.config
        config = hypercorn.config.Config()
        config.bind = [f"{settings.APP_HOST}:{settings.APP_PORT}"]
        hypercorn.asyncio.serve(app, config)
    else:
        print(f"🔧 Starting uvicorn on {settings.APP_HOST}:{settings.APP_PORT}")
        uvicorn.run(
            "src.main:app",
            host=settings.APP_HOST,
            port=settings.APP_PORT,
            reload=False,
            workers=1,
            access_log=True,
            log_level="debug"  # Enable debug logging
        ) 