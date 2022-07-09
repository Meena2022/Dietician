"""
import pytest
import requests

BASEURL = "http://127.0.0.1:5000/"
MORBIDITY_URL = "{}morbidity".format(BASEURL)


def test_1_get_allmorbidity():
    equests.get(MORBIDITY_URL)
    assert r.status_code, 200

"""
def test_2_morbidity():
    pass


def test_3_post_morbidity():
    pass


def test_4_put_morbidity():
    pass