from fastapi import FastAPI, Query, Body
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotel

app = FastAPI()

app.include_router(router_hotel)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
