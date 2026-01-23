import json
import csv

#Set Adresses
ADRESS_RECIPE = "rezepte.json"
ADRESS_INGREDIENT = "zutaten.csv"

#load ingredients as list from ADRESS_INGREDIENT
def ingredients_load():
    available_ingredients = []
    with open(ADRESS_INGREDIENT, mode="r") as f:
        reader = csv.reader(f)
        for line in reader:
            #only import not empty rows
            if line:
                available_ingredients.append(line)
    return available_ingredients

#save ingredients as CSV in ADRESS_INGREDIENT
def ingredients_save(ingredient_list: list):
    #empty csv
    with open(ADRESS_INGREDIENT, 'w', newline='', encoding='utf-8') as f:
        pass
    #save passed ingredient_list in csv
    with open(ADRESS_INGREDIENT, mode="w") as f:
                writer = csv.writer(f)
                for line in ingredient_list:
                    #check if line contains ingredient
                    if line not in (None, "", []):
                        writer.writerow(line)

#load recipes from ADRESS_RECIPE
def recipes_load():
    with open(ADRESS_RECIPE, "r") as f:
        recipes = json.load(f)
    return recipes

#save recipes as JSON in ADRESS_RECIPE
def recipes_save(recipes: dict):
    with open(ADRESS_RECIPE, "w") as f:
        json.dump(recipes, f, indent=4)

def normalize_string(string):
    #String to all caps
    string_normalized = string.upper()
    return string_normalized

def normalize_list(inputstring):
    ingredient_list = []
    for ingredient in inputstring.split():
        ingredient_normalized = normalize_string(ingredient)
        ingredient_list.append(ingredient_normalized)
    return ingredient_list

def ingredient_add(ingredients_toadd):
    #load available ingredients
    available_ingredients = ingredients_load()
    #set lists for return messages
    ingredients_added = []
    ingredients_doubled = []
    #check if new ingredient(s) is/are already in the inventory
    for ingredient in ingredients_toadd.split():
        #normalize ingredient
        ingredient_normalized = normalize_string(ingredient)
        #if ingredient is new -> add to inventory_list and return_list
        if ingredient_normalized and [ingredient_normalized] not in available_ingredients:
            available_ingredients.append([ingredient_normalized])
            ingredients_added.append(ingredient)
        #if ingredient is alredy in inventory -> add to return_list_double
        else:
            ingredients_doubled.append(ingredient)
    ingredients_save(available_ingredients)
    #define return cases
    #added new ingredients & had double ingredients
    if len(ingredients_doubled) > 0 and len(ingredients_added) > 0:
        return f"Alredy available ingredients: {', '.join(ingredients_doubled)}!\nAdded ingredients: {', '.join(ingredients_added)}!"
    #added new ingredients
    if len(ingredients_doubled) == 0 and len(ingredients_added) > 0:
        return f"Added ingredients: {', '.join(ingredients_added)}!"
    #had double ingredients
    if len(ingredients_doubled) > 0 and len(ingredients_added) == 0:
        return f"Alredy available ingredients: {', '.join(ingredients_doubled)}!"
    #nothing
    if len(ingredients_doubled) == 0 and len(ingredients_added) == 0:
        return "Nothing happened."

#Zutatenliste bearbeiten
def ingredients_delete(ingredients_todelete):
    #load available ingredients
    available_ingredients = ingredients_load()
    #set lists for return messages
    ingredients_deleted = []
    ingredients_notfound = []
    #check if ingredient to delete is in available ingredients
    for ingredient in ingredients_todelete.split():
        #normalize ingredient
        ingredient_normalized = normalize_string(ingredient)
        #if ingredient is available -> remove from inventory_list and add to return_list
        if [ingredient_normalized] in available_ingredients:
            available_ingredients.remove([ingredient_normalized])
            ingredients_deleted.append(ingredient)
        #if ingredient is not available -> add to return_list
        else:
            ingredients_notfound.append(ingredient)
    ingredients_save(available_ingredients)
    #define return cases
    #ingredients removed & ingredients not found
    if len(ingredients_notfound) > 0 and len(ingredients_deleted) > 0:
        return f"Ingredients not found: {', '.join(ingredients_notfound)}!\nRemoved ingredients: {', '.join(ingredients_deleted)}!"
    #ingredients removed
    if len(ingredients_notfound) == 0 and len(ingredients_deleted) > 0:
        return f"Removed ingredients: {', '.join(ingredients_deleted)}!"
    #ingredients not found
    if len(ingredients_notfound) > 0 and len(ingredients_deleted) == 0:
        return f"Ingredients not found: {', '.join(ingredients_notfound)}!"
    #nothing
    if len(ingredients_notfound) == 0 and len(ingredients_deleted) == 0:
        return "Nothing happened."
    
#Add Recipes
def recipes_add(new_name, new_ingredients):
    #load available recipes
    recipes = recipes_load()
    #normalize name
    name_normalized = normalize_string(new_name)
    #check if new name is already in recipes
    if name_normalized in recipes:
        return f"recipe '{new_name}' alredy exists!"
    #ingredients to list
    ingredient_list = normalize_list(new_ingredients)
    #append recipes with new recipe & new ingredinets
    recipes[name_normalized] = ingredient_list
    #Save recipes
    recipes_save(recipes)
    return f"Recipe '{new_name}' was added."

#delete recipe
def recipes_delete(recipe_name):
    #load available recipes
    recipes = recipes_load()
    #normalize name
    name_normalized = normalize_string(recipe_name)
    #check if recipe is in saved recipes
    if name_normalized in recipes:
        del recipes[name_normalized]
        recipes_save(recipes)
        return f"Recipe '{recipe_name}' was removed."
    #if recipe is unknown
    else:
        return f"Recipe '{recipe_name}' was not found."

#update recipe name
def recipes_update_name(old_name, new_name):
    #load available recipes
    recipes = recipes_load()
    #normalze names
    old_normalized = normalize_string(old_name)
    new_normalized = normalize_string(new_name)
    #check if recipe exists
    if old_name in recipes:
        #load ingredients from recipe
        ingredients = recipes[old_normalized]
        #save recipe with new name
        recipes[new_normalized] = ingredients
        #delete old recipe
        del recipes[old_normalized]
        #save recipes
        recipes_save(recipes)
        return f"Recipe '{old_name}' changed to {new_name}."
    else:
        return f"Recipe '{old_name}' not found."
    
#update recipe ingredients
def recipes_update_ingredients(recipe_name, new_ingredients):
    #load available recipes
    recipes = recipes_load()
    #normalize name
    name_normalized = normalize_string(recipe_name)
    #check if recipe exists
    if name_normalized in recipes:
        ingredient_list = normalize_list(new_ingredients)
        #Update ingredients for recipes
        recipes[name_normalized] = ingredient_list
        #save recipes
        recipes_save(recipes)
        return f"Updated ingredients for '{recipe_name}'."
    else:
        return f"Recipe '{recipe_name}' not found."

#display 1 recipe
def recipes_display(recipe_name):
    #load available recipes
    recipes = recipes_load()
    #normalize name
    name_normalized = normalize_string(recipe_name)
    #check if recipe
    if name_normalized in recipes:
        #get needed ingredients
        ingredients = recipes[name_normalized]
        #return
        return f"Recipe '{recipe_name}' needs: {', '.join(ingredients)}"
    else:
        return f"Rezept '{recipe_name}' nicht gefunden."

#check recipes
def recipes_check(recipe_name):
    missing_ingredients = []
    #load available recipes
    recipes = recipes_load()
    #normalize name
    name_normalized = normalize_string(recipe_name)
    #load available ingredients
    available_ingredients = ingredients_load()
    #check if recipe exists
    if name_normalized not in recipes:
        return f"Recipe '{recipe_name}' not found!"
    #load needed ingredients
    needed_ingredients = recipes[name_normalized]
    #check for missing ingredients
    for ingredient in needed_ingredients:
        if [ingredient] not in available_ingredients:
            missing_ingredients.append(ingredient)
    #if missing ingredients exist
    if len(missing_ingredients) > 0:
        return f"Missing ingredients for {recipe_name}: {', '.join(missing_ingredients)}!"
    #if all ingredients are available
    else:
        return "All ingredients found!"

#Main
def main():
    print("Wellcome.")
    while True:
        print("\nPlease select a mode:\n")
        print("Choose 1 to add ingredients!")
        print("Choose 2 to remove ingredients!")
        print("Choose 3 to add recipe!")
        print("Choose 4 to delete recipe!")
        print("Choose 5 to update recipe name!")
        print("Choose 6 to update recipe ingredients!")
        print("Choose 7 to show 1 recipe!")
        print("Choose 8 to show all ingredients!")
        print("Choose 9 to show all recipe names!")
        print("Choose ENTER to compare recipe with available ingredients!")
        print("Choose 0 to end!\n")

        match input("Modus: "):
            case "1":#add ingredients
                ingredients = input("Enter the new ingredient(s): ")
                print(ingredient_add(ingredients))
            case "2":#remove ingredient
                ingredients = input("Enter the ingredient(s) which shall be removed: ")
                print(ingredients_delete(ingredients))
            case "3":#add recipe
                name = input("Enter the name of the recipe: ")
                ingredients = input("Enter the ingredients of the recipe: ")
                print(recipes_add(name, ingredients))
            case "4":#delete recipe
                name = input("Enter the recipe which shall be removed: ")
                recipes_delete(name)
            case "5":#recipe update name
                old_name = input("Enter the old name of the recipe: ")
                new_name = input("Enter the new name of the recipe: ")
                print(recipes_update_name(old_name, new_name))
            case "6":#recipe update ingredients
                name = input("Enter the name of the recipe: ")
                ingredients = input("Enter the new ingredientes of the recipe: ")
                print(recipes_update_ingredients(name, ingredients))
            case "7":#show 1 recipe
                name = input("Enter the name of the recipe: ")
                print(recipes_display(name))
            case "8":#show all ingredients
                ingredients = ingredients_load()
                ingredients = str(ingredients).replace("[","").replace("]","").replace("'","").split(", ")
                ingredients = str(ingredients).replace("'", "")
                print(ingredients)
            case "9":#show all recipes
                recipes = recipes_load()
                recipes_list = list(recipes.keys())
                print(recipes_list)
            case "0":#exit
                break
            case "":#recipes_check
                name = input("Enter the name of the recipe: ")                
                print(name)
                print(recipes_check(name))
            case _:#ELSE
                print("unvalid entry!")

if __name__ == "__main__":
    main()

