import json
import csv

#Variablen setzen
REZEPTADRESSE = "rezepte.json"
ZUTATENADRESSE = "zutaten.csv"

#Zutaten laden
def zutaten_laden():
    vorhandene_zutaten = []
    with open(ZUTATENADRESSE, mode="r") as f:
        reader = csv.reader(f)
        for zeile in reader:
            if zeile:  # Nur nicht-leere Zeilen laden
                vorhandene_zutaten.append(zeile)
    return vorhandene_zutaten

#Rezepte laden
def rezepte_laden():
    with open(REZEPTADRESSE, "r") as f:
        rezepte = json.load(f)
    return rezepte

#Zutaten speichern
def zutaten_speichern(zutatenliste):
    #CSV Datei leeren
    with open(ZUTATENADRESSE, 'w', newline='', encoding='utf-8') as f:
        pass
    #neue Zutatenliste speichern
    with open(ZUTATENADRESSE, mode="w") as f:
                writer = csv.writer(f)
                for eintrag in zutatenliste:
                    if eintrag not in (None, "", []):
                        writer.writerow(eintrag) 

#Rezepte speichern
def rezepte_speichern(rezepte):
    with open(REZEPTADRESSE, "w") as f:
        json.dump(rezepte, f, indent=4)

def zutaten_hinzufuegen(neue_zutaten):
    vorhandene_zutaten = zutaten_laden()
    hinzugefuegte_zutaten = []
    doppelte_zutaten = []
    for zutat in neue_zutaten.split():
        if zutat and [zutat] not in vorhandene_zutaten:
            vorhandene_zutaten.append([zutat])
            hinzugefuegte_zutaten.append(zutat)
        else:
            doppelte_zutaten.append(zutat)
    zutaten_speichern(vorhandene_zutaten)
    if len(doppelte_zutaten) > 0 and len(hinzugefuegte_zutaten) > 0:
        return f"Bereits vorhandene Zutaten: {', '.join(doppelte_zutaten)}!\nHinzugefügte Zutaten: {', '.join(hinzugefuegte_zutaten)}!"
    if len(doppelte_zutaten) == 0 and len(hinzugefuegte_zutaten) > 0:
        return f"Hinzugefügte Zutaten: {', '.join(hinzugefuegte_zutaten)}!"
    if len(doppelte_zutaten) > 0 and len(hinzugefuegte_zutaten) == 0:
        return f"Bereits vorhandene Zutaten: {', '.join(doppelte_zutaten)}!"
    if len(doppelte_zutaten) == 0 and len(hinzugefuegte_zutaten) == 0:
        return "Keine neuen Zutaten hinzugefügt."

#Zutatenliste bearbeiten
def zutaten_entfernen(weg_zutaten):
    vorhandene_zutaten = zutaten_laden()
    entfernte_zutaten = []
    nicht_gefundene_zutaten = []
    for zutat in weg_zutaten.split():
        if [zutat] in vorhandene_zutaten:
            vorhandene_zutaten.remove([zutat])
            entfernte_zutaten.append(zutat)
        else:
            print(f"{zutat} nicht gefunden.")
            nicht_gefundene_zutaten.append(zutat)
    zutaten_speichern(vorhandene_zutaten)
    if len(nicht_gefundene_zutaten) > 0 and len(entfernte_zutaten) > 0:
        return f"Nicht gefundene Zutaten: {', '.join(nicht_gefundene_zutaten)}!\nEntfernte Zutaten: {', '.join(entfernte_zutaten)}!"
    if len(nicht_gefundene_zutaten) == 0 and len(entfernte_zutaten) > 0:
        return f"Entfernte Zutaten: {', '.join(entfernte_zutaten)}!"
    if len(nicht_gefundene_zutaten) > 0 and len(entfernte_zutaten) == 0:
        return f"Nicht gefundene Zutaten: {', '.join(nicht_gefundene_zutaten)}!"
    if len(nicht_gefundene_zutaten) == 0 and len(entfernte_zutaten) == 0:
        return "Keine Zutaten entfernt."
    
#Rezepte hinzufügen
def rezepte_hinzufuegen():
    rezepte = rezepte_laden()
    rezeptname_neu = input("Geben Sie den Namen des neuen Rezepts ein: ")
    if rezeptname_neu in rezepte:
        return f"Rezept '{rezeptname_neu}' existiert bereits!"
    zutaten_neues_rezept = input("Geben Sie die Zutaten des Rezepts ein (durch Leerzeichen getrennt): ")
    zutaten_neu = zutaten_neues_rezept.split()
    rezepte[rezeptname_neu] = zutaten_neu
    rezepte_speichern(rezepte)
    return f"Rezept '{rezeptname_neu}' wurde hinzugefügt."

#Rezepte entfernen
def rezepte_entfernen(rezeptname):
    rezepte = rezepte_laden()
    rezeptname = input("Geben Sie den Namen des neuen Rezepts ein: ")
    if rezeptname in rezepte:
        del rezepte[rezeptname]
        rezepte_speichern(rezepte)
        return f"Rezept '{rezeptname}' wurde entfernt."
    else:
        return f"Rezept '{rezeptname}' nicht gefunden."

#Rezepte bearbeiten
def rezepte_bearbeiten():
    rezepte = rezepte_laden()
    rezeptname = input("Geben Sie den Namen des neuen Rezepts ein: ")
    if rezeptname in rezepte:
        match input("Möchten Sie den Namen (1) oder die Zutaten (2) bearbeiten? "):
            case "1":
                return 0
            case "2":
                zutatenliste = input("Geben Sie die neuen Zutaten des Rezepts ein (durch Leerzeichen getrennt): ")
                zutaten = zutatenliste.split()
                rezepte[rezeptname] = zutaten
                rezepte_speichern(rezepte)
                print(f"Rezept '{rezeptname}' wurde aktualisiert.")
            case _:
                print("Ungültige Auswahl.")
    else:
        print(f"Rezept '{rezeptname}' nicht gefunden.")

#Rezeptprüfung
def rezeptprüfung(rezeptname):
  fehlend = []
  rezepte = rezepte_laden()
  vorhandene_zutaten = zutaten_laden()
  if rezeptname not in rezepte:
    return f"Rezept '{rezeptname}' nicht gefunden!"
  benoetigt = rezepte[rezeptname]
  for zutat in benoetigt:
    if [zutat] not in vorhandene_zutaten:
      fehlend.append(zutat)

  if len(fehlend) > 0:
    return f"Fehlende Zutaten für {rezeptname}: {', '.join(fehlend)}!"
  else:
    return "Alle Zutaten gefunden!"

#Ausgabe
while True:
    print("Willkommen.")
    print("Bitte wählen Sie einen Modus:")

    vorhandene_zutaten = zutaten_laden()
    rezepte = rezepte_laden()
    rezepte_liste = list(rezepte.keys())

    print("Wähle 1 zum Zutaten hinzufügen!")
    print("Wähle 2 zum Zutaten entfernen!")
    print("Wähle 3 zum Rezepte hinzufügen!")
    print("Wähle 4 zum Rezepte bearbeiten!")
    print("Wähle 5 zum Rezepte entfernen!")
    print("Wähle 7 zum Zutaten anzeigen!")
    print("Wähle 8 zum Rezepte anzeigen!")
    print("Wähle 9 zum Vergleichen!")
    print("Wähle 0 zum Beenden!")
    modus = input("Modus: ")

    match modus:
        case "1":#Zutaten hinzufügen
            print(zutaten_hinzufuegen(input("Geben Sie die hinzuzufügende Zutat(en) ein: ")))
        case "2":#Zutaten entfernen
            print(zutaten_entfernen(input("Geben Sie die zu entfernende Zutat(en) ein: ")))
        case "3":#Rezepte hinzufügen
            print(rezepte_hinzufuegen())
        case "4":#Rezepte bearbeiten
            rezepte_bearbeiten()
        case "5":#Rezepte entfernen
            print(rezepte_entfernen(input("Geben Sie den Namen des zu entfernenden Rezepts ein: ")))
        case "7":#Zutaten anzeigen
            print(vorhandene_zutaten)
        case "8":#Rezepte anzeigen
            print(rezepte_liste)
        case "9":#Rezeptprüfung
            print(rezeptprüfung(input("Rezeptname: ")))
        case "0":#Beenden
            break
        case _:#ELSE
            print("Ungültige Eingabe.")

