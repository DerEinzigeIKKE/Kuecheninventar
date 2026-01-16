import streamlit as st
from PIL import Image
import json

from database import init_db, get_db, Recipe, User
from auth import register_user, authenticate_user
from api_utils import analyze_ingredients_from_images, fetch_recipes_from_edamam

# Seitenkonfiguration
st.set_page_config(page_title="Kücheninventar", layout="wide")

def main():
    """
    Hauptfunktion der Streamlit-Anwendung.
    """
    # Datenbank initialisieren
    init_db()

    # Session State für Login-Status initialisieren
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None

    # Sidebar für Authentifizierung
    st.sidebar.title("Benutzerkonto")
    
    db = next(get_db()) 

    if st.session_state.user_id is None:
        auth_mode = st.sidebar.radio("Modus wählen", ["Login", "Registrieren"])
        
        username = st.sidebar.text_input("Benutzername")
        password = st.sidebar.text_input("Passwort", type="password")
        
        if auth_mode == "Login":
            if st.sidebar.button("Einloggen"):
                user = authenticate_user(db, username, password)
                if user:
                    st.session_state.user_id = user.id
                    st.session_state.username = user.username
                    st.sidebar.success(f"Willkommen zurück, {user.username}!")
                    st.rerun()
                else:
                    st.sidebar.error("Ungültiger Benutzername oder Passwort.")
        
        elif auth_mode == "Registrieren":
            if st.sidebar.button("Registrieren"):
                if username and password:
                    success = register_user(db, username, password)
                    if success:
                        st.sidebar.success("Registrierung erfolgreich! Bitte einloggen.")
                    else:
                        st.sidebar.error("Benutzername bereits vergeben.")
                else:
                    st.sidebar.warning("Bitte alle Felder ausfüllen.")
    
    else:
        # Eingeloggter Bereich
        st.sidebar.write(f"Angemeldet als: **{st.session_state.username}**")
        if st.sidebar.button("Ausloggen"):
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()

        st.title("Kücheninventar")
        
        tab1, tab2 = st.tabs(["Suche & Entdecken", "Meine Gespeicherten Rezepte"])
        
        # --- TAB 1: Suche ---
        with tab1:
            st.header("Zutaten eingeben oder scannen")
            
            col1, col2 = st.columns(2)
            
            detected_ingredients = []
            
            with col1:
                st.subheader("Bild-Upload")
                uploaded_files = st.file_uploader(
                    "Lade Fotos deiner Zutaten hoch", 
                    accept_multiple_files=True, 
                    type=['png', 'jpg', 'jpeg'],
                    key="ingredient_images_upload"
                )
                
                if uploaded_files:
                    images = []
                    for uploaded_file in uploaded_files:
                        image = Image.open(uploaded_file)
                        images.append(image)
                        st.image(image, caption="Hochgeladenes Bild", width=150)
                    
                    if st.button("Zutaten erkennen"):
                        with st.spinner("Qwen analysiert deine Bilder..."):
                            detected_ingredients = analyze_ingredients_from_images(images)
                            if detected_ingredients:
                                st.success(f"Erkannte Zutaten: {', '.join(detected_ingredients)}")
                                with st.spinner("Suche nach passenden Rezepten..."):
                                    st.session_state.recipes = fetch_recipes_from_edamam(detected_ingredients)
                                    st.session_state.search_performed = True
                            else:
                                st.error("Keine Zutaten erkannt oder Fehler aufgetreten.")

            with col2:
                st.subheader("Manuelle Eingabe")
                text_input = st.text_input("Zutaten eingeben (kommagetrennt)", value=", ".join(detected_ingredients) if detected_ingredients else "")
                
            # Suche auslösen
            final_ingredients = [x.strip() for x in text_input.split(',')] if text_input else detected_ingredients
            
            if 'recipes' not in st.session_state:
                st.session_state.recipes = []
            if 'search_performed' not in st.session_state:
                st.session_state.search_performed = False

            if st.button("Rezepte suchen"):
                if final_ingredients:
                    with st.spinner("Suche nach Rezepten via Edamam..."):
                        st.session_state.recipes = fetch_recipes_from_edamam(final_ingredients)
                        st.session_state.search_performed = True
                else:
                    st.warning("Bitte gib mindestens eine Zutat an.")
            
            if st.session_state.recipes:
                st.write(f"Gefundene Rezepte: {len(st.session_state.recipes)}")
                for idx, recipe in enumerate(st.session_state.recipes):
                    with st.expander(f"{recipe['label']}"):
                        col_img, col_desc = st.columns([1, 2])
                        with col_img:
                            if recipe['image']:
                                st.image(recipe['image'])
                        with col_desc:
                            st.write("**Zutaten:**")
                            for line in recipe['ingredientLines']:
                                st.write(f"- {line}")
                            
                            st.write(f"**Kalorien:** {recipe['calories']} kcal")
                            st.write(f"**Küche:** {recipe['cuisineType']}")
                            st.write(f"[Zum Rezept]({recipe['url']})")
                            
                            # Speichern-Button
                            if st.button(f"Speichern", key=f"save_{idx}"):
                                # Prüfen, ob bereits gespeichert (einfache Logik)
                                existing = db.query(Recipe).filter_by(
                                    user_id=st.session_state.user_id, 
                                    title=recipe['label']
                                ).first()
                                
                                if not existing:
                                    new_recipe = Recipe(
                                        user_id=st.session_state.user_id,
                                        title=recipe['label'],
                                        url=recipe['url'],
                                        image_url=recipe['image'],
                                        ingredients=json.dumps(recipe['ingredientLines']),
                                        calories=recipe['calories'],
                                        cuisine_type=recipe['cuisineType']
                                    )
                                    db.add(new_recipe)
                                    db.commit()
                                    st.success("Rezept gespeichert!")
                                else:
                                    st.warning("Rezept bereits in deiner Sammlung.")
            elif st.session_state.search_performed:
                 st.info("Keine Rezepte gefunden.")

        # --- TAB 2: Gespeicherte Rezepte ---
        with tab2:
            st.header("Meine Lieblingsrezepte")
            saved_recipes = db.query(Recipe).filter(Recipe.user_id == st.session_state.user_id).all()
            
            if saved_recipes:
                for s_recipe in saved_recipes:
                    with st.expander(s_recipe.title):
                        if s_recipe.image_url:
                            st.image(s_recipe.image_url, width=200)
                        
                        st.write(f"**Kalorien:** {s_recipe.calories} kcal")
                        st.write(f"**Küche:** {s_recipe.cuisine_type}")
                        st.write(f"[Rezept ansehen]({s_recipe.url})")
                        
                        if s_recipe.ingredients:
                            try:
                                ing_list = json.loads(s_recipe.ingredients)
                                st.write("**Zutaten:**")
                                for item in ing_list:
                                    st.write(f"- {item}")
                            except:
                                st.write("Zutaten konnten nicht geladen werden.")
                        
                        if st.button("Löschen", key=f"del_{s_recipe.id}"):
                            db.delete(s_recipe)
                            db.commit()
                            st.rerun()
            else:
                st.info("Du hast noch keine Rezepte gespeichert.")

if __name__ == "__main__":
    main()
