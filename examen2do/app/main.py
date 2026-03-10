from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List
from datetime import datetime

app = FastAPI(title="examen 2 parcial")

#modelos 
class CrearReserva(BaseModel):
    Habitacion: str
    Nombre_Huesped: str= Field(min_length=5)
    Fecha: datetime= Field(min_length=datetime)
    Dias: int= Field(le=8)

class Reserva(BaseModel):
    id: int



#Base de datos
Reservas: Dict[int, Reserva] = {}

#endpoints

@app.post("/Reservas")