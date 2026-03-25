from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import settings
from api.auth.rout import router as ro

app = FastAPI()
app.include_router(router=ro, tags=["Jwt"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.server.allow_origins,
    allow_credentials=settings.server.allow_credentails,
    allow_methods=settings.server.allow_methods,
    allow_headers=settings.server.allow_headers,
)


if __name__ == "__main__":
    import uvicorn as uvi
    uvi.run("app:app", host=settings.server.host, port=settings.server.port, reload=settings.server.reload)