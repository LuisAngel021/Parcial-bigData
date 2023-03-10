import boto3
import requests
import datetime
from unittest import mock
from funciones import capturar_html, lambda2
from unittest.mock import MagicMock, patch

client = boto3.client('s3')


def test_capturar_html():
    url = 'https://casas.mitula.com.co/searchRE/nivel2-Bogot%C3%A1/nivel1-Cundinamarca/op-1/tipo-Casa/q-Bogot%C3%A1'
    response = requests.get(url)
    html_file = "{}.html".format(datetime.datetime.now().strftime('%Y-%m-%d'))
    client.put_object(Bucket='landing-casas-021', Key=html_file, Body=response.content)
    assert client.list_objects(Bucket='landing-casas-021')['Contents'][0]['Key'] == html_file


@patch('boto3.resource')
@patch('boto3.client')
def test_lambda2(mock_s3_client, mock_s3_resource):
    # Simula el objeto S3 y los métodos get() y put_object()
    mock_bucket = MagicMock()
    mock_object = MagicMock()
    mock_object.get.return_value = {'Body': MagicMock(read=MagicMock(return_value=b'<html><body><div class="listing-card__information-main"><div class="listing-card__price-wrapper">Price</div><div class="listing-card__property">1</div><div class="listing-card__property">2</div><div class="listing-card__property">3</div></div></body></html>'))}
    mock_bucket.Object.return_value = mock_object
    mock_s3_resource.return_value.Bucket.return_value = mock_bucket
    mock_s3_client.return_value.put_object.return_value = {}

    # Ejecuta la función lambda2()
    lambda2()

    # Comprueba que el método put_object() fue llamado con los parámetros correctos
    mock_s3_client.return_value.put_object.assert_called_with(
        Body=' Precio, num_habitaciones, num_banos, metros_cuadrados\nPrice,1,2,3\n',
        Bucket='casas-final-021',
        Key=f"{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"
    )


def test_capturar_html_con_mock():

    mock_requests = MagicMock()
    mock_response = MagicMock()
    mock_response.content = b'contenido.html'
    mock_requests.get.return_value = mock_response
    mock_boto3 = MagicMock()
    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client
    with patch.dict('sys.modules', {'boto3': mock_boto3, 'requests': mock_requests}):
        capturar_html()
    mock_client.put_object(Bucket='landing-casas-021', Key=mock.ANY, Body=mock_response.content)
