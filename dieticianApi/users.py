from flask import request
from flask_restful import Resource
import controller as dynamodb
import commonFunc as PRE_REQUISITE


class UsersApi(Resource):
    def get(self, FirstName=None, Email=None, Contact=None, UserType=None, DieticianId=None):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        if request.args.__contains__('FirstName'):
            value = request.args.get('FirstName')
            response = dynamodb.read_attr_that_contains_value('FirstName', value, projectionexp)
        elif FirstName.__ne__(None):
            response = dynamodb.read_attr_that_contains_value('FirstName', FirstName, projectionexp)
        elif request.args.__contains__('Email'):
            value = request.args.get('Email')
            response = dynamodb.read_attr_that_contains_value('Email', value, projectionexp)
        elif Email.__ne__(None):
            response = dynamodb.read_attr_that_contains_value('Email', Email, projectionexp)
        elif request.args.__contains__('Contact'):
            value = request.args.get('Contact')
            response = dynamodb.read_attr_that_contains_value('Contact', value, projectionexp)
        elif Contact.__ne__(None):
            response = dynamodb.read_attr_that_contains_value('Contact', Contact, projectionexp)
        elif request.args.__contains__('UserType'):
            value = request.args.get('UserType')
            response = dynamodb.read_attr_that_contains_value('UserType', value, projectionexp)
        elif UserType.__ne__(None):
            response = dynamodb.read_attr_that_contains_value('UserType', UserType, projectionexp)
        elif request.args.__contains__('DieticianId'):
            value = request.args.get('DieticianId')
            response = dynamodb.read_attr_that_contains_value('DieticianId', value, projectionexp)
        elif DieticianId.__ne__(None):
            response = dynamodb.read_attr_that_contains_value('DieticianId', DieticianId, projectionexp)
        else:
            response = dynamodb.read_all('InfoType', 'User', projectionexp)

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }

    def post(self):
        # data['InfoType'],data['UserId'],data['FirstName'],data['LastName'],data['Address'],data['Contact']
        # data['Email'],data['Allergy'],data['FoodCategory'],data['DieticianId'],data['LoginUsername'],data['Password']
        data = request.get_json()
        status_flag  = PRE_REQUISITE.validate_request_body(data,'user')  # Coding not completed
        print ('Status :',status_flag)
        if len(status_flag)==0:
            auto_user_id = PRE_REQUISITE.generate_user_id(data['UserType'])
            if data['UserType']=='Dietician': data['DieticianId']=auto_user_id
            if bool(auto_user_id):
                response = dynamodb.write_user(auto_user_id, data)
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return {
                        'UserId': auto_user_id,
                        'Message': 'User successful created.'
                    }
                return {
                    'Message': 'error occurred',
                    'response': response
                }
        return {
                'Message': 'Missing Items OR Invalid Entry.Check on ' + str(status_flag)
              }


    def put(self):
        # data['FirstName'],data['LastName'],data['Address'],data['Contact'],data['Email'],data['Allergy'],data['FoodCategory']
        data = request.get_json()
        dietician_id = request.args.get('DieticianId')
        user_id = request.args.get('UserId')
        if isinstance(dietician_id, type(None))==False  and isinstance(user_id, type(None))==False:
            response = dynamodb.update_user(dietician_id, user_id, data)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'Message': 'User updated successful',
                    'ModifiedAttributes': response['Attributes']
                }
            return {
                'Message': 'error occurred',
                'response': response
            }
        return {
                'Message': 'Missing request params - DiceticianId and UserId.'
            }

    def delete(self):
        #delete_user
        dietician_id = request.args.get('DieticianId')
        user_id = request.args.get('UserId')
        print (isinstance(dietician_id, type(None)),isinstance(user_id, type(None)))
        if isinstance(dietician_id, type(None)) == False and isinstance(user_id, type(None)) == False:
            print(dietician_id, user_id)
            response = dynamodb.delete_user(dietician_id, user_id)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'DieticianId': dietician_id,
                    'UserId': user_id,
                    'Message': 'User successful deleted.'
                }
            return {
                'Message': 'error occurred',
                'response': response
            }
        return {
                'Message': 'Missing request params - DieticianId and UserId.'
            }