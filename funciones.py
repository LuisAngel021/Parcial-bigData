import json
import boto3
import requests
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

client = boto3.client('s3')
BUCKET_NAME = 'landing-casas-021'

def mi_funcion():
    
    url = 'https://casas.mitula.com.co/searchRE/nivel2-Bogot%C3%A1/nivel1-Cundinamarca/op-1/tipo-Casa/q-Bogot%C3%A1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    html_file = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.html"
    client.put_object(Bucket=BUCKET_NAME,Key='yyyy-mm-dd.html',Body=response.content)

mi_funcion()