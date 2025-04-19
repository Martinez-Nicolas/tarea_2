from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Vuelo, VueloBase
from database import get_db
from doubly_linked import DoublyLinkedList
from typing import List

app = FastAPI(title="Gestor de Vuelos")

dll_vuelos = DoublyLinkedList()

@app.post("/vuelos", response_model=VueloBase)
def agregar_vuelo(vuelo: VueloBase, al_frente: bool = False, db: Session = Depends(get_db)):
    nuevo_vuelo = Vuelo(**vuelo.dict())
    if al_frente:
        dll_vuelos.insertar_al_frente(nuevo_vuelo)
    else:
        dll_vuelos.insertar_al_final(nuevo_vuelo)
    return nuevo_vuelo

@app.get("/vuelos/total")
def total_vuelos():
    return {"total": dll_vuelos.longitud()}

@app.get("/vuelos/proximo", response_model=VueloBase)
def obtener_proximo():
    vuelo = dll_vuelos.obtener_primero()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos disponibles.")
    return vuelo

@app.get("/vuelos/ultimo", response_model=VueloBase)
def obtener_ultimo():
    vuelo = dll_vuelos.obtener_ultimo()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos disponibles.")
    return vuelo

@app.post("/vuelos/insertar", response_model=VueloBase)
def insertar_en_posicion(vuelo: VueloBase, posicion: int):
    if posicion < 0 or posicion > dll_vuelos.longitud():
        raise HTTPException(status_code=400, detail="Posición inválida.")
    nuevo_vuelo = Vuelo(**vuelo.dict())
    dll_vuelos.insertar_en_posicion(nuevo_vuelo, posicion)
    return nuevo_vuelo

@app.delete("/vuelos/extraer")
def extraer_vuelo(posicion: int):
    if posicion < 0 or posicion >= dll_vuelos.longitud():
        raise HTTPException(status_code=400, detail="Posición inválida.")
    vuelo = dll_vuelos.extraer_de_posicion(posicion)
    return {"mensaje": "Vuelo extraído correctamente", "vuelo": vuelo}

@app.get("/vuelos/lista", response_model=List[VueloBase])
def listar_vuelos():
    return dll_vuelos.listar()

@app.patch("/vuelos/reordenar")
def reordenar_vuelos(nueva_orden: List[int]):
    vuelos_actuales = dll_vuelos.listar()
    if set(nueva_orden) != set(range(len(vuelos_actuales))):
        raise HTTPException(status_code=400, detail="Orden inválido.")

    vuelos_reordenados = [vuelos_actuales[i] for i in nueva_orden]
    dll_vuelos.clear()
    for vuelo in vuelos_reordenados:
        dll_vuelos.insertar_al_final(vuelo)

    return {"mensaje": "Vuelos reordenados correctamente"}