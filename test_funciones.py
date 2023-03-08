import json
import boto3
import requests
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from funciones import mi_funcion

def test_mi_funcion():

    mi_funcion()
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('landing-casas-021')
    objs = list(bucket.objects.filter(Prefix=datetime.datetime.now().strftime('%Y-%m-%d')))
    assert len(objs) == 1
    
    
