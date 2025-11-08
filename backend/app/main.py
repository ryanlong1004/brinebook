from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import recipes, search, photos, ratings, tags, auth

app = FastAPI(
    title="BrineBook API",
    description="AI-powered restaurant recipe vault",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(photos.router, prefix="/api/photos", tags=["photos"])
app.include_router(ratings.router, prefix="/api/ratings", tags=["ratings"])
app.include_router(tags.router, prefix="/api/tags", tags=["tags"])


@app.get("/")
async def root():
    return {"message": "BrineBook API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
