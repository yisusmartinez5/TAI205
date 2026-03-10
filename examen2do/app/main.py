from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(title="examen 2 parcial")

#modelos 
class CrearReserva(BaseModel):
    Habitacion: str
    Nombre_Huesped: str= Field(min_length=5)
    Fecha: datetime= Field(min_length=datetime)
    Dias: int= Field(le=8)

class Reserva(BaseModel):
    id: int
    estado: str

class Usuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr


#Base de datos
Reservas: Dict[int, Reserva] = {}

#seguridad
seguridad = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth= secrets.compare_digest(credenciales.username,"hotel")
    passAuth= secrets.compare_digest(credenciales.password,"r2026")

    if not (userAuth and passAuth ):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "credenciales no autorizadas"
        )
    return credenciales.username

#endpoints

#registrar reserva
@app.post("/Reservas", status_code=status.HTTP_201_CREATED)
def crear_reserva(data: CrearReserva):
    global reserva_id_seq

    nuevo=  Reserva(
        id=reserva_id_seq,
        Habitacion=data.Habitacion,
        Nombre_Huesped=data.Nombre_Huesped,
        Fecha=data.fecha,
        Dias=data.Dias,
        estado="Confirmada"
    )
    Reservas[reserva_id_seq] = nuevo
    reserva_id_seq += 1
    return nuevo

#Listar reservas
@app.get("/Reservas", response_model=List[Reserva])
def listar_reservas():
    return list(Reserva.values())