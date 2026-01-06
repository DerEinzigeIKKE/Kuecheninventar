# Projektarbeit WiSe 25/26 Programmieren mit Python
# Kuecheninventar
Python Projektarbeit mit Inventarverwaltung, Rezeptverwaltung und Rezeptabgleich

# TODO
- GUI :/
+ Funktionen vereinzeln
+ Hardcode durch Variablen in oberen Teil der Main ersetzen (z.B. Speicheradressen)

# Inventar 
CSV mit allen Zutaten (1 Zutat pro Zeile)

# Rezepte
JSON im Format {"Rezept1": ["Zutat1","Zutat2","Zutat3","Zutat4","Zutat5"],"Rezept2": ["Zutat1","Zutat2","Zutat3","Zutat4","Zutat5"]}

# Functions

## Ingredients
+ load: ingredients_load()
+ save: ingredients_save(ingredient_list) -> parameter: list
+ add:  ingredient_add(ingredients_toadd) -> parameter: string (from input)
+ remove: ingredient_delete(ingretdients_todelete) -> parameter: string (from input)


## Recipes
+ load: recipes_load()
+ save: recipes_save(recipes) -> parameter: dictionary
+ add:  recipes_add(new_name, new_ingredients) -> parameters: string, string (from input)
+ remove: recipes_delete(recipe_name) -> parameter: string (from input)
+ update name: recipes_update_name(old_name, new_name) -> parameter: string, string (from input)
+ update ingredient: recipes_update_ingredients(recipe_name, new_ingredients) -> parameter: string, string (from input)
+ show: recipes_display(recipe_name) -> parameter: string (from input)

## Comparison
+ recipes_check(recipe_name) -> parameter: string (from input)
