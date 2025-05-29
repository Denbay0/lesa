# src/main.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.main_api:app",  # импортное имя вашего FastAPI-приложения
        host="0.0.0.0",
        port=8000,
    )
