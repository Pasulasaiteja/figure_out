"""
Transformers - AI-Driven Fitness & Wellness Platform
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, users, health_assessment, workout, nutrition, progress, chat, calendar, achievements

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transformers API",
    description="AI-Driven Fitness & Wellness Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(health_assessment.router, prefix="/api/assessment", tags=["Health Assessment"])
app.include_router(workout.router, prefix="/api/workout", tags=["Workout"])
app.include_router(nutrition.router, prefix="/api/nutrition", tags=["Nutrition"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Coach"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(achievements.router, prefix="/api/achievements", tags=["Achievements"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Transformers - AI-Driven Fitness Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "transformers-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
