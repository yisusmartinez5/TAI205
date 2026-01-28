#1. importaciones
from fastapi import FastAPI

#2. Inicializacion APP
app= FastAPI()

#3. Endpoints
@app.get("/")
async def holaMundo():
    return{"mensaje":"hola mundo FastAPI"}

@app.get("/bienvenidos")
async def bienvenidos():
    return{"mensaje":"bienvenidos"}