import pytest
import requests
import json


BASEURL = "http://127.0.0.1:5000/"

def test_1_get_recipes():
    recipe_url = "{}Recipes/".format(BASEURL)
    print(recipe_url)
    response = requests.get(recipe_url)
    print(response)
    assert response.status_code == 200
    print(response.status_code)
    assert response.content, "application/json"
    print(response.content)
    assert isinstance(response.json, object)


@pytest.mark.parametrize("foodCategory,result", [('Vegetarian', 200)])
def test_2_recipe_foodCategory(foodCategory, result):
    recipe_url_foodCategory = "{}Recipes/RecipeFoodCategory={}".format(BASEURL, foodCategory)
    response = requests.get(recipe_url_foodCategory)
    responsebody = response.json()
    assert response.status_code == result
    assert response.content, "application/json"
    assert isinstance(response.json, object)
    assert ("RecipeUrl" in responsebody["Items"][0].keys()), True
    assert ("RecipeName" in responsebody["Items"][0].keys()), True
    assert ("RecipeImg" in responsebody["Items"][0].keys()), True
    assert ("RecipeStep" in responsebody["Items"][0].keys()), True
    assert ("RecipeType" in responsebody["Items"][0].keys()), True
    assert ("RecipeId" in responsebody["Items"][0].keys()), True


@pytest.mark.parametrize("ingredient,result", [('Ajwain', 200), ('dal', 200), ('wheat', 200)])
def test_3_Recipe_Ingredient(ingredient, result):
    Recipe_Ingredient_url = "{}Recipes/RecipeIngredient={}".format(BASEURL, ingredient)
    response = requests.get(Recipe_Ingredient_url)
    responsebody = response.json()
    assert response.status_code == result
    assert response.content, "application/json"
    assert isinstance(response.json, object)
    assert ("RecipeName" in responsebody["Items"][0].keys()), True
    assert ("RecipeImg" in responsebody["Items"][0].keys()), True
    assert ("RecipeStep" in responsebody["Items"][0].keys()), True
    assert ("RecipeType" in responsebody["Items"][0].keys()), True
    assert ("RecipeFoodCategory" in responsebody["Items"][0].keys()), True
    assert ("RecipeId" in responsebody["Items"][0].keys()), True


@pytest.mark.parametrize("nutrient,result", [('Energy 56 cal', 200), ('Fiber 4 g', 200)])
def test_3_Recipe_nutrient(nutrient, result):
    Recipe_Nutrient_url = "{}Recipes/RecipeNutrient={}".format(BASEURL, nutrient)
    response = requests.get(Recipe_Nutrient_url)
    responsebody = response.json()
    assert response.status_code == result
    assert response.content, "application/json"
    assert isinstance(response.json, object)
    assert ("RecipeName" in responsebody["Items"][0].keys()), True
    assert ("RecipeImg" in responsebody["Items"][0].keys()), True
    assert ("RecipeStep" in responsebody["Items"][0].keys()), True
    assert ("RecipeType" in responsebody["Items"][0].keys()), True
    assert ("RecipeFoodCategory" in responsebody["Items"][0].keys()), True
    assert ("RecipeId" in responsebody["Items"][0].keys()), True

@pytest.mark.parametrize("type,result", [('Lunch', 200), ('Dinner', 200)])
def test_3_Recipe_type(type, result):
    Recipe_Type_url = "{}Recipes/RecipeType={}".format(BASEURL, type)
    response = requests.get(Recipe_Type_url)
    responsebody = response.json()
    assert response.status_code == result
    assert response.content, "application/json"
    assert isinstance(response.json, object)
    assert ("RecipeName" in responsebody["Items"][0].keys()), True
    assert ("RecipeStep" in responsebody["Items"][0].keys()), True
    assert ("RecipeType" in responsebody["Items"][0].keys()), True
    assert ("RecipeFoodCategory" in responsebody["Items"][0].keys()), True
    assert ("RecipeId" in responsebody["Items"][0].keys()), True