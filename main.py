from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import json
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Az alkalmazás indításakor olvasd be az adatokat a JSON fájlból
def load_data():
    try:
        with open('termek_lista.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return []

termek_lista = load_data()

# Pydantic modell az új termék adatainak validációjához
class Termek(BaseModel):
    termek_neve: str
    leiras: str
    ara: int  # Árat most egész számként deklaráljuk
    kategoria: str

# Főoldal
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "termek_lista": termek_lista})

# Új termék hozzáadása JSON formátumban
@app.post('/add_product', response_model=Termek)
async def add_product(termek: Termek):
    try:
        # Az új terméknek generáljunk egyedi ID-t (például a lista hossza alapján)
        new_id = len(termek_lista) + 1
        termek_dict = termek.dict()
        termek_dict["ID"] = new_id

        # Az új termék hozzáadása a termek_lista-hoz
        termek_lista.append(termek_dict)

        # Az új termék mentése JSON fájlba
        with open('termek_lista.json', 'w', encoding='utf-8') as json_file:
            json.dump(termek_lista, json_file, ensure_ascii=False, indent=4)

        return termek  # Visszaadjuk az új terméket a válaszban, ami tartalmazza az ID-t
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hibás kérés: {str(e)}")

# API futtatása
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
