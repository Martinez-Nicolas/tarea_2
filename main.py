#uvicorn main:app --reload

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Vuelo, VueloBase
from database import get_db
from doubly_linked import DoublyLinkedList
from typing import List

app = FastAPI()

# Creamos una instancia de la lista doblemente enlazada para manejar los vuelos
vuelos_lista = DoublyLinkedList()

# 1. POST /vuelos - Agregar un vuelo (normal o emergencia)
@app.post("/vuelos", response_model=VueloBase)
def agregar_vuelo(vuelo: VueloBase, al_frente: bool = False, db: Session = Depends(get_db)):
    db_vuelo = Vuelo(nombre=vuelo.nombre, tipo=vuelo.tipo, prioridad=vuelo.prioridad)
    
    if al_frente:
        vuelos_lista.insertar_al_frente(db_vuelo)  # Agregar al frente usando la lista doblemente enlazada
    else:
        vuelos_lista.insertar_al_final(db_vuelo)  # Agregar al final usando la lista doblemente enlazada
    
    return db_vuelo

# 2. GET /vuelos/total - Retorna el número total de vuelos
@app.get("/vuelos/total")
def total_vuelos(db: Session = Depends(get_db)):
    return {"total": vuelos_lista.longitud()}  # Retornar el tamaño de la lista

# 3. GET /vuelos/proximo - Retorna el primer vuelo sin remover
@app.get("/vuelos/proximo", response_model=VueloBase)
def proximo_vuelo(db: Session = Depends(get_db)):
    db_vuelo = vuelos_lista.obtener_primero()  # Obtener el primer vuelo de la lista
    if db_vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos disponibles.")
    return db_vuelo

# 4. GET /vuelos/ultimo - Retorna el último vuelo sin remover
@app.get("/vuelos/ultimo", response_model=VueloBase)
def ultimo_vuelo(db: Session = Depends(get_db)):
    db_vuelo = vuelos_lista.obtener_ultimo()  # Obtener el último vuelo de la lista
    if db_vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos disponibles.")
    return db_vuelo

# 5. POST /vuelos/insertar - Inserta un vuelo en una posición específica
@app.post("/vuelos/insertar", response_model=VueloBase)
def insertar_vuelo(vuelo: VueloBase, posicion: int, db: Session = Depends(get_db)):
    if posicion < 0 or posicion >= vuelos_lista.longitud():
        raise HTTPException(status_code=400, detail="Posición inválida.")
    
    # Crear el nuevo vuelo que se quiere insertar
    db_vuelo = Vuelo(nombre=vuelo.nombre, tipo=vuelo.tipo, prioridad=vuelo.prioridad)
    
    # Insertar el vuelo en la lista doblemente enlazada en la posición especificada
    vuelos_lista.insertar_en_posicion(db_vuelo, posicion)
    
    # Devolver el vuelo insertado
    return {"mensaje": "Vuelo insertado correctamente", "vuelo": db_vuelo}

# 6. DELETE /vuelos/extraer - Elimina un vuelo de una posición específica
@app.delete("/vuelos/extraer", response_model=VueloBase)
def extraer_vuelo(posicion: int, db: Session = Depends(get_db)):
    if posicion < 0 or posicion >= vuelos_lista.longitud():
        raise HTTPException(status_code=400, detail="Posición inválida.")
    
    vuelo_extraido = vuelos_lista.extraer_de_posicion(posicion)  # Eliminar vuelo de la posición especificada
    return {"mensaje": "Vuelo extraído correctamente", "vuelo": vuelo_extraido}

# 7. GET /vuelos/lista - Lista todos los vuelos en orden actual
@app.get("/vuelos/lista", response_model=List[VueloBase])
def listar_vuelos(db: Session = Depends(get_db)):
    vuelos = []
    current = vuelos_lista.head
    while current:
        vuelos.append(current.data)
        current = current.next
    return vuelos

# 8. PATCH /vuelos/reordenar - Reordenar vuelos manualmente
@app.patch("/vuelos/reordenar")
def reordenar_vuelos(nueva_orden: List[int], db: Session = Depends(get_db)):
    vuelos = []
    current = vuelos_lista.head
    while current:
        vuelos.append(current.data)
        current = current.next
    
    if set(nueva_orden) != set(range(len(vuelos))):
        raise HTTPException(status_code=400, detail="Orden inválido.")
    
    vuelos_reordenados = [vuelos[i] for i in nueva_orden]
    vuelos_lista.clear()  # Limpiar la lista antes de agregar los vuelos reordenados
    
    for vuelo in vuelos_reordenados:
        vuelos_lista.insertar_al_final(vuelo)  # Insertar de nuevo en el orden reordenado
    
    return {"mensaje": "Vuelos reordenados correctamente"}
