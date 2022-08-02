import json
import requests
from authlib.integrations.requests_client import OAuth2Session
import os


def handler(event, context):
    if(os.environ.get('client_secret') is not None):
        client_secret_for_enviroment = os.environ.get('client_secret')

    client_id = "0oa5ax230woZ3C2uN5d7"
    client_secret = client_secret_for_enviroment
    scope = 'ag1 ag2 ag3 eq1 eq2 org1 org2 files offline_access'
    client = OAuth2Session(client_id, client_secret, scope=scope,
                           redirect_uri="http://localhost:9090/callback")
    token_endpoint = "https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/token"
    token = "G1AWrayoyCFB4F11xDpuwQXAzmFFEfXfLkh3lIo3U-U"
    new_token = client.refresh_token(token_endpoint, refresh_token=token)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': {"access_token": 'Bearer '+new_token["access_token"]}
    }
