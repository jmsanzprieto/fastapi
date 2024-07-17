from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI(
    title="API de Pruebas",
    description="Esta es una API de ejemplo para demostrar las funcionalidades de FastAPI.",
    version="1.0.0"
)

def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

data = load_data()

class Item(BaseModel):
    name: str
    description: str

class ItemUpdate(BaseModel):
    name: str = None
    description: str = None

@app.get("/", tags=["Root"], summary="Mensaje de bienvenida")
async def read_root():
    return {"message": "API de pruebas"}

## Ruta para ver todos los elementos
@app.get("/items", tags=["Items"], summary="Obtener todos los elementos")
async def read_items():
    return data

## Ruta para ver un elemento por su ID
@app.get("/items/{item_id}", tags=["Items"], summary="Obtener un elemento por ID")
async def read_item(item_id: int):
    item = next((item for item in data if item["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="No existe el elemento")
    return item

## Ruta para crear un nuevo elemento
@app.post("/items", tags=["Items"], summary="Crear un nuevo elemento", status_code=201)
async def create_item(item: Item):
    new_id = max(item["id"] for item in data) + 1 if data else 1
    new_item = {"id": new_id, **item.dict()}
    data.append(new_item)
    save_data(data)
    ## Mensaje de exito del proceso
    return {"message": "Se ha guardado correctamente el elemento"}


## Ruta para actualizar un elemento
@app.put("/items/{item_id}", tags=["Items"], summary="Actualizar un elemento existente")
async def update_item(item_id: int, item: ItemUpdate):
    item_data = next((item for item in data if item["id"] == item_id), None)
    if item_data is None:
        raise HTTPException(status_code=404, detail="No existe el elemento")

    item_data.update(item.dict(exclude_unset=True))
    save_data(data)
    ## Mensaje de exito del proceso
    return {"message": "Se ha actualizado correctamente el elemento"}


## Ruta para borrar un elemento
@app.delete("/items/{item_id}", tags=["Items"], summary="Eliminar un elemento", status_code=200)
async def delete_item(item_id: int):
    global data
    item_data = next((item for item in data if item["id"] == item_id), None)
    if item_data is None:
        raise HTTPException(status_code=404, detail="No existe el elemento")

    data = [item for item in data if item["id"] != item_id]
    save_data(data)
    ## Mensaje de exito del proceso
    return {"message": "Se ha borrado correctamente el elemento"}
