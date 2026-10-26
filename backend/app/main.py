from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.brain.rules import default_rules


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    default_rules()  # invalid rules.yaml stops the app at startup, with a clear error
    yield


app = FastAPI(title="Statement Categorizer", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
