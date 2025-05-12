import uvicorn
from app.main import make_app

if __name__ == "__main__":
    app = make_app()
    uvicorn.run(app, host="0.0.0.0", port=8002)
