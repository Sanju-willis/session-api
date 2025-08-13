# src\main.py
import os
from .app import create_app

# Set debug mode
os.environ["DEBUG"] = "true"

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)