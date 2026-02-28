#1. Importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio
from pydantic import BaseModel,Field

#2. Inicializacion APP
app= FastAPI(
    title="Mi primer API", 
    description="Jesus martinez",
    version="1.0.0"
    )

#BD ficticia
usuarios=[
    {"id":1, "nombre":"dianis", "edad":20},
    {"id":2, "nombre":"yahir", "edad":22},
    {"id":3, "nombre":"julian", "edad":22},
]

#Modelo de validacion Pydantic
class crear_usuario(BaseModel):
    id:int
    nombre:str
    edad:int

#3. Endpoints
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@app.get("/v1/bienvenidos", tags=['Bienvenidos'])
async def bien():
    return {"mensaje":'Bienvenidos'}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3) #peticion, consultaBD...
    return {"Calificacion":"7.5",
            "estatus":"200"
            }
    
@app.get("/v1/parametro0/{id}", tags=['Parametros'])
async def cosultaUno(id:int):
    await asyncio.sleep(3)
    return {"Resultado":"Usuario encontrado",
            "Estatus":"200",
            }

@app.get("/v1/parametro1/", tags=['Parametro opcional'])
async def cosultaOP(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Resultado":"Usuario encontrado"}
    else:
         return {"Aviso":"No se proporciono id"}
     
     
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def cosultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado correctamente",
        "status":"200",
        "usuario":usuario
    }
    
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario_actualizado.get("nombre", usr["nombre"])
            usr["edad"] = usuario_actualizado.get("edad", usr["edad"])
            
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usr
            }
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200",
                "usuario_eliminado": usr
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")