import copy
import random
import key_constants as PREFIX


def validate_request_body(data:dict, info_type):
    #Validae Json body for PUT , POSt
    filled_attributes = []
    missed_attributes = []
    req_attribute = []
    extra_attributes = ['Extra attributes mentioned.']
    notreq_attributes = []
    req_value = []

    if info_type.__eq__('user_post'): req_attribute=copy.deepcopy(PREFIX.REQUIRE_USER_DATA)
    if info_type.__eq__('user_put'): req_attribute=copy.deepcopy(PREFIX.UPDATABLE_USER_DATA)
    if info_type.__eq__('morbidity_post'): req_attribute = copy.deepcopy(PREFIX.REQUIRE_MORB_DATA)
    if info_type.__eq__('morbidity_put'): req_attribute = copy.deepcopy(PREFIX.UPDATABLE_MORB_DATA)

    # Collect Json body attributes
    for key in data.keys():
        filled_attributes.append(key)

    # Validate Json body - Check any extra attributes are passed.
    if len(filled_attributes) > len(req_attribute):
        return extra_attributes


    # Validate Json body - Check all required attributes are passed.
    if len(filled_attributes) == len(req_attribute):
        for attributes in filled_attributes:
            if attributes not in req_attribute:
                notreq_attributes.append(key)

    if len(notreq_attributes)>0: return notreq_attributes

    # Validate Json body - Find the missing attributes list.
    if len(filled_attributes) < len(req_attribute):
        for item in req_attribute:
            if item not in filled_attributes: missed_attributes.append(item)

    if len(missed_attributes) > 0: return missed_attributes


    # Validate Json body - attributes data type and attributes values
    for key, value in data.items():
        if key.__eq__('Address') and not isinstance(value, dict):
            req_value.append(key)
        elif key.__ne__('Address') and not isinstance(value, str):
            req_value.append(key)
        elif key.__ne__('Address') and isinstance(value, str):
            if len(value) == 0: req_value.append(key)
        elif key == 'UserType' and value not in PREFIX.USER_TYPE_PREFIX:
             req_value.append(key)

    if len(req_value) > 0:
        return req_value
    else:
        return []


def generate_user_id(user_type):
    # Function to generate USER_ID based on {usertype}
    uid = ''
    for key in PREFIX.USER_TYPE_PREFIX.keys():
        if user_type.__eq__(key):
            uid = PREFIX.USER_TYPE_PREFIX[key] + str(random.randrange(100, 10000, 1))
    return uid


def generate_test_id(morbidity_name, test_name):
    # Function to generate TEST_ID based on {MorbidityName, TestName}
    test_id = morbidity_name[0:3] + '_' + test_name[0:3]
    return test_id.upper()