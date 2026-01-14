import os
import requests
from dotenv import load_dotenv

# 1. Umgebungsvariablen neu laden
load_dotenv()

APP_ID = os.getenv("EDAMAM_APP_ID")
APP_KEY = os.getenv("EDAMAM_APP_KEY")

print("--- DEBUG START ---")

# CHECK 1: Sind die Keys überhaupt da?
if not APP_ID or not APP_KEY:
    print("❌ FEHLER: APP_ID oder APP_KEY ist leer! Prüfe deine .env Datei.")
    exit()
else:
    # Wir zeigen nur die ersten 3 Zeichen zur Sicherheit
    print(f"✅ APP_ID geladen: {APP_ID[:3]}***")
    print(f"✅ APP_KEY geladen: {APP_KEY[:3]}***")
    # Prüfen auf versteckte Leerzeichen
    if len(APP_ID.strip()) != len(APP_ID) or len(APP_KEY.strip()) != len(APP_KEY):
        print("⚠️ WARNUNG: Deine Keys enthalten Leerzeichen am Anfang oder Ende! Das verursacht den 401.")

# CHECK 2: Test-Anfrage an Edamam
test_url = "https://api.edamam.com/api/recipes/v2"
test_params = {
    "type": "public",
    "q": "chicken",  # Einfacher Test-Query
    "app_id": APP_ID.strip(), # .strip() entfernt versehentliche Leerzeichen
    "app_key": APP_KEY.strip()
}

try:
    # Wir bauen den Request vor, um die URL zu sehen
    req = requests.Request('GET', test_url, params=test_params)
    prepped = req.prepare()
    
    print(f"\nVersuche URL aufzurufen:\n{prepped.url}")
    
    # Echte Anfrage senden
    session = requests.Session()
    response = session.send(prepped)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ ERFOLG! Die API funktioniert.")
        print("Gefundene Rezepte:", len(response.json().get('hits', [])))
    elif response.status_code == 401:
        print("❌ 401 UNAUTHORIZED. Mögliche Gründe:")
        print("1. ID und Key sind vertauscht.")
        print("2. Falscher API-Plan (Recipe Search API V2 vs. Database API).")
        print("3. Tippfehler in der .env.")
    else:
        print(f"Anderer Fehler: {response.text}")

except Exception as e:
    print(f"Kritischer Fehler: {e}")

print("--- DEBUG ENDE ---")