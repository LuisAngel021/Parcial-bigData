import json
from urllib.request import urlopen
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    with urlopen("https://casas.mitula.com.co/searchRE/nivel2-Bogot%C3%A1/nivel1-Cundinamarca/tipo-Casa/q-Bogot%C3%A1") as response:
        body = response.read()
        
    
    client = boto3.client('s3')
    client.put_object(Body=body,Bucket='arn:aws:s3:::bigdata-parcial',Key='mitula.txt')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
