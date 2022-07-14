
from flask import request,jsonify
from flask_restx import Resource,Namespace, fields
from flask_login import login_required
import controller as dynamodb
import commonFunc as PRE_REQUISITE
import key_constants as PREFIX

api = Namespace("Users API", description="All the API's for User Data")

address_field = {}
address_field['Address1'] = fields.String(readOnly=True, description='Address line 1')
address_field['Address2'] = fields.String(readOnly=True, description='Address line 2')
address_field['City'] = fields.String(readOnly=True, description='City of the user')
address_field['State'] = fields.String(readOnly=True, description='State of the user')
address_field['Country'] = fields.String(readOnly=True, description='Country of the user')


users_put_body = api.model('UsersPutApi', {
    'FirstName': fields.String(required=True, description='First Name of the user'),
    'LastName': fields.String(required=True, description='Last Name of the user'),
    'Address': fields.Nested(api.model('address_field', address_field)),
    'Contact': fields.String(required=True, description='Contact number of the user'),
    'Email': fields.String(required=True, description='Email Address of the user'),
    'FoodCategory': fields.String(required=True, description='FoodCategory of the user'),
    'Allergy': fields.String(required=True, description="User's Allergy"),
})

users_post_body = api.clone('UsersPostApi',users_put_body, {
    'LoginUsername': fields.String(required=True, description='Login user name'),
    'Password': fields.String(required=True, description='Password'),
    'UserType': fields.String(required=True, description='Type of user'),
    'DieticianId': fields.String(required=True, description='ID of the Dietician'),
})

class UsersApi(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @login_required
    def get(self):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_all('InfoType', 'User', projectionexp)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }

    @api.doc(responses={200: 'Success', 400: 'Validation Error', 500: 'Internal Server Error'})
    @api.expect(users_post_body)
    @login_required
    def post(self):
        data = request.get_json()

        # Json body validation
        status_flag  = PRE_REQUISITE.validate_request_body(data, 'user_post')
        if len(status_flag) == 0:
            # Check - duplication based on Firstname , Contact , Email
            if dynamodb.check_user_duplication(data['FirstName'], data['Contact'], data['Email']) == 0:
                # Generate UserID based on Usertype
                auto_user_id = PRE_REQUISITE.generate_user_id(data['UserType'])  # Auto

                if bool(auto_user_id):
                    if data['UserType'] == 'Dietician': data['DieticianId'] = auto_user_id
                    response = dynamodb.write_user(auto_user_id, data)
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        return {
                                'UserId': auto_user_id,
                                'Message': 'Successfully Created.'

                        }
                    return {
                        'Message': 'error occurred',
                        'response': response
                    }
            return {
                'Message': 'User detail already Exists. Check on [ Firstname, Contact , Email ]'
            }
        return{
            'Message': 'Missing Items OR Invalid Entry. Check on ' + str(status_flag)
        }

    @api.doc(responses={200: 'Success', 400: 'Validation Error', 500: 'Internal Server Error'})
    @api.expect(users_put_body)
    @api.doc(params={
        'DieticianId': 'Id of the Dietician',
        'UserId': 'Type of the user'
    })
    @login_required
    def put(self,DieticianId,UserId):
        data = request.get_json()
        # Json body validation
        status_flag = PRE_REQUISITE.validate_request_body(data, 'user_put')
        if len(status_flag) == 0:
            response = dynamodb.update_user(DieticianId, UserId, data)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'UserId' : UserId,
                    'FirstName': data['FirstName'],
                    'Message': 'User updated successful',
                    }
            return {
                'Message': 'error occurred',
                'response': response
            }
        return {
            'Message': 'Missing Items OR Invalid Entry.Check on ' + str(status_flag)
        }

    @api.doc(responses={200: 'Success', 400: 'Validation Error',404:'Not Found'})
    @api.doc(params={
        'DieticianId': 'Id of the Dietician',
        'UserId': 'Type of the user'
    })
    @login_required
    def delete(self,DieticianId,UserId):
        # Check - Dieticianid, Userid are avilable in DB for delete
        response = dynamodb.check_user_availability(DieticianId,UserId)
        if response > 0:
            response = dynamodb.delete_user(DieticianId, UserId)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'DieticianId': DieticianId,
                    'UserId': UserId,
                    'Message': 'Successfully Deleted.'
                }
            return {
                'Message': 'error occurred',
                'response': response
            }
        return{
            'Message' : 'Already Deleted OR wrong DieticinaId ,UserId.'
        }


class UserFirstNameAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @api.doc(params={'FirstName': 'First Name of the user'})
    @login_required
    def get(self,FirstName):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_attr_that_contains_value('FirstName', FirstName, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class UserEmailAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @api.doc(params={'Email': 'Email of the user'})
    @login_required
    def get(self,Email):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_attr_that_contains_value('Email', Email, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class UserContactAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @api.doc(params={'Contact': 'Contact of the user'})
    @login_required
    def get(self,Contact):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_attr_that_contains_value('Contact', Contact, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class UserTypeAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @api.doc(params={'UserType': 'Type of the user eg. Dietician / Patient'})
    @login_required
    def get(self,UserType):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_attr_that_contains_value('UserType', UserType, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class UserDieticianIdAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @api.doc(params={'DieticianId': 'Id of the Dietician'})
    @login_required
    def get(self, DieticianId):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_all('DieticianId', DieticianId, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

#endpoints for User
api.add_resource(UserFirstNameAPI, '/FirstName=<FirstName>', methods=['GET'])
api.add_resource(UserEmailAPI, '/Email=<Email>', methods=['GET'])
api.add_resource(UserContactAPI, '/Contact=<Contact>', methods=['GET'])
api.add_resource(UserTypeAPI, '/UserType=<UserType>', methods=['GET'])
api.add_resource(UserDieticianIdAPI, '/DieticianId=<DieticianId>', methods=['GET'])
api.add_resource(UsersApi, '/DieticianId=<DieticianId>&UserId=<UserId>', methods=['PUT','DELETE'])
api.add_resource(UsersApi, '/', methods=['GET','POST'])