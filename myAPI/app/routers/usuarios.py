#3. Endpoints
from fastapi import FastAPI,status,HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/")
async def cosultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
@routerU.post("/")
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "mensaje":"usuario agregado correctamente",
        "status":"200",
        "usuario":usuario
    }
    
@routerU.put("/{id}")
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

@routerU.delete("/{id}")
async def eliminar_usuario(id: int, userAuth:str=Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado correctamente por {userAuth}",
                "status": "200",
                "usuario_eliminado": usr
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")