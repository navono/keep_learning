from .server import app


@app.get("/")
async def home():
    return {'message': 'Hello, FastAPI!'}
