# 1. importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

# 2. inicializacion app
app = FastAPI(
    title="Mi primer API con JWT",
    description="API protegida con OAuth2 + JWT en FastAPI",
    version="2.0.0"
)

# 3. base de datos ficticia de usuarios del sistema
fake_users_db = {
    "jesusmartinez": {
        "username": "jesusmartinez",
        "password": "123456"
    }
}

# 4. base de datos ficticia de datos del api
usuarios = [
    {"id": 1, "nombre": "jesus", "edad": 21},
    {"id": 2, "nombre": "yahir", "edad": 22},
    {"id": 3, "nombre": "julian", "edad": 22},
]

# 5. modelos de validacion
class UsuarioCrear(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    edad: Optional[int] = Field(None, ge=1, le=123)

class Token(BaseModel):
    access_token: str
    token_type: str

# 6. configuracion jwt
SECRET_KEY = "mi_clave_super_secreta_para_jwt_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 7. esquema oauth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 8. funciones de autenticacion
def autenticar_usuario(username: str, password: str):
    usuario = fake_users_db.get(username)
    if not usuario:
        return None
    if usuario["password"] != password:
        return None
    return usuario

def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validar_token(token: str = Depends(oauth2_scheme)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credenciales_exception

    except JWTError:
        raise credenciales_exception

    usuario = fake_users_db.get(username)
    if usuario is None:
        raise credenciales_exception

    return username

# 9. endpoint para generar token
@app.post("/token", response_model=Token, tags=["Autenticacion"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar_usuario(form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contrasena incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = crear_access_token(
        data={"sub": usuario["username"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# 10. endpoints
@app.get("/", tags=["Inicio"])
async def hola_mundo():
    return {"mensaje": "Hola mundo FASTAPI"}

@app.get("/v1/bienvenidos", tags=["Bienvenidos"])
async def bien():
    return {"mensaje": "Bienvenidos"}

@app.get("/v1/promedio", tags=["Calificaciones"])
async def promedio():
    await asyncio.sleep(3)
    return {
        "Calificacion": "7.5",
        "estatus": "200"
    }

@app.get("/v1/parametro0/{id}", tags=["Parametros"])
async def consulta_uno(id: int):
    await asyncio.sleep(3)
    return {
        "Resultado": "Usuario encontrado",
        "Estatus": "200"
    }

@app.get("/v1/parametro1/", tags=["Parametro opcional"])
async def consulta_op(id: Optional[int] = None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado": id, "Datos": usuario}
        return {"Resultado": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporciono id"}

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def consulta_t():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def crear_usuario(usuario: UsuarioCrear):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())
    return {
        "mensaje": "Usuario agregado correctamente",
        "status": "200",
        "usuario": usuario
    }

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(
    id: int,
    usuario_actualizado: UsuarioActualizar,
    user_auth: str = Depends(validar_token)
):
    for usr in usuarios:
        if usr["id"] == id:
            if usuario_actualizado.nombre is not None:
                usr["nombre"] = usuario_actualizado.nombre
            if usuario_actualizado.edad is not None:
                usr["edad"] = usuario_actualizado.edad

            return {
                "mensaje": f"Usuario actualizado correctamente por {user_auth}",
                "status": "200",
                "usuario": usr
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(
    id: int,
    user_auth: str = Depends(validar_token)
):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado correctamente por {user_auth}",
                "status": "200",
                "usuario_eliminado": usr
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")