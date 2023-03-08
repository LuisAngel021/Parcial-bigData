from funciones import mi_funcion
import json
import boto3
import requests
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pytest_mock import mocker

def test_mi_funcion(mocker):
    # Setup
    client_mock = mocker.patch("boto3.client")
    mock_put_object = client_mock.return_value.put_object
    mock_soup = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.text = '<html></html>'
    mock_response.content = b'<html></html>'
    mock_response.status_code = 200
    mocker.patch("requests.get", return_value=mock_response)
    mocker.patch("bs4.BeautifulSoup", return_value=mock_soup)
    expected_bucket_name = "bigdata-parcial"
    expected_key = "MiTula.txt"

    # Exercise
    mi_funcion()

    # Assert
    requests.get.assert_called_once_with(
        'https://casas.mitula.com.co/searchRE/nivel2-Bogot%C3%A1/nivel1-Cundinamarca/op-1/tipo-Casa/q-Bogot%C3%A1')
    client_mock.assert_called_once_with('s3')
    mock_put_object.assert_called_once_with(Bucket=expected_bucket_name, Key=expected_key, Body=mock_response.content)
    mock_soup.prettify.assert_called_once()
