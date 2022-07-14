import pytest
import requests
import csv
import json
from base import Config_Base as config



def test_1_get_allUser():
    endpoint = config.USER_ENDPOINT
    response = requests.get(endpoint)
    print(response)
    print(endpoint)
    assert response.status_code == 200
    assert response.content, "application/json"
    assert isinstance(response.json, object)


@pytest.mark.parametrize("fname,result",[('Severse',200),('Gamora',200),('Pink',200)])
def test_2_get_userbyfirstname(fname,result):
    endpoint = config.USER_FNAME_ENDPOINT.format(fname)
    response = requests.get(endpoint)
    assert response.status_code == result
    assert response.content , "application/json"
    assert isinstance(response.json, object)

@pytest.mark.parametrize("email,result",[('joker@gamil.com',200),('micky@gmail.com',200),('Wonder@g.com',200)])
def test_3_userbyemailid(email,result):
    endpoint = config.USER_EMAIL_ENDPOINT.format(email)
    response = requests.get(endpoint)
    assert response.status_code == result
    assert response.content , "application/json"
    assert isinstance(response.json, object)


@pytest.mark.parametrize("contact,result",[('345678333',200),('345678122',200),('345678190',200)])
def test_4_userbyContactno(contact,result):
    endpoint = config.USER_CONTACT_ENDPOINT.format(contact)
    response = requests.get(endpoint)
    assert response.status_code == result
    assert response.content , "application/json"


@pytest.mark.parametrize("usertype,result",[('Patient',200),('Dietician',200)])
def test_5_userbyUserType(usertype,result):
    endpoint = config.USER_TYPE_ENDPOINT.format(usertype)
    response = requests.get(endpoint)
    assert response.status_code == result
    assert response.content , "application/json"


@pytest.mark.parametrize("dietician,result",[('DT001',200),('DT002',200)])
def test_6_userbyDieticianId(dietician,result):
    endpoint = config.USER_TYPE_ENDPOINT.format(dietician)
    response = requests.get(endpoint)
    assert response.status_code == result
    assert response.content , "application/json"


def test_7_post_user():

    endpoint = config.USER_ENDPOINT
    csv_list = config.read_cvs("testfiles/UserPost.txt")
    user_list = config.convert_csv_dict(config.USER__POST_KEYS, csv_list)
    user_detail = {}
    Address_map = {}
    print("create Address dict")
    for index, item in enumerate(user_list):
        temp_dict = item
        for key, value in temp_dict.items():
            if key in ('Address1', 'Address2', 'City', 'State', 'Country'):
                Address_map[key] = value
            else:
                user_detail[key] = value
        user_detail['Address'] = Address_map

        payload = json.dumps(user_detail)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", endpoint, headers=headers, data=payload)
        assert response.status_code == 200
        assert response.content , "application/json"


def test_8_put_morbidity():
    print("Read from csv file and  create as  list")
    csv_list = config.read_cvs("testfiles/UserPut.txt")
    user_list = []
    for item in enumerate(csv_list):
        DId = item[1][11]
        UId = item[1][12]
        d = ({k: v for k, v in zip(config.USER_PUT_KEYS, item[1])})
        user_list.append(d)

        user_detail = {}
        Address_map = {}
        for key, value in d.items():
            if key in ('Address1', 'Address2', 'City', 'State', 'Country'):
                Address_map[key] = value
            else:
                user_detail[key] = value
        user_detail['Address'] = Address_map
        payload = json.dumps(user_detail)
        headers = {
            'Content-Type': 'application/json'
        }
        endpoint = config.USER_PUT_ENDPOINT.format(DId,UId)
        response = requests.request("PUT", endpoint, headers=headers, data=payload)
        assert response.status_code == 200
        assert response.content , "application/json"


@pytest.mark.parametrize("dieticianid,userid,result",[('DT001','PT457',200),('DT001','PT823',200)])
def test_9_delete_user(dieticianid,userid,result):
    endpoint = config.USER_DEL_ENDPOINT.format(dieticianid,userid)
    response = requests.delete(endpoint)
    assert response.status_code == result
    assert response.content , "application/json"
