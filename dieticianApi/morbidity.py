from flask import request
from flask_restx import Resource,Namespace, fields
from flask_login import login_required
import controller as dynamodb
import key_constants as PREFIX
import commonFunc as PRE_REQUISITE

api = Namespace("Morbidity API", description="All the API's for Morbidity Data")

morbidity_put_body = api.model('MorbidityPutApi', {
    'MorbidityMarkerRef': fields.String(required=True, description='Morbidity marker reference'),
    'MorbidityTestUnit': fields.String(required=True, description='The unit of morbidity test eg. mg/Dl')
})

morbidity_post_body = api.model('MorbidityPostApi', {
    'MorbidityName':fields.String(required=True, description='Name of the Morbidity'),
    'MorbidityTestName':fields.String(required=True, description='Name of the morbidity test'),
    'MorbidityMarkerRef': fields.String(required=True, description='Morbidity marker reference'),
    'MorbidityTestUnit': fields.String(required=True, description='The unit of morbidity test eg. mg/Dl')
})

class MorbidityApi(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @login_required
    def get(self):
        projectionexp = 'MorbidityName,MorbidityTestId,MorbidityTestName,MorbidityMarkerRef,MorbidityTestUnit'
        response = dynamodb.read_all('InfoType', 'Morbidity', projectionexp)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response and response['Count'] > 0:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }

    @api.doc(responses={200: 'Success', 400: 'Validation Error', 500: 'Internal Server Error'})
    @api.expect(morbidity_post_body)
    @login_required
    def post(self):
        data = request.get_json()

        # Json body validation
        status_flag = PRE_REQUISITE.validate_request_body(data, 'morbidity_post')

        if len(status_flag) == 0:
            # Check - duplication based on Morbidity Name , Test Name
            if dynamodb.check_morbidity_duplication(data['MorbidityName'], data['MorbidityTestName']) == 0:
                # Generate TsetID based on Morbidity Name ,Test Name
                auto_test_id = PRE_REQUISITE.generate_test_id(data['MorbidityName'], data['MorbidityTestName'])
                response = dynamodb.write_morbidity(auto_test_id,data)
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return {
                        'MorbidityTestId': auto_test_id,
                        'Message': 'Morbidity successful created.'
                    }
                return {

                    'MorbidityTestId': auto_test_id,
                    'MorbidityName': data['MorbidityName'],
                    'Message': 'Morbidity successful created.'
                }
            return {
                    'Message': 'error occurred'
                }
        return{
            'Message': 'Missing Items OR Invalid Entry.Check on ' + str(status_flag)

        }

    @api.doc(responses={200: 'Success', 400: 'Validation Error', 500: 'Internal Server Error'})
    @api.expect(morbidity_put_body)
    @api.doc(params={
        'MorbidityName': 'Name of the Morbidity',
        'MorbidityTestId': 'Test ID of the morbidity'
    })
    @login_required
    def put(self,MorbidityName,MorbidityTestId):
        data = request.get_json()
        # Json body validation
        status_flag = PRE_REQUISITE.validate_request_body(data, 'morbidity_put')
        if len(status_flag) == 0:
            response = dynamodb.update_morbidity(MorbidityName, MorbidityTestId, data)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'MorbidityTestId': MorbidityTestId,
                    'MorbidityName': MorbidityName,
                    'MorbidityMarkerRef': data['MorbidityMarkerRef'],
                    'MorbidityTestUnit': data['MorbidityTestUnit'],
                    'Message': 'Successfully Updated.',
                }
            return {
                'Message': 'error occurred',
                'response': response
            }
        return{
            'Message': 'Missing Items OR Invalid Entry.Check on ' + str(status_flag)
        }

    @api.doc(responses={200: 'Success', 400: 'Validation Error', 404: 'Not Found'})
    @api.doc(params={
        'MorbidityName': 'Name of the Morbidity',
        'MorbidityTestId': 'Test ID of the morbidity'
    })
    @login_required
    def delete(self,MorbidityName,MorbidityTestId):
        # Check - Morbidity name, Test id are avilable in DB for delete
        response = dynamodb.check_morbidity_availability(MorbidityName, MorbidityTestId)
        if response > 0:
            response = dynamodb.delete_morbidity(MorbidityName, MorbidityTestId)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'MorbidityName': MorbidityName,
                    'MorbidityTestId': MorbidityTestId,
                    'Message': 'Successfully Deleted.'
                }
            return {
                'Message': 'error occurred',
                'response': response
            }
        return{
            'Message': 'Already Deleted OR wrong MorbidityName ,MorbidityTestId.'
        }
class MorbidityNameApi(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @api.doc(params={'MorbidityName': 'Name of the Morbidity'})
    @login_required
    def get(self,MorbidityName):
        projectionexp = 'MorbidityName,MorbidityTestId,MorbidityTestName,MorbidityMarkerRef,MorbidityTestUnit'
        pk_value = PREFIX.MORBIDITY_PK_PREFIX + MorbidityName
        response = dynamodb.read_using_PK(pk_value, projectionexp)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response and response['Count'] > 0:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }

class MorbidityTestIDApi(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error',401: 'Unauthorised Acces',404:'Not Found'})
    @api.doc(params={'MorbidityTestId': 'Test ID of the morbidity'})
    @login_required
    def get(self,MorbidityTestId):
        projectionexp = 'MorbidityName,MorbidityTestId,MorbidityTestName,MorbidityMarkerRef,MorbidityTestUnit'
        response = dynamodb.read_attr_that_contains_value('MorbidityTestId', MorbidityTestId, projectionexp)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response and response['Count'] > 0:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }


#endpoints for Morbidity
api.add_resource(MorbidityNameApi, '/MorbidityName=<MorbidityName>', methods=['GET'])
api.add_resource(MorbidityTestIDApi, '/MorbidityTestId=<MorbidityTestId>', methods=['GET'])
api.add_resource(MorbidityApi, '/MorbidityName=<MorbidityName>&MorbidityTestId=<MorbidityTestId>', methods=['PUT','DELETE'])
api.add_resource(MorbidityApi, '/', methods=['GET','POST'])




