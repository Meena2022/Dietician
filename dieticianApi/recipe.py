from flask import request
from flask_restful import Resource
import controller as dynamodb

class RecipeApi(Resource):
    def get(self,recipeFoodCategory=None,recipeType=None,recipeIngredient=None,recipeNutrient=None):
        projectionexp = "RecipeId, RecipeFoodCategory, RecipeType, RecipeName, RecipeIngredient, RecipeNutrient, RecipeStep, RecipeUrl , RecipeImg"
        if recipeFoodCategory.__ne__(None):
            response = dynamodb.read_all('RecipeFoodCategory', recipeFoodCategory, projectionexp)
        elif request.args.__contains__('RecipeFoodCategory'):
            value = request.args.get('RecipeFoodCategory')
            response = dynamodb.read_all('RecipeFoodCategory', value, projectionexp)
        elif recipeType.__ne__(None):
            response = dynamodb.read_all('RecipeType', recipeType, projectionexp)
        elif request.args.__contains__('RecipeType'):
            value = request.args.get('RecipeType')
            response = dynamodb.read_all('RecipeType', value, projectionexp)
        elif recipeIngredient.__ne__(None):
            response = dynamodb.read_attr_that_contains_value('RecipeIngredient', recipeIngredient, projectionexp)
        elif request.args.__contains__('RecipeIngredient'):
            value = request.args.get('RecipeIngredient')
            response = dynamodb.read_attr_that_contains_value('RecipeIngredient', value, projectionexp)
        elif recipeNutrient.__ne__(None):
            response = dynamodb.read_attr_that_contains_value('RecipeNutrient', recipeNutrient, projectionexp)
        elif request.args.__contains__('RecipeNutrient'):
            value = request.args.get('RecipeNutrient')
            response = dynamodb.read_attr_that_contains_value('RecipeNutrient', value, projectionexp)
        else:
            response = dynamodb.read_all('InfoType', 'Recipe',projectionexp)
        response = dynamodb.replace_decimals(response)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }