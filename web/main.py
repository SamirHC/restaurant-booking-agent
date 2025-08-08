from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from web.routes import router


app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")
app.include_router(router)
