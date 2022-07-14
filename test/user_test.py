import pytest
import requests
import csv
import json

BASEURL = "http://127.0.0.1:5000/"
EMAIL = "joker@gamil.com"
FIRSTNAME = "Bat"
CONTACT = "234083664"
USERTYPE = "Patient"
DIETICIANID = "DT003"
USERID = "PT0014"

def test_1_get_userbyfirstname():
    users_url = "{}Users/FirstName={}".format(BASEURL, FIRSTNAME)
    r = requests.get(users_url)
    assert r.status_code, 200
    assert r.content, "application/json"
    assert isinstance(r.json, object)
    # assert set(r.json.keys()) >= {'Email', 'UserId'}
    # assert r.json['UserId'] == "PT0005"


def test_2_userbyemailid():
    users_url = "{}Users/Email={}".format(BASEURL, EMAIL)
    r = requests.get(users_url)
    assert r.status_code, 200
    assert r.content, "application/json"


def test_3_userbyContactno():
    users_url = "{}Users/Contact={}".format(BASEURL, CONTACT)
    r = requests.get(users_url)
    assert r.status_code, 200
    assert r.content, "application/json"


def test_4_userbyUserType():
    users_url = "{}Users/UserType={}".format(BASEURL, USERTYPE)
    r = requests.get(users_url)
    assert r.status_code, 200
    assert r.content, "application/json"

def test_5_userbyDieticianId():
    users_url = "{}Users/DieticianId={}".format(BASEURL, DIETICIANID)
    r = requests.get(users_url)
    assert r.status_code, 200
    assert r.content, "application/json"

def test_6_post_user():
    user_key_list = ['UserType', 'FirstName', 'LastName', 'Contact', 'Email', 'Allergy', 'FoodCategory',
                     'DieticianId', 'Address1', 'Address2', 'City', 'State', 'Country', 'LoginUsername', 'Password']

    print("Read from csv file and  create as  list")
    csv_list = []
    with open("C:/Users/abhij/PycharmProjects/Dietician/test/testfiles/UserPost.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter='=')
        for row in csvReader:
            csv_list.append(row)
    print(csv_list)

    print("Convert cvs list into list of dict")
    user_list = []
    for item in enumerate(csv_list):
        d = ({k: v for k, v in zip(user_key_list, item[1])})
        user_list.append(d)
    print(user_list)

    user_detail = {}
    Address_map = {}
    temp_dict = {}
    print("create Address dict")
    users_url = "{}users".format(BASEURL)
    for index, item in enumerate(user_list):
        temp_dict = item
        for key, value in temp_dict.items():
            if key in ('Address1', 'Address2', 'City', 'State', 'Country'):
                Address_map[key] = value
            else:
                user_detail[key] = value
        user_detail['Address'] = Address_map
        print(user_detail)


    # for item in enumerate(user_detail):
    #     print(user_detail)
        print(users_url)
        payload = json.dumps(user_detail)
        headers = {
            'Content-Type': 'application/json'
        }

        print(payload)
        # response=requests.post(,data=payload,headers=headers)
        response = requests.request("POST", users_url, headers=headers, data=payload)
        assert response.status_code, 200
        assert response.content, "application/json"

        # print(response.status_code)
        print(response.text.__contains__("Successfully Created."))


def test_7_put_morbidity():
    user_key_list = ['FirstName', 'LastName', 'Contact', 'Email', 'Allergy', 'FoodCategory',
                      'Address1', 'Address2', 'City', 'State', 'Country']

    print("Read from csv file and  create as  list")
    csv_list = []
    with open("C:/Users/abhij/PycharmProjects/Dietician/test/testfile/UserPut.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter='=')
        for row in csvReader:
            csv_list.append(row)
    print(csv_list)

    print("Convert cvs list into list of dict")
    user_list = []
    users_url = "{}users?DieticianId={}&UserId={}"
    for item in enumerate(csv_list):

        DId = item[1][11]
        UId = item[1][12]
        d = ({k: v for k, v in zip(user_key_list, item[1])})
        user_list.append(d)

        user_detail = {}
        Address_map = {}

        print("create Address dict")

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

        users_url = users_url.format(BASEURL, DId, UId)

        response = requests.request("PUT", users_url, headers=headers, data=payload)
        assert response.status_code, 200
        assert response.content, "application/json"

        print(response.text.__contains__("Successfully Updated."))

        assert response.url == "http://127.0.0.1:5000/users?DieticianId=DT001&UserId=PT889"


def test_8_delete_user():
    users_url = "{}Users/DieticianId={}/UserId={}".format(BASEURL, DIETICIANID, USERID)
    r = requests.delete(users_url)
    print(users_url)
    assert r.status_code, 200
