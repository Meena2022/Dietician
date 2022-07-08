from flask import request
from flask_restful import Resource
import controller as dynamodb
import key_constants as PREFIX


class MorbidityApi(Resource):
    def get(self):
        if request.args.__contains__('MorbidityName'):
            key = 'MorbidityName'
            value = request.args.get('MorbidityName')
            print(key, value)
        if request.args.__contains__('MorbidityTestId'):
            key = 'MorbidityTestId'
            value = request.args.get('MorbidityTestId')
        else:
            key = 'None'
            value = 'None'
        response = dynamodb.read_morbidity(key, value)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }

    def post(self):
        # data['MorbidityName'],data['MorbidityTestName'],data['MorbidityMarkerRef'],data[MorbidityTestUnit]
        data = request.get_json()
        auto_test_id = PREFIX.generate_test_id(data['MorbidityName'], data['MorbidityTestName'])
        response = dynamodb.write_morbidity(data)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'MorbidityTestId': auto_test_id,
                'Message': 'Morbidity successful created.'
            }
        return {
            'Message': 'error occurred',
            'response': response
        }

    def put(self):
        data = request.get_json()
        if request.args.__contains__('MorbidityName'):
            morbidity_name = request.args.get('MorbidityName')
        if request.args.__contains__('MorbidityTestId'):
            test_id = request.args.get('MorbidityTestId')
        else:
            morbidity_name = 'None'
            test_id = 'None'
        response = dynamodb.update_morbidity(morbidity_name, test_id, data)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'Message': 'update successful',
                'ModifiedAttributes': response['Attributes']
            }
        return {
            'Message': 'errooccurred',
            'response': response
        }

    def delete(self):
        morbidity_name = request.args.get('MorbidityName')
        test_id = request.args.get('MorbidityTestId')
        print('nane :' + request.args.get('MorbidityName'), test_id)
        response = dynamodb.delete_morbidity(morbidity_name, test_id)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                # 'MorbidityName': morbidity_name,
                # 'MorbidityTestId': test_id,
                'Message': 'Test successful deleted.'
            }
        return {
            'Message': 'error occurred',
            'response': response
        }


