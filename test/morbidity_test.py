import pytest
import requests
import csv
import json
from base import ConfigBase as config


#getrequest for all morbidities
def test_1_get_allmorbidity():
    #print("Get All Morbidities")
    response = requests.request("GET", config.MORBIDITY_ENDPOINT)
    responsebody = response.json()
    assert response.url == "http://127.0.0.1:5000/Morbidity/"
    assert response.status_code == 200
    assert response.content , "application/json"
    assert ("MorbidityName" in responsebody["Items"][0].keys()),True
    assert ("MorbidityTestName" in responsebody["Items"][0].keys()),True
    assert ("MorbidityMarkerRef" in responsebody["Items"][0].keys()),True
    assert ("MorbidityTestUnit" in responsebody["Items"][0].keys()),True
    assert ("MorbidityTestId" in responsebody["Items"][0].keys()),True


#getrequest for a morbidityname
@pytest.mark.parametrize("morbidityname,result",[('Hypothyroidism',200),('Pre Diabetes',200)])
def test_2_get_morbidityname(morbidityname,result):
    endpoint = config.MORBIDITY_NAME_ENDPOINT.format(morbidityname)
    response = requests.request("GET", endpoint)
    responsebody = response.json()
    assert response.url.__contains__("http://127.0.0.1:5000/Morbidity/MorbidityName="),True
    assert response.content , "application/json"
    assert response.status_code == result
    assert ("MorbidityName" in responsebody["Items"][0].keys()), True
    assert response.text.__contains__(morbidityname),True


#getrequest for a morbiditytestid
@pytest.mark.parametrize("testid,result",[('DIA1_BG',200),('RHEU_CCF',200)])
def test_3_get_morbiditytestid(testid,result):
    endpoint = config.MORBIDITY_TESTID_ENDPOINT.format(testid)
    response = requests.request("GET", endpoint)
    responsebody = response.json()
    assert response.url.__contains__("http://127.0.0.1:5000/Morbidity/MorbidityTestId="), True
    assert response.content, "application/json"
    assert response.status_code, result
    assert ("MorbidityName" in responsebody["Items"][0].keys()), True
    assert ("MorbidityTestName" in responsebody["Items"][0].keys()), True
    assert ("MorbidityMarkerRef" in responsebody["Items"][0].keys()), True
    assert ("MorbidityTestId" in responsebody["Items"][0].keys()), True
    assert response.text.__contains__(testid), True


# Add New Morbidity by Post Method
def test_4_post_morbidity():
    csv_list = config.read_cvs("testfiles/postmorbiditydetails.txt")
    Morbidity_list = config.convert_csv_dict(config.MORBIDITY_POST_KEYS,csv_list)
    for item in enumerate(Morbidity_list):
        morbidity_data = item[1]
        payload = json.dumps(morbidity_data)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", config.MORBIDITY_ENDPOINT, headers=headers, data=payload)
        assert response.content, "application/json"
        assert response.status_code == 200
        assert response.text.__contains__("Morbidity successful created.")

#Update Morbidity by Put Method
def test_5_put_morbidity():
    #Put Method for Morbidity
    csv_list = config.read_cvs("testfiles/putmorbiditydetails.txt")
    for item in enumerate(csv_list):
        morbidity_data = ({k: v for k, v in zip(config.MORBIDITY_PUT_KEYS, item[1])})
        morbidityname=item[1][2]
        morbiditytestid=item[1][3]
        payload = json.dumps(morbidity_data)
        headers = {
            'Content-Type': 'application/json'
        }
        endpoint = config.MORBIDITY_PUT_ENDPOINT.format(morbidityname,morbiditytestid)
        response = requests.request("PUT", endpoint , headers=headers, data=payload)
        assert response.content, "application/json"
        assert response.status_code == 200
        assert response.text.__contains__("Successfully Updated.")

# delete Morbidity
@pytest.mark.parametrize("morbidityname,testid,result",[('dabcHypothyroidism','DAB_1AT',200),('dabcHypothyroidism','DAB_10A',200)])
def test_5_delete_morbidity(morbidityname,testid,result):
    #Delete Method for Morbidity
    endpoint = config.MORBIDITY_DEL_ENDPOINT.format(morbidityname, testid)
    response = requests.request("DELETE",endpoint)
    assert response.content, "application/json"
    assert response.status_code, result
    assert (response.text.__contains__("Successfully Deleted"))


