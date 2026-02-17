#1.-importacioones
from fastapi import FastAPI,status,HTTPException 
from typing import Optional
import asyncio

#2. Inicializacion APP
app= FastAPI(
    title='Mi primer API',
    description="Gael Jesus Martinez Garcia",
    version='1.0.0')
#BD ficticia
usuarios=[
    {"id":"1","nombre:":"Diana", "edad":"20"},
    {"id":"1","nombre:":"Gael", "edad":"21"},
    {"id":"1","nombre:":"Ivan", "edad":"38"},
]


#3. Endpoints
@app.get("/", tags=['Inicio'])
async def bien():
    return{"mensaje":"Bienvenido"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenidos():
    return{"mensaje":"bienvenidos"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3) #peticion, consultaBD
    return{"Calificacion":"7.5",
           "estatus":"200"
           }
@app.get("/v1/usuario/{id}", tags=['Parametro'])
async def consultauno(id:int):
    await asyncio.sleep(3) #peticion, consultaBD
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200",
        }

@app.get("/v1/parametroO/", tags=['Parametros opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id, "Datos":usuarios }
        return { "Mensaje":"usuario no encontrado" }
    else:
        return { "Aviso":"No se proporciono Id" }

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def crea_usuario(usuario:dict):
    for usr in usuarios: 
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                datail="El ID ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje": "usuario agregado correctamente",
        "status":"200",
        "usuario":usuario
    }
 
@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def elimina_usuario(id: int):
    for pos, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(pos)
            return {
                "mensaje": "Usuario eliminado",
                "status": "200",
                "usuario": eliminado
            }

    raise HTTPException(
        status_code=404, 
        detail="No se encontro el usuario"
        )

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for pos, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[pos] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado",
                "status": "200",
                "usuario": usuario_actualizado
            }
    raise HTTPException(
        status_code=404, 
        detail="No se encontro el usuario"
        )