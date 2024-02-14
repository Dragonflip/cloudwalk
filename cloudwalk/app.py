from fastapi import FastAPI

from cloudwalk.routes import clients


app = FastAPI()

app.include_router(clients.router)


@app.get('/ping')
def read_root():
    return {'message': 'pong'}
