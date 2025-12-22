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
            # Nur nicht-leere Zeilen laden
            if zeile:
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
    #vorhandene Zutaten laden
    vorhandene_zutaten = zutaten_laden()
    hinzugefuegte_zutaten = []
    doppelte_zutaten = []
    #neue Zutaten überprüfen
    for zutat in neue_zutaten.split():
        #Zutat hinzufügen, wenn sie noch nicht vorhanden ist
        if zutat and [zutat] not in vorhandene_zutaten:
            vorhandene_zutaten.append([zutat])
            hinzugefuegte_zutaten.append(zutat)
        #Zutat als doppelt markieren, wenn sie bereits vorhanden ist
        else:
            doppelte_zutaten.append(zutat)
    zutaten_speichern(vorhandene_zutaten)
    #Rückgabefälle definieren
    #neue und doppelte Zutaten
    if len(doppelte_zutaten) > 0 and len(hinzugefuegte_zutaten) > 0:
        return f"Bereits vorhandene Zutaten: {', '.join(doppelte_zutaten)}!\nHinzugefügte Zutaten: {', '.join(hinzugefuegte_zutaten)}!"
    #nur neue Zutaten
    if len(doppelte_zutaten) == 0 and len(hinzugefuegte_zutaten) > 0:
        return f"Hinzugefügte Zutaten: {', '.join(hinzugefuegte_zutaten)}!"
    #nur doppelte Zutaten
    if len(doppelte_zutaten) > 0 and len(hinzugefuegte_zutaten) == 0:
        return f"Bereits vorhandene Zutaten: {', '.join(doppelte_zutaten)}!"
    #weder neue noch doppelte Zutaten
    if len(doppelte_zutaten) == 0 and len(hinzugefuegte_zutaten) == 0:
        return "Keine neuen Zutaten hinzugefügt."

#Zutatenliste bearbeiten
def zutaten_entfernen(weg_zutaten):
    #vorhandene Zutaten laden
    vorhandene_zutaten = zutaten_laden()
    entfernte_zutaten = []
    nicht_gefundene_zutaten = []
    #zu entfernende Zutaten überprüfen
    for zutat in weg_zutaten.split():
        #Wenn Zutat vorhanden -> entfernen
        if [zutat] in vorhandene_zutaten:
            vorhandene_zutaten.remove([zutat])
            entfernte_zutaten.append(zutat)
        #Wenn Zutat nicht vorhanden -> nicht gefunden
        else:
            nicht_gefundene_zutaten.append(zutat)
    zutaten_speichern(vorhandene_zutaten)
    #Rückgabefälle definieren
    #entfernte und nicht gefundene Zutaten
    if len(nicht_gefundene_zutaten) > 0 and len(entfernte_zutaten) > 0:
        return f"Nicht gefundene Zutaten: {', '.join(nicht_gefundene_zutaten)}!\nEntfernte Zutaten: {', '.join(entfernte_zutaten)}!"
    #nur entfernte Zutaten
    if len(nicht_gefundene_zutaten) == 0 and len(entfernte_zutaten) > 0:
        return f"Entfernte Zutaten: {', '.join(entfernte_zutaten)}!"
    #nur nicht gefundene Zutaten
    if len(nicht_gefundene_zutaten) > 0 and len(entfernte_zutaten) == 0:
        return f"Nicht gefundene Zutaten: {', '.join(nicht_gefundene_zutaten)}!"
    #weder entfernte noch nicht gefundene Zutaten
    if len(nicht_gefundene_zutaten) == 0 and len(entfernte_zutaten) == 0:
        return "Keine Zutaten entfernt."
    
#Rezepte hinzufügen
def rezepte_hinzufuegen(neuer_name, neue_zutaten):
    #vorhandene Rezepte laden
    rezepte = rezepte_laden()
    #prüfen, ob Rezeptname bereits existiert
    if neuer_name in rezepte:
        return f"Rezept '{neuer_name}' existiert bereits!"
    #Zutaten in Liste umwandeln
    zutaten_neu = neue_zutaten.split()
    #neue Zutaten zum Rezept hinzufügen
    rezepte[neuer_name] = zutaten_neu
    #Rezepte speichern
    rezepte_speichern(rezepte)
    return f"Rezept '{neuer_name}' wurde hinzugefügt."

#Rezepte entfernen
def rezepte_entfernen(rezeptname):
    #vorhandene Rezepte laden
    rezepte = rezepte_laden()
    #prüfen, ob Rezept existiert
    if rezeptname in rezepte:
        del rezepte[rezeptname]
        rezepte_speichern(rezepte)
        return f"Rezept '{rezeptname}' wurde entfernt."
    #falls Rezept nicht existiert
    else:
        return f"Rezept '{rezeptname}' nicht gefunden."

#Rezepte bearbeiten
def rezepte_bearbeiten(rezeptname):
    #vorhandene Rezepte laden
    rezepte = rezepte_laden()
    #prüfen, ob Rezept existiert
    if rezeptname in rezepte:
        match input("Möchten Sie den Namen (1) oder die Zutaten (2) bearbeiten? "):
            case "1":
                #Zutaten von Rezept holen
                zutatenliste = rezepte[rezeptname]
                neuer_name = input("Geben Sie den neuen Namen des Rezepts ein: ")
                #Zutaten auf neuen Namen speichern
                rezepte[neuer_name] = zutatenliste
                #altes Rezept löschen
                del rezepte[rezeptname]
                #Rezepte speichern
                rezepte_speichern(rezepte)
            case "2":
                zutatenliste = input("Geben Sie die neuen Zutaten des Rezepts ein (durch Leerzeichen getrennt): ")
                #Zutaten in Liste umwandeln
                zutaten = zutatenliste.split()
                #Zutaten des Rezepts aktualisieren
                rezepte[rezeptname] = zutaten
                #Rezepte speichern
                rezepte_speichern(rezepte)
                print(f"Rezept '{rezeptname}' wurde aktualisiert.")
            case _:
                print("Ungültige Auswahl.")
    #falls Rezept nicht existiert
    else:
        print(f"Rezept '{rezeptname}' nicht gefunden.")

#Ein Rezept anzeigen
def rezept_anzeigen(rezeptname):
    #vorhandene Rezepte laden
    rezepte = rezepte_laden()
    #prüfen, ob Rezept existiert
    if rezeptname in rezepte:
        #Zutatenliste holen
        zutatenliste = rezepte[rezeptname]
        #Rezept und Zutaten zurückgeben
        return f"Rezept '{rezeptname}': {', '.join(zutatenliste)}"
    #falls Rezept nicht existiert
    else:
        return f"Rezept '{rezeptname}' nicht gefunden."

#Rezeptprüfung
def rezeptprüfung(rezeptname):
    fehlend = []
    #vorhandene Rezepte laden
    rezepte = rezepte_laden()
    #vorhandene Zutaten laden
    vorhandene_zutaten = zutaten_laden()
    #prüfen, ob Rezept existiert
    if rezeptname not in rezepte:
        return f"Rezept '{rezeptname}' nicht gefunden!"
    #benötigte Zutaten laden
    benoetigt = rezepte[rezeptname]
    #fehlende Zutaten überprüfen
    for zutat in benoetigt:
        if [zutat] not in vorhandene_zutaten:
            fehlend.append(zutat)
    #falls fehlende Zutaten vorhanden sind
    if len(fehlend) > 0:
        return f"Fehlende Zutaten für {rezeptname}: {', '.join(fehlend)}!"
    #falls alle Zutaten vorhanden sind
    else:
        return "Alle Zutaten gefunden!"

#Main
def main():
    print("Willkommen.")
    while True:
        print("Bitte wählen Sie einen Modus:")

        vorhandene_zutaten = zutaten_laden()
        rezepte = rezepte_laden()
        rezepte_liste = list(rezepte.keys())

        print("Wähle 1 zum Zutaten hinzufügen!")
        print("Wähle 2 zum Zutaten entfernen!")
        print("Wähle 3 zum Rezepte hinzufügen!")
        print("Wähle 4 zum Rezepte bearbeiten!")
        print("Wähle 5 zum Rezepte entfernen!")
        print("Wähle 6 um EIN Rezept anzuzeigen!")
        print("Wähle 7 zum Zutaten anzeigen!")
        print("Wähle 8 zum Rezepte anzeigen!")
        print("Wähle 9 zum Vergleichen!")
        print("Wähle 0 zum Beenden!")

        match input("Modus: "):
            case "1":#Zutaten hinzufügen
                neue_zutaten = input("Geben Sie die hinzuzufügende Zutat(en) ein: ")
                print(zutaten_hinzufuegen(neue_zutaten))
            case "2":#Zutaten entfernen
                entfernende_zutaten = input("Geben Sie die zu entfernende Zutat(en) ein: ")
                print(zutaten_entfernen(entfernende_zutaten))
            case "3":#Rezepte hinzufügen
                neuer_name = input("Geben Sie den Namen des neuen Rezepts ein: ")
                neue_zutaten = input("Geben Sie die Zutaten des Rezepts ein (durch Leerzeichen getrennt): ")
                print(rezepte_hinzufuegen(neuer_name, neue_zutaten))
            case "4":#Rezepte bearbeiten
                rezeptname = input("Geben Sie den Namen des zu bearbeitenden Rezepts ein: ")
                rezepte_bearbeiten(rezeptname)
            case "5":#Rezepte entfernen
                rezeptname = input("Geben Sie den Namen des zu entfernenden Rezepts ein: ")
                print(rezepte_entfernen(rezeptname))
            case "6":#Ein Rezept anzeigen
                rezeptname = input("Geben Sie den Namen des Rezept ein: ")
                print(rezept_anzeigen(rezeptname))
            case "7":#Zutaten anzeigen
                print(vorhandene_zutaten)
            case "8":#Rezepte anzeigen
                print(rezepte_liste)
            case "9":#Rezeptprüfung
                rezeptname = input("Geben Sie den Namen des Rezept ein: ")
                print(rezeptname)
                print(rezeptprüfung(rezeptname))
            case "0":#Beenden
                break
            case _:#ELSE
                print("Ungültige Eingabe.")

