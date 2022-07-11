from flask import request
from flask_restful import Resource
import controller as dynamodb
import key_constants as PREFIX
import commonFunc as PRE_REQUISITE


class MorbidityApi(Resource):
    def get(self,morbidityName=None,morbidityTestId=None):
        projectionexp = 'MorbidityName,MorbidityTestId,MorbidityTestName,MorbidityMarkerRef,MorbidityTestUnit'
        if morbidityName.__ne__(None) :
            pk_value = PREFIX.MORBIDITY_PK_PREFIX + morbidityName
            response = dynamodb.read_using_PK(pk_value,projectionexp)
        elif request.args.__contains__('MorbidityName'):
            value = request.args.get('MorbidityName')
            pk_value = PREFIX.MORBIDITY_PK_PREFIX + str(value)
            response = dynamodb.read_using_PK(pk_value,projectionexp)
        elif morbidityTestId.__ne__(None):
            response = dynamodb.read_attr_that_contains_value('MorbidityTestId',morbidityTestId, projectionexp)
        elif request.args.__contains__('MorbidityTestId'):
            value = request.args.get('MorbidityTestId')
            response = dynamodb.read_attr_that_contains_value('MorbidityTestId',value, projectionexp)
        else:
            response = dynamodb.read_all('InfoType','Morbidity',projectionexp)

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
        status_flag = PRE_REQUISITE.validate_request_body(data, 'morbidity')  # Coding not completed
        print('Status :', status_flag)
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

    def put(self):
        data = request.get_json()
        morbidity_name = request.args.get('MorbidityName')
        test_id = request.args.get('MorbidityTestId')
        print('nane :', morbidity_name, test_id)
        if isinstance(morbidity_name, type(None)) == False and isinstance(test_id, type(None)) == False:
            response = dynamodb.update_morbidity(morbidity_name, test_id, data)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'Message': 'update successful',
                }
            return {
                'Message': 'error occurred',
                'response': response
            }
        return{
            'Message': 'Missing request params - MorbidityName and MorbidityTestId.'
        }

    def delete(self):
        morbidity_name = request.args.get('MorbidityName')
        test_id = request.args.get('MorbidityTestId')
        print('nane :' , morbidity_name, test_id)
        if isinstance(morbidity_name, type(None)) == False and isinstance(test_id, type(None)) == False:
            response = dynamodb.delete_morbidity(morbidity_name, test_id)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'MorbidityName': morbidity_name,
                    'MorbidityTestId': test_id,
                    'Message': 'Test successful deleted.'
                }
            return {
                'Message': 'error occurred',
                'response': response
            }
        return{
            'Message': 'Missing request params - MorbidityName and MorbidityTestId.'
        }




