from flask import request
from flask_restx import Resource,Namespace, fields
import controller as dynamodb
import key_constants as PREFIX
import commonFunc as PRE_REQUISITE

api = Namespace("Morbidity API", description="All the API's for Morbidity Data")

morbidity_put = api.model('MorbidityApi', {
    'MorbidityMarkerRef': fields.String(required=True, description='Morbidity marker reference'),
    'MorbidityTestUnit': fields.String(required=True, description='The unit of morbidity test eg. mg/Dl')
})

class MorbidityApi(Resource):
    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    def get(self):
        projectionexp = 'MorbidityName,MorbidityTestId,MorbidityTestName,MorbidityMarkerRef,MorbidityTestUnit'
        response = dynamodb.read_all('InfoType', 'Morbidity', projectionexp)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }

    def post(self):
        data = request.get_json()
        status_flag = PRE_REQUISITE.validate_request_body(data, 'morbidity')  # Coding not completed

        if len(status_flag) == 0:
            auto_test_id = PRE_REQUISITE.generate_test_id(data['MorbidityName'], data['MorbidityTestName'])
            print('id :', auto_test_id)
            response = dynamodb.write_morbidity(auto_test_id,data)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'MorbidityTestId': auto_test_id,
                    'Message': 'Morbidity successful created.'
                }
            return {
                    'Message': 'error occurred',
                    'response': response
                }
        return{
                'Message': 'Missing Items OR Invalid Entry.Check on ' + str(status_flag)
            }

    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    @api.expect(morbidity_put)
    @api.doc(params={
        'MorbidityName': 'Name of the Morbidity',
        'MorbidityTestId': 'Test ID of the morbidity'
    })
    def put(self,MorbidityName,MorbidityTestId):
        data = request.get_json()

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

    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    @api.doc(params={
        'MorbidityName': 'Name of the Morbidity',
        'MorbidityTestId': 'Test ID of the morbidity'
    })
    def delete(self,MorbidityName,MorbidityTestId):
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

class MorbidityNameApi(Resource):
    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'MorbidityName': 'Name of the Morbidity'})
    def get(self,MorbidityName):
        projectionexp = 'MorbidityName,MorbidityTestId,MorbidityTestName,MorbidityMarkerRef,MorbidityTestUnit'
        pk_value = PREFIX.MORBIDITY_PK_PREFIX + MorbidityName
        response = dynamodb.read_using_PK(pk_value, projectionexp)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }

class MorbidityTestIDApi(Resource):
    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'MorbidityTestId': 'Test ID of the morbidity'})
    def get(self,MorbidityTestId):
        projectionexp = 'MorbidityName,MorbidityTestId,MorbidityTestName,MorbidityMarkerRef,MorbidityTestUnit'
        response = dynamodb.read_attr_that_contains_value('MorbidityTestId', MorbidityTestId, projectionexp)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response:
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




