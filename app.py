from fastapi import FastAPI
from codereviewai.api import router as review_router

app = FastAPI(title="Code Review AI")

app.include_router(review_router, tags=["Review Agent"])
