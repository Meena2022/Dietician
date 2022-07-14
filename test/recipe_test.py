import pytest
import requests
import json
from base import ConfigBase as config


def test_1_get_recipes():
    response = requests.get(config.USER_ENDPOINT)
    assert response.status_code == 200
    assert response.content, "application/json"
    assert isinstance(response.json, object)


@pytest.mark.parametrize("foodCategory,result", [('Vegetarian', 200)])
def test_2_recipe_foodCategory(foodCategory, result):
    endpoint = config.RECIPE_FOODCATG_ENDPOINT.format(foodCategory)
    response = requests.get(endpoint)
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
    endpoint = config.RECIPE_INGR_ENDPOINT.format(ingredient)
    response = requests.get(endpoint)
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
    endpoint = config.RECIPE_NUTRI_ENDPOINT.format(nutrient)
    response = requests.get(endpoint)
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
    endpoint = config.RECIPE_RTYPE_ENDPOINT.format(type)
    response = requests.get(endpoint)
    responsebody = response.json()
    assert response.status_code == result
    assert response.content, "application/json"
    assert isinstance(response.json, object)
    assert ("RecipeName" in responsebody["Items"][0].keys()), True
    assert ("RecipeStep" in responsebody["Items"][0].keys()), True
    assert ("RecipeType" in responsebody["Items"][0].keys()), True
    assert ("RecipeFoodCategory" in responsebody["Items"][0].keys()), True
    assert ("RecipeId" in responsebody["Items"][0].keys()), True