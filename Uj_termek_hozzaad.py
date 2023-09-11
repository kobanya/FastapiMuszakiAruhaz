import requests
import json

# Felhasználótól bekért adatok
termek_neve = input("Termék neve: ")
leiras = input("Leírás: ")
ara = int(input("Ára (egész szám): "))
kategoria = input("Kategória: ")

# Az új termék adatainak létrehozása
uj_termek = {
    "termek_neve": termek_neve,
    "leiras": leiras,
    "ara": ara,
    "kategoria": kategoria
}

# API végpont URL-je
api_url = "http://localhost:8000/add_product"  # Cseréld ki az API URL-jét a saját projektzedre

# POST kérés elküldése az új termék létrehozásához
try:
    response = requests.post(api_url, json=uj_termek)
    if response.status_code == 200:
        print("Az új termék sikeresen hozzáadva.")
        print("Az új termék adatai:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Hiba történt a kérés során. Státuszkód: {response.status_code}")
except Exception as e:
    print(f"Hiba történt a kérés során: {str(e)}")
