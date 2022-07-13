import decimal
from datetime import datetime
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from urllib3.connectionpool import xrange

import config
import key_constants as PREFIX
import random


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
now = datetime.now().__str__()

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



"""
MORBIDITY API - FUNCTIONS
"""

def write_morbidity(auto_test_id, data: dict):
    response = DietTable.put_item(
        Item={
            'PK': PREFIX.MORBIDITY_PK_PREFIX + data['MorbidityName'],
            'SK': PREFIX.MORBIDITY_SK_PREFIX + auto_test_id,
            'InfoType': PREFIX.INFO_TYPE['MORBIDITY'],
            'MorbidityName': data['MorbidityName'],
            'MorbidityTestId': auto_test_id,
            'MorbidityTestName': data['MorbidityTestName'],
            'MorbidityMarkerRef': data['MorbidityMarkerRef'],
            'MorbidityTestUnit': data['MorbidityTestUnit'],
            'Createdon': now,
            'Modifiedon': now
        }
    )
    return response


def update_morbidity(morbidity_name, test_id, data: dict):
    pk_value = PREFIX.MORBIDITY_PK_PREFIX+morbidity_name
    sk_value = PREFIX.MORBIDITY_SK_PREFIX+test_id
    response = DietTable.update_item(
        Key={
            'PK': pk_value,
            'SK': sk_value
        },
        UpdateExpression='SET MorbidityMarkerRef = :markerRef, MorbidityTestUnit = :testUnit',
        ExpressionAttributeValues={
            ':markerRef': data['MorbidityMarkerRef'],
            ':testUnit': data['MorbidityTestUnit']
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

def write_user(auto_user_id,data):
    response = DietTable.put_item(
        Item={
            'PK': PREFIX.USER_PREFIX['PK'] + data['DieticianId'],
            'SK': PREFIX.USER_PREFIX['SK'] + auto_user_id,
            'InfoType': PREFIX.INFO_TYPE['USER'],
            'UserId': auto_user_id,
            'UserType': data['UserType'],
            'FirstName': data['FirstName'],
            'LastName': data['FirstName'],
            'Address': data['Address'],
            'Contact': data['Contact'],
            'Email': data['Email'],
            'Allergy': data['Allergy'],
            'FoodCategory': data['FoodCategory'],
            'DieticianId': data['DieticianId'],
            'LoginUsername': data['LoginUsername'],
            'Password': data['Password'],
            'Createdon': now,
            'Modifiedon': now
        }
    )
    return response


def update_user(dietician_id, user_id, data: dict):
    print(PREFIX.USER_PREFIX['PK']+ dietician_id, PREFIX.USER_PREFIX['SK'] + user_id)
    response = DietTable.update_item(
        Key={
            'PK': PREFIX.USER_PREFIX['PK'] + dietician_id,
            'SK': PREFIX.USER_PREFIX['SK'] + user_id
        },
        UpdateExpression='SET FirstName = :FirstName, LastName = :LastName,Address = :Address,Contact = :Contact,'
                         'Email = :Email,Allergy = :Allergy,FoodCategory= :FoodCategory,Modifiedon = :Modifiedon',
        ExpressionAttributeValues={
            ':FirstName': data['FirstName'],
            ':LastName': data['LastName'],
            ':Address': data['Address'],
            ':Contact': data['Contact'],
            ':Email': data['Email'],
            ':Allergy': data['Allergy'],
            ':FoodCategory': data['FoodCategory'],
            ':Modifiedon': now
        },
        ReturnValues="UPDATED_NEW"  # returns the new updated values
    )
    return response


def delete_user(dietician_id, user_id):
    print(PREFIX.USER_PREFIX['PK'] + dietician_id, PREFIX.USER_PREFIX['SK'] + user_id)
    response = DietTable.delete_item(
        Key={
            'PK': PREFIX.USER_PREFIX['PK'] + dietician_id,
            'SK': PREFIX.USER_PREFIX['SK'] + user_id
        }
    )
    return response

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
