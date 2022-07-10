import random
import key_constants as PREFIX


def validate_request_body(data:dict,infotype):
    filled_attributes = []
    missed_attributes = []
    req_value = []
    user_type = False

    # Collect Json body attributes
    for key in data.keys():
        filled_attributes.append(key)

    # Validate Json body - for missing values
    for key, value in data.items():
        if len(value) == 0:
            req_value.append(key)


    if infotype.__eq__('user'):
    #Check the value of User-type
        for key in PREFIX.USER_TYPE_PREFIX.keys():
            if data['UserType'] == key: user_type=True

        # Find the missing attribute and values
        for item in PREFIX.REQUIRE_USER_DATA:
            print(item)
            if item not in filled_attributes:
                missed_attributes.append(item)
    elif infotype.__eq__('morbidity'):
        # Find the missing attribute and values
        for item in PREFIX.REQUIRE_MORB_DATA:
            print(item)
            if item not in filled_attributes:
                missed_attributes.append(item)

    print('Missed :',missed_attributes)
    print('Req :', req_value)

    if len(req_value) > 0:
        return req_value
    elif len(missed_attributes) > 0:
        return missed_attributes
    elif user_type == False and infotype.__eq__('user'):
        return [ 'User Type Should be Dietician / Patient' ]
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