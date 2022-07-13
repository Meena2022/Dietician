import pytest
import requests
import csv
import json
import jsonpath


BASEURL = "http://127.0.0.1:5000/"
MORBIDITY_URL = "{}Morbidity".format(BASEURL)
MORBIDITYNAME_URL = "{}Morbidity/MorbidityName=Hypertension".format(BASEURL)
MORBIDITYTESTID_URL = "{}Morbidity/MorbidityTestId=RHEU_CCF".format(BASEURL)
MORBIDITYPUT_URL="{}Morbidity?MorbidityName={}&MorbidityTestId={}"



#getrequest for all morbidities
def test_1_get_allmorbidity():
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
    payload = {}
    headers = {}
    response = requests.request("GET", MORBIDITYNAME_URL, headers=headers, data=payload)
    responsebody = response.json()
    print("Get Request for MorbidityName Successfully Pass")
    print(response.url)
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
    payload = {}
    headers = {}
    response = requests.request("GET", MORBIDITYTESTID_URL, headers=headers, data=payload)
    responsebody = response.json()
    print("Get Request for MorbidityTestID Successfully Pass")
    print(response.url)
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

def test_4_post_morbidity():
    ##print("Read from csv file and  create as  list")
    csv_list = []
    key_list = ['MorbidityTestName', 'MorbidityTestUnit', 'MorbidityMarkerRef', 'MorbidityName']
    with open("D:/Numpy/Dietician Project/DieticianHackathon -3 phases/postmorbiditydetails.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter='=')
        for row in csvReader:
            csv_list.append(row)
    # print(csv_list)
    #print("Convert cvs list into list of dict")
    Morbidity_list = []
    for item in enumerate(csv_list):
        d = ({k: v for k, v in zip(key_list, item[1])})
        Morbidity_list.append(d)
    for item in enumerate(Morbidity_list):
        payload = json.dumps(item[1])
        headers = {
            'Content-Type': 'application/json'
        }
        #response=requests.post(,data=payload,headers=headers)
        response = requests.request("POST", MORBIDITY_URL, headers=headers, data=payload)
        print(response.content)
        print(response.status_code)
        print(response.text.__contains__("Morbidity successful created."))

def test_5_put_morbidity():
       csv_list = []
       key_list = ['MorbidityTestUnit', 'MorbidityMarkerRef']
       #print("Read from csv file and  create as  list")
       with open("D:/Numpy/Dietician Project/DieticianHackathon -3 phases/putmorbiditydetails.txt") as csvfile:
            csvReader = csv.reader(csvfile, delimiter='=')
            for row in csvReader:
                csv_list.append(row)
       print(csv_list)
       d = {}
       for item in enumerate(csv_list):
           print(item)
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
           #print(response.text.__contains__("Morbidity successful created."))

def test_5_delete_morbidity():
    csv_list = []
    with open("D:/Numpy/Dietician Project/DieticianHackathon -3 phases/deletemorbiditydetails.txt") as csvfile:
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