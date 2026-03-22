from fastapi import FastAPI
from routers.reports import router

app = FastAPI()
app.include_router(router)