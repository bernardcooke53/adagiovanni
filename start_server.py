import os
from pathlib import Path

import uvicorn

SRC_DIR = Path(__file__).parent / "src"
os.chdir(SRC_DIR)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"


def serve() -> None:
    uvicorn.run(
        "adagiovanni.main:app",
        host="0.0.0.0",
        port=8000,
        factory=True,
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    serve()
