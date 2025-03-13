from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from .routes.linkedin_routes import router as linkedin_router


app = FastAPI(title="LinkedIn Insider API",
             description="API for scraping and analyzing LinkedIn company pages",
             version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  
)


app.include_router(linkedin_router, prefix="/api")


@app.get("/")
def home():
    return JSONResponse(content={"message": "Welcome to LinkedIn Insider API"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
