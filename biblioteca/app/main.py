# Importaciones
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List
from datetime import datetime

app = FastAPI(title="Biblioteca API")

CURRENT_YEAR = datetime.now().year

# MODELOS
class LibroCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    autor: str = Field(min_length=2, max_length=100)
    anio: int = Field(gt=1450, le=CURRENT_YEAR)
    paginas: int = Field(gt=1)


class Libro(LibroCreate):
    id: int
    estado: str


class Usuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr


class PrestamoCreate(BaseModel):
    libro_id: int
    usuario: Usuario


class Prestamo(BaseModel):
    id: int
    libro_id: int
    usuario: Usuario
    fecha_prestamo: str
    devuelto: bool


# BASE DE DATOS 
libros: Dict[int, Libro] = {}
prestamos: Dict[int, Prestamo] = {}
libros_prestados_activos: Dict[int, int] = {}

libro_id_seq = 1
prestamo_id_seq = 1

# ENDPOINTS
@app.get("/health")
def health():
    return {"status": "ok"}


# Registrar libro
@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(data: LibroCreate):
    global libro_id_seq

    nuevo = Libro(
        id=libro_id_seq,
        nombre=data.nombre,
        autor=data.autor,
        anio=data.anio,
        paginas=data.paginas,
        estado="disponible"
    )

    libros[libro_id_seq] = nuevo
    libro_id_seq += 1
    return nuevo


# Listar libros
@app.get("/libros", response_model=List[Libro])
def listar_libros():
    return list(libros.values())


# Buscar libro por nombre
@app.get("/libros/buscar", response_model=List[Libro])
def buscar_libro(nombre: str):
    resultados = [
        libro for libro in libros.values()
        if nombre.lower() in libro.nombre.lower()
    ]
    return resultados


# Registrar préstamo
@app.post("/prestamos", status_code=status.HTTP_201_CREATED)
def registrar_prestamo(data: PrestamoCreate):
    global prestamo_id_seq

    libro = libros.get(data.libro_id)

    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    if libro.estado == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado")

    prestamo = Prestamo(
        id=prestamo_id_seq,
        libro_id=data.libro_id,
        usuario=data.usuario,
        fecha_prestamo=datetime.now().isoformat(),
        devuelto=False
    )

    prestamos[prestamo_id_seq] = prestamo
    libros_prestados_activos[data.libro_id] = prestamo_id_seq

    libro.estado = "prestado"
    libros[data.libro_id] = libro

    prestamo_id_seq += 1
    return prestamo


# Devolver libro
@app.put("/prestamos/{prestamo_id}/devolver")
def devolver_libro(prestamo_id: int):
    prestamo = prestamos.get(prestamo_id)

    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    if prestamo.devuelto:
        return {"mensaje": "El préstamo ya estaba devuelto"}

    prestamo.devuelto = True
    libro = libros.get(prestamo.libro_id)

    if libro:
        libro.estado = "disponible"
        libros[prestamo.libro_id] = libro

    libros_prestados_activos.pop(prestamo.libro_id, None)

    return {"mensaje": "Libro devuelto correctamente"}


# Eliminar préstamo
@app.delete("/prestamos/{prestamo_id}")
def eliminar_prestamo(prestamo_id: int):
    prestamo = prestamos.get(prestamo_id)

    if not prestamo:
        raise HTTPException(status_code=409, detail="El préstamo ya no existe")

    prestamos.pop(prestamo_id)
    libros_prestados_activos.pop(prestamo.libro_id, None)

    libro = libros.get(prestamo.libro_id)
    if libro:
        libro.estado = "disponible"
        libros[prestamo.libro_id] = libro

    return {"mensaje": "Préstamo eliminado correctamente"}