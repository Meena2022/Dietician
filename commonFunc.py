import copy
import random
import key_constants as PREFIX


def validate_request_body(data:dict, info_type):
    filled_attributes = []
    missed_attributes = []
    req_attribute = []
    extra_attributes = ['Extra attributes mentioned in request.']
    req_value = []

    if info_type.__eq__('user_post'): req_attribute=copy.deepcopy(PREFIX.REQUIRE_USER_DATA)
    if info_type.__eq__('user_put'): req_attribute=copy.deepcopy(PREFIX.UPDATABLE_USER_DATA)
    if info_type.__eq__('morbidity_post'): req_attribute = copy.deepcopy(PREFIX.REQUIRE_MORB_DATA)
    if info_type.__eq__('morbidity_put'): req_attribute = copy.deepcopy(PREFIX.UPDATABLE_MORB_DATA)

    # Collect Json body attributes
    for key in data.keys():
        filled_attributes.append(key)
    print(len(req_attribute),len(filled_attributes))
    # Validate Json body - Check only required attributes are passed.
    if len(filled_attributes) > len(req_attribute):
        return extra_attributes

    # Validate Json body - Find the missing attributes list.
    if len(filled_attributes) < len(req_attribute):
        print(info_type)
        #if info_type.__eq__('user_post') or info_type.__eq__('user_put'):
        for item in req_attribute:
            print(item)
            if item not in filled_attributes: missed_attributes.append(item)
        #elif info_type.__contains__('morbidity'):
            #for item in req_attribute:
               # print(item)
                #if item not in filled_attributes: missed_attributes.append(item)

    if len(missed_attributes) > 0: return missed_attributes

    # Validate Json body - attributes data type and attributes values
    for key, value in data.items():
        print(key, value, len(value))
        if 'Address'.__eq__(key) and not isinstance(value, dict):
            print(key, type(key), type(value), type(value) is dict, not isinstance(value, dict))
            req_value.append(key)
        elif 'Address'.__ne__(key) and not isinstance(value, str):
            print(key, type(value), isinstance(type(value), str), not isinstance(value, str))
            req_value.append(key)
        elif 'Address'.__ne__(key) and isinstance(value, str) and len(value) == 0:
            print(key, type(value), isinstance(type(value), str), not isinstance(value, str))
            req_value.append(key)
        elif key == 'UserType' and value not in PREFIX.USER_TYPE_PREFIX:
            print(key, value, req_attribute.keys())
            req_value.append(key)

    if len(req_value) > 0:
        return req_value
    else:
        return []


def generate_user_id(user_type):
    # Function to generate USER_ID based on {usertype}
    uid = ''
    for key in PREFIX.USER_TYPE_PREFIX.keys():
        print(key,PREFIX.USER_TYPE_PREFIX[key])
        if user_type.__eq__(key):
            uid=PREFIX.USER_TYPE_PREFIX[key] + str(random.randrange(100,1000,1))
    return uid


def generate_test_id(morbidity_name, test_name):
    test_id = morbidity_name[0:3] + '_' + test_name[0:3]
    return test_id.upper()