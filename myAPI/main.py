#1. importaciones
from fastapi import FastAPI
from typing import Optional
import asyncio 

#2. Inicializacion APP
app= FastAPI(
    title='Mi primer API',
    description='Jesus Martinez',
    version='1.0.0'
    )

#Base de datos ficticia 
usuarios=[
    {"id":"1", "nombre":"Jesus", "apellido":"Martinez", "edad":23},
    {"id":"2", "nombre":"Ana", "apellido":"Lopez", "edad":30},
    {"id":"3", "nombre":"Luis", "apellido":"Garcia", "edad":28},]

#3. Endpoints
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return{"mensaje":"hola mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenidos():
    return{"mensaje":"bienvenidos"}

@app.get("/v1/promedio", tags=['calificaciones'])
async def promedio():
    await asyncio.sleep(3) #peticion, consulta BD
    return{
        "calificación":"7.5",
        "status":"200"
           }

@app.get("/v1/usuario/{id}", tags=['Parametros'])
async def consultaUno(id: int):
    await asyncio.sleep(3)
    return{
        "Resultado":"Usuario encontrado",
        "Estatus":"200"
        }

@app.get("/v1/usuarios_op/", tags=['Parametros opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id, "Datos":usuarios }
        return { "Mensaje":"usuario no encontrado" }
    else:
        return { "Aviso":"No se proporciono Id" }


