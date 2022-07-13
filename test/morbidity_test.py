import pytest
import requests
import csv
import json
BASEURL = "http://127.0.0.1:5000/"
MORBIDITY_URL = "{}Morbidity".format(BASEURL)
MORBIDITYNAME_URL = "{}Morbidity/MorbidityName=Hypertension".format(BASEURL)
MORBIDITYTESTID_URL = "{}Morbidity/MorbidityTestId=RHEU_CCF".format(BASEURL)
MORBIDITYPUT_URL="{}Morbidity/MorbidityName={}&MorbidityTestId={}"
#getrequest for all morbidities
def test_1_get_allmorbidity():
    print("Get All Morbidities")
    payload = {}
    headers = {}
    response = requests.request("GET", MORBIDITY_URL, headers=headers, data=payload)
    responsebody=response.json()
    print("Get Request for Morbidity Successfully Pass")
    assert response.url,"http://127.0.0.1:5000/Morbidity"
    assert response.content,"application/json"
    assert response.status_code, 200
    assert ("MorbidityName" in responsebody["Items"][0].keys()),True
    assert ("MorbidityTestName" in responsebody["Items"][0].keys()),True
    assert ("MorbidityMarkerRef" in responsebody["Items"][0].keys()),True
    assert ("MorbidityTestUnit" in responsebody["Items"][0].keys()),True
    assert ("MorbidityTestId" in responsebody["Items"][0].keys()),True
    print(response.status_code)
#getrequest for a morbidityname
def test_2_get_morbidityname():
    print("Get Morbidity by Morbidity Name")
    payload = {}
    headers = {}
    response = requests.request("GET", MORBIDITYNAME_URL, headers=headers, data=payload)
    responsebody = response.json()
    print("Get Request for MorbidityName Successfully Pass")
    #print(response.url)
    assert response.url == "http://127.0.0.1:5000/Morbidity/MorbidityName=Hypertension"
    assert response.content, "application/json"
    assert response.status_code, 200
    assert ("MorbidityName" in responsebody["Items"][0].keys()), True
    assert response.text.__contains__("Hypertension"),True
    print(responsebody["Items"][0].keys())
    print(response.status_code)
    print(response.text)
#getrequest for a morbiditytestid
def test_3_get_morbiditytestid():
    print("Get Morbidity by MorbidityTestId")
    payload = {}
    headers = {}
    response = requests.request("GET", MORBIDITYTESTID_URL, headers=headers, data=payload)
    responsebody = response.json()
    print("Get Request for MorbidityTestID Successfully Pass")
    #print(response.url)
    assert response.url=="http://127.0.0.1:5000/Morbidity/MorbidityTestId=RHEU_CCF"
    assert response.content, "application/json"
    assert response.status_code, 200
    assert ("MorbidityName" in responsebody["Items"][0].keys()), True
    assert ("MorbidityTestName" in responsebody["Items"][0].keys()), True
    assert ("MorbidityMarkerRef" in responsebody["Items"][0].keys()), True
    assert ("MorbidityTestId" in responsebody["Items"][0].keys()), True
    assert response.text.__contains__("RHEU_CCF"), True
    print(responsebody["Items"][0].keys())
    print(response.status_code)
    print(response.text)
# Add New Morbidity by Post Method
def test_4_post_morbidity():
    print("Post Method for Morbidity by MorbidityName")
    csv_list = []
    key_list = ['MorbidityTestName','MorbidityTestUnit','MorbidityMarkerRef','MorbidityName']
    with open("/test/testfiles/postmorbiditydetails.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter='=')
        for row in csvReader:
            csv_list.append(row)
    print(csv_list)
    #print("Convert cvs list into list of dict")
    Morbidity_list = []
    for item in enumerate(csv_list):
        d = ({k: v for k, v in zip(key_list, item[1])})
        Morbidity_list.append(d)
    for item in enumerate(Morbidity_list):
        print (item)
        payload = json.dumps(item[1])
        headers = {
            'Content-Type': 'application/json'
        }
        #response=requests.post(,data=payload,headers=headers)
        response = requests.request("POST", MORBIDITY_URL, headers=headers, data=payload)
        print(response.content)
        print(response.status_code)
        #print(respnse.text)
        print(response.text.__contains__("Morbidity successful created."))
#Update Morbidity by Put Method
def test_5_put_morbidity():
       print("Put Method for Morbidity")
       csv_list = []
       key_list = ['MorbidityTestUnit', 'MorbidityMarkerRef']
       #print("Read from csv file and  create as  list")
       with open("C:/Sunandha/GITdata/Dietician/test/testfiles/putmorbiditydetails.txt") as csvfile:
            csvReader = csv.reader(csvfile, delimiter='=')
            for row in csvReader:
                csv_list.append(row)
       #print(csv_list)
       d = {}
       for item in enumerate(csv_list):
           #print(item)
           temp_d = {}
           d = ({k: v for k, v in zip(key_list, item[1])})
           jsonbody= d
           morbidityname=item[1][2]
           morbiditytestid=item[1][3]
           #print(jsonbody, item[1][2], item[1][3])
           payload = json.dumps(jsonbody)
           headers = {
                'Content-Type': 'application/json'
           }
           MPUTURL = MORBIDITYPUT_URL.format(BASEURL,morbidityname,morbiditytestid)
           response = requests.request("PUT", MPUTURL, headers=headers, data=payload)
           print(response.content)
           print(response.status_code)
           assert(response.text.__contains__("Successfully Updated."))
# delete Morbidity
def test_5_delete_morbidity():
    print("Delete Method for Morbidity")
    csv_list = []
    with open("C:/Sunandha/GITdata/Dietician/test/testfiles/deletemorbiditydetails.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter='=')
        for row in csvReader:
            csv_list.append(row)
    print(csv_list)
    for item in enumerate(csv_list):
        print(item)
        morbidityname = item[1][0]
        morbiditytestid = item[1][1]
        # print(jsonbody, item[1][2], item[1][3])
        MDELURL = MORBIDITYPUT_URL.format(BASEURL, morbidityname, morbiditytestid)
        response = requests.request("DELETE",MDELURL)
        print(response.content)
        print(response.status_code)
        assert (response.text.__contains__("Successfully Deleted"))