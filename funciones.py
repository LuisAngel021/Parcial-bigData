import json
import boto3
import requests
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

client = boto3.client('s3')
BUCKET_NAME = 'landing-casas-021'

def capturar_html(url, x):
    url = 'https://casas.mitula.com.co/searchRE/nivel2-Bogot%C3%A1/nivel1-Cundinamarca/op-1/tipo-Casa/q-Bogot%C3%A1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    html_file = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.html"
    client.put_object(Bucket=BUCKET_NAME, Key=html_file, Body=response.content)


def lambda2():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    obj = bucket.Object(f"{datetime.datetime.now().strftime('%Y-%m-%d')}.html")
    body = obj.get()['Body'].read()
    soup = BeautifulSoup(body, 'html.parser')

    properties = soup.find_all('div', {'class': 'listing-card__information-main'})

    data = []

    for property in properties:
        price = property.find('div', {'class': 'listing-card__price-wrapper'}).text.strip()
        sqft = property.find_all('div', {'class': 'listing-card__property'})
        sqft2 = sqft    
        casa = [price]
        for property2 in sqft2:
            casa.append(property2.text.strip())
          
        data.append(casa)    
    
    print(data)
    s = ""
    s = s + " Precio, num_habitaciones, num_banos, metros_cuadrados\n"
    for fila in data:
        if len(fila) >= 4:
            s = s + fila[0] + "," + fila[1].replace(".", " ") + "," + fila[2].replace(".", " ") + "," + fila[3] +"\n"
        
    client = boto3.client('s3')
    client.put_object(Body=s, Bucket='casas-final-021', Key=f"{datetime.datetime.now().strftime('%Y-%m-%d')}.csv")
