import uvicorn
from fastapi import FastAPI
from interface.api.routers import router as api_router
from data.env_loader import PORT

app = FastAPI(
    title="TodoList API",
    description="API for managing projects and tasks",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to TodoList API"}

if __name__ == "__main__":
    uvicorn.run("api_main:app", host="0.0.0.0", port=PORT, reload=True)
