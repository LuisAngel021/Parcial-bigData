import requests
from bs4 import BeautifulSoup
import datetime
import boto3
import csv

BUCKET_NAME = 'casas-final-021'

def lambda_handler():

# URL de la página a analizar
    url = "https://casas.mitula.com.co/searchRE/nivel3-Chapinero/nivel2-Bogot%C3%A1/nivel1-Cundinamarca/op-1/tipo-Casa/q-Bogot%C3%A1-Chapinero"

# Realizamos la petición GET a la página y obtenemos su contenido
    response = requests.get(url)    
    content = response.content

    # Parseamos el contenido HTML utilizando BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Encontramos todos los elementos HTML que contienen información de las casas
    casas = soup.find_all('div', {'class': 'listing-item'})
    
    # Creamos una lista para almacenar los datos de cada casa
    data = []
    
    # Recorremos todos los elementos HTML de las casas y extraemos su información
    for casa in casas:
        # Extraemos la información de dirección, precio, área, número de habitaciones y número de baños
        direccion = casa.find('div', {'class': 'listing-item__title'}).text.strip()
        precio = casa.find('div', {'class': 'listing-item__price'}).text.strip()
        area = casa.find('div', {'class': 'listing-item__attrs'}).find_all('div')[0].text.strip()
        habitaciones = casa.find('div', {'class': 'listing-item__attrs'}).find_all('div')[1].text.strip()
        banos = casa.find('div', {'class': 'listing-item__attrs'}).find_all('div')[2].text.strip()
    
        # Almacenamos la información de la casa en la lista de datos
        data.append([direccion, precio, area, habitaciones, banos])
    
    # Abrimos un archivo CSV y escribimos la información de las casas
    with open('casas.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['direccion', 'precio', 'area', 'habitaciones', 'banos'])
        writer.writerows(data)
    
    # Imprimimos la lista de datos para comprobar que se ha extraído correctamente
    print(data)


lambda_handler()