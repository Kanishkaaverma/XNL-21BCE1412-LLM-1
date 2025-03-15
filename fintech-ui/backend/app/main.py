from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, dashboard, trade, compliance
from .config import settings

app = FastAPI(title="FinTech LLM Dashboard API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(trade.router, prefix="/api/trade", tags=["trade"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["compliance"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FinTech LLM Dashboard API"}