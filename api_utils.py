import os
import requests
import ollama
import io
from dotenv import load_dotenv
from typing import List
from PIL import Image

# Laden der Umgebungsvariablen aus der .env Datei
load_dotenv()

# Konfiguration der Edamam API
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")
EDAMAM_URL = "https://api.edamam.com/api/recipes/v2"

def analyze_ingredients_from_images(images: List[Image.Image]) -> List[str]:
    """
    Verwendet das lokale Ollama-Modell (Qwen 2.5-VL), um Zutaten aus Bildern zu erkennen.
    
    Args:
        images (List[Image.Image]): Eine Liste von PIL-Image-Objekten.
        
    Returns:
        List[str]: Eine Liste von erkannten Zutaten als Strings.
    """
    # Prompt auf Englisch für das Qwen-Modell
    prompt = (
        "Analyze these images and identify ONLY edible food ingredients suitable for cooking. "
        "Ignore everything else (like trees, landscapes, people, plates, utensils). "
        "If you see valid ingredients, return them as a comma-separated list (e.g., 'Tomato, Onion'). "
        "If the image contains NO edible ingredients, return exactly: 'Fehler: Keine essbaren Zutaten erkannt'."
    )

    image_bytes_list = []
    
    # Konvertiere PIL-Bilder in Bytes für Ollama
    try:
        for img in images:
            img_byte_arr = io.BytesIO()
            # Format beibehalten oder als PNG speichern, falls kein Format gesetzt
            fmt = img.format if img.format else 'PNG'
            img.save(img_byte_arr, format=fmt)
            image_bytes_list.append(img_byte_arr.getvalue())
    except Exception as e:
        return [f"Fehler bei der Bildverarbeitung: {str(e)}"]

    try:
        response = ollama.chat(
            model='qwen2.5vl:3b',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': image_bytes_list
            }]
        )
        
        # Verarbeitung der Antwort
        text = response['message']['content'].strip()
        
        # Check explicit error from model
        if text.startswith("Fehler:"):
            return [text]

        # Bereinigen und Splitten der Liste
        ingredients = [item.strip() for item in text.split(',') if item.strip()]
        return ingredients

    except Exception as e:
        return [f"Fehler bei der Ollama-Analyse: {str(e)}"]

def fetch_recipes_from_edamam(ingredients: List[str]) -> List[dict]:
    """
    Sucht nach Rezepten über die Edamam API basierend auf einer Liste von Zutaten.
    
    Args:
        ingredients (List[str]): Eine Liste von Zutaten.
        
    Returns:
        List[dict]: Eine Liste von Rezept-Dictionaries mit Titel, URL, Bild, etc.
    """
    if not EDAMAM_APP_ID or not EDAMAM_APP_KEY:
        return []

    query = ",".join(ingredients)
    params = {
        "type": "public",
        "q": query,
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY
    }
    
    # Header hinzufügen, um "requires userID" Fehler zu beheben
    headers = {
        "Edamam-Account-User": "kuecheninventar_user"
    }

    try:
        response = requests.get(EDAMAM_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        recipes = []
        if "hits" in data:
            for hit in data["hits"]:
                recipe_data = hit["recipe"]
                recipes.append({
                    "label": recipe_data.get("label"),
                    "url": recipe_data.get("url"),
                    "image": recipe_data.get("image"),
                    "ingredientLines": recipe_data.get("ingredientLines", []),
                    "calories": int(recipe_data.get("calories", 0)),
                    "cuisineType": ", ".join(recipe_data.get("cuisineType", []))
                })
        return recipes
    except Exception as e:
        print(f"Fehler beim Abrufen der Rezepte: {e}")
        return []
