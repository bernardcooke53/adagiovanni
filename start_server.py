import os
from pathlib import Path

import uvicorn

SRC_DIR = Path(__file__).parent / "src"
os.chdir(SRC_DIR)

if __name__ == "__main__":
    uvicorn.run(
        "adagiovanni.main:app", host="0.0.0.0", port=8000, reload=True, workers=1
    )
