import decimal
from datetime import datetime
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from urllib3.connectionpool import xrange

import config
import key_constants as PREFIX


AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
ENDPOINT_URL = config.ENDPOINT_URL
# facet = config.FACET_DATA

resource = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
    endpoint_url=ENDPOINT_URL,
)

DietTable = resource.Table('DietProject_Table')


"""
COMMON METHODS
"""

def read_all(filterexp,filterexpval,projectionexp):
    response = DietTable.scan(
        FilterExpression=Key(filterexp).eq(filterexpval),
        ProjectionExpression=projectionexp
    )
    return response

def read_attr_that_contains_value(filterexp,filterexpval,projectionexp):
    response = DietTable.scan(
        FilterExpression=Attr(filterexp).contains(filterexpval),
        ProjectionExpression=projectionexp
    )
    return response

def read_using_PK(pk_value,projectionexp):
    response = DietTable.query(
        KeyConditionExpression=Key('PK').eq(pk_value),
        ProjectionExpression=projectionexp
    )
    return response


def generate_user_id():
    pass


def generate_recipe_id():
    pass

def generate_test_id(morbidity_name, test_name):
    test_id = morbidity_name[0:3] + '_' + test_name[0:3]
    return test_id.upper()


"""
MORBIDITY API - FUNCTIONS
"""

def write_morbidity(auto_test_id, data: dict):
    print(data)
    now = datetime.now().__str__()
    response = DietTable.put_item(
        Item={
            'PK': PREFIX.MORBIDITY_PK_PREFIX + data['MorbidityName'],
            'SK': PREFIX.MORBIDITY_SK_PREFIX + data['MorbidityTestName'],
            'InfoType': PREFIX.MORBIDITY_INFO,
            'MorbidityName': data['MorbidityName'],
            'MorbidityTestId': auto_test_id,
            'MorbidityTestName': data['MorbidityTestName'],
            'MorbidityMarkerRef': data['MorbidityMarkerRef'],
            'MorbidityTestunit': data['MorbidityTestunit'],
            'Createdon': now,
            'Modifiedon': now
        }
    )
    return response


def update_morbidity(morbidity_name, test_id, data: dict):
    print(PREFIX.MORBIDITY_PK_PREFIX+morbidity_name, PREFIX.MORBIDITY_SK_PREFIX+test_id, data['MorbidityMarkerRef'])
    response = DietTable.update_item(
        Key={
            'PK': PREFIX.MORBIDITY_PK_PREFIX+morbidity_name,
            'SK': PREFIX.MORBIDITY_SK_PREFIX+test_id
        },
        UpdateExpression='SET MorbidityMarkerRef = :MorbidityMarkerRef, MorbidityTestunit = :MorbidityTestunit',
        ExpressionAttributeValues={
            ':MorbidityMarkerRef': data['MorbidityMarkerRef'],
            ':MorbidityTestunit': data['MorbidityTestunit']
        },
        ReturnValues="UPDATED_NEW"  # returns the new updated values
    )
    return response


def delete_morbidity(morbidity_name, test_id):
    print(PREFIX.MORBIDITY_PK_PREFIX+morbidity_name, PREFIX.MORBIDITY_SK_PREFIX+test_id)
    response = DietTable.delete_item(
        Key={
            'PK': PREFIX.MORBIDITY_PK_PREFIX+morbidity_name,
            'SK': PREFIX.MORBIDITY_SK_PREFIX+test_id
          }
    )
    return response


"""
USER API - FUNCTIONS
"""


def read_all_users():
    print ('all user')
    response = DietTable.scan(
        FilterExpression='begins_with ( UserId , :uid_prefix1) OR begins_with ( UserId , :uid_prefix2)',
        ExpressionAttributeValues={
            ':uid_prefix1': 'PT',
            ':uid_prefix2': 'DT'
        }
    )
    return response


def read_by_usertype(user_type):
   pass

def read_by_firstname(firastname):
    pass


def read_by_contact(contact):
    pass


def read_by_email(mail_id):
    pass


def write_user(auto_user_id,data):
    pass


def update_user():
    pass


def delete_user():
    pass

def replace_decimals(obj):
    if isinstance(obj, list):
        for i in xrange(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj:
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj
