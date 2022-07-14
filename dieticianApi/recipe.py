from flask_restx import Resource,Namespace
import controller as dynamodb

api = Namespace("Recipe API", description="All the API's for getting Recipe Data")

class RecipeApi(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    def get(self):
        projectionexp = "RecipeId, RecipeFoodCategory, RecipeType, RecipeName, RecipeIngredient, RecipeNutrient, RecipeStep, RecipeUrl , RecipeImg"
        result = dynamodb.read_all('InfoType', 'Recipe',projectionexp)
        response = dynamodb.replace_decimals(result)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if 'Items' in response and response['Count'] > 0:
                return {'Items': response['Items']}
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class RecipeFoodCategoryAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'RecipeFoodCategory': 'Category of the Recipe Vegetarian / Non-Vegetarian'})
    def get(self,RecipeFoodCategory):
        projectionexp = "RecipeId, RecipeFoodCategory, RecipeType, RecipeName, RecipeIngredient, RecipeNutrient, RecipeStep, RecipeUrl , RecipeImg"
        response = dynamodb.read_all('RecipeFoodCategory', RecipeFoodCategory, projectionexp)
        response = dynamodb.replace_decimals(response)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if 'Items' in response and response['Count'] > 0:
                return {'Items': response['Items']}
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class RecipeTypeAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'RecipeType': 'Type of the recipe Lunch / Dinner / Snack / Main Course'})
    def get(self,RecipeType):
        projectionexp = "RecipeId, RecipeFoodCategory, RecipeType, RecipeName, RecipeIngredient, RecipeNutrient, RecipeStep, RecipeUrl , RecipeImg"
        response = dynamodb.read_all('RecipeType', RecipeType, projectionexp)
        response = dynamodb.replace_decimals(response)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if 'Items' in response and response['Count'] > 0:
                return {'Items': response['Items']}
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class RecipeIngredientAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'RecipeIngredient': 'One of the ingredient of the recipe eg. Paneer'})
    def get(self,RecipeIngredient):
        projectionexp = "RecipeId, RecipeFoodCategory, RecipeType, RecipeName, RecipeIngredient, RecipeNutrient, RecipeStep, RecipeUrl , RecipeImg"
        response = dynamodb.read_attr_that_contains_value('RecipeIngredient', RecipeIngredient, projectionexp)
        response = dynamodb.replace_decimals(response)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if 'Items' in response and response['Count'] > 0:
                return {'Items': response['Items']}
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class RecipeNutrientAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'RecipeNutrient': 'Nutrient content of the recipe eg. Energy 56 cal'})
    def get(self,RecipeNutrient):
        projectionexp = "RecipeId, RecipeFoodCategory, RecipeType, RecipeName, RecipeIngredient, RecipeNutrient, RecipeStep, RecipeUrl , RecipeImg"
        response = dynamodb.read_attr_that_contains_value('RecipeNutrient', RecipeNutrient, projectionexp)
        response = dynamodb.replace_decimals(response)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if 'Items' in response and response['Count'] > 0:
                return {'Items': response['Items']}
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

#endpoints for Recipe
api.add_resource(RecipeApi, '/', methods=['GET'])
api.add_resource(RecipeFoodCategoryAPI, '/RecipeFoodCategory=<RecipeFoodCategory>', methods=['GET'])
api.add_resource(RecipeTypeAPI, '/RecipeType=<RecipeType>', methods=['GET'])
api.add_resource(RecipeIngredientAPI, '/RecipeIngredient=<RecipeIngredient>', methods=['GET'])
api.add_resource(RecipeNutrientAPI, '/RecipeNutrient=<RecipeNutrient>', methods=['GET'])