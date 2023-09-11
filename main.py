from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import json

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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "termek_lista": termek_lista})

# Új termék hozzáadása JSON formátumban
@app.post('/add_product')
async def add_product(json_file: UploadFile):
    try:
        # JSON fájl beolvasása és feldolgozása
        with json_file.file as file:
            data = json.load(file)

        return {"message": "Az új termék sikeresen hozzáadva."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hibás kérés: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
