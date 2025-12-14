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

#Zutatenliste bearbeiten
def zutaten_bearbeiten():
    print("Möchten Sie eine Zutat hinzufügen (1) oder entfernen (2)?")
    wahl = input("Eingabe: ")
    vorhandene_zutaten = zutaten_laden()
    match wahl:
#Zutat hinzufügen        
        case "1":
            neue_zutat = input("Geben Sie die hinzuzufügende Zutat(en) ein: ")
            for zutat in neue_zutat.split():
                if zutat and [zutat] not in vorhandene_zutaten:
                    vorhandene_zutaten.append([zutat])
                    print(f"{zutat} wurde hinzugefügt.")
                else:
                    print(f"{zutat} ist bereits vorhanden.")
            zutaten_speichern(vorhandene_zutaten)

#Zutat entfernen
        case "2":
            entfernende_zutat = input("Geben Sie die zu entfernende Zutat ein: ")
            for zutat in entfernende_zutat.split():
                if [zutat] in vorhandene_zutaten:
                    vorhandene_zutaten.remove([zutat])
                    print(f"{zutat} wurde entfernt.")
                else:
                    print(f"{zutat} ist nicht vorhanden.")
            zutaten_speichern(vorhandene_zutaten)

        case _: #ELSE
            print("Ungültige Auswahl.")

#Rezepte bearbeiten
def rezepte_bearbeiten():
    print("Möchten Sie ein Rezept hinzufügen (1) oder entfernen (2) oder bearbeiten (3)?")
    wahl = input("Eingabe: ")
    rezepte = rezepte_laden()
    match wahl:
        case "1": #Rezept hinzufügen
            rezeptname_neu = input("Geben Sie den Namen des neuen Rezepts ein: ")
            zutaten_neues_rezept = input("Geben Sie die Zutaten des Rezepts ein (durch Leerzeichen getrennt): ")
            zutaten_neu = zutaten_neues_rezept.split()
            rezepte[rezeptname_neu] = zutaten_neu
            rezepte_speichern(rezepte)
            print(f"Rezept '{rezeptname_neu}' wurde hinzugefügt.")

        case "2": #Rezept entfernen
            rezeptname = input("Geben Sie den Namen des neuen Rezepts ein: ")
            if rezeptname in rezepte:
                del rezepte[rezeptname]
                rezepte_speichern(rezepte)
                print(f"Rezept '{rezeptname}' wurde entfernt.")
            else:
                print(f"Rezept '{rezeptname}' nicht gefunden.")

        case "3": #Rezept bearbeiten
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

        case _: #ELSE
            print("Ungültige Auswahl.")

#Rezeptprüfung
def fehlende_zutaten(rezeptname):
  fehlend = []
  if rezeptname not in rezepte:
    return f"Rezept '{rezeptname}' nicht gefunden!"
  benoetigt = rezepte[rezeptname]
  for zutat in benoetigt:
    if [zutat] not in vorhandene_zutaten:
      fehlend.append(zutat)

  if fehlend is not None:
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

    print("Wähle 1 zum Zutaten bearbeiten!")
    print("Wähle 2 zum Rezepte bearbeiten!")
    print("Wähle 3 zum Rezepte überprüfen!")
    print("Wähle 9 zum Beenden!")
    modus = input("Modus: ")

    match modus:
        case "1":
            print("Vorhandene Zutaten:")
            print(vorhandene_zutaten)
            zutaten_bearbeiten()
            vorhandene_zutaten = zutaten_laden()
            print(vorhandene_zutaten)
        case "2":
            print("Verfügbare Rezepte:")
            print(rezepte)
            rezepte_bearbeiten()
        case "3":
            print("Wählen Sie ein Rezept der folgenden Auswahl:")
            print(rezepte_liste)
            rezept_wunsch = input("Rezeptname: ")
            print(fehlende_zutaten(rezept_wunsch))
        case "9":
            break
        case _:
            print("Ungültige Eingabe.")

