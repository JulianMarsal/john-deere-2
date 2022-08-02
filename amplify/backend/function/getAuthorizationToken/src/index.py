import json
import requests


def handler(event, context):
    #code = event['arguments']['code']
    code = event["multiValueQueryStringParameters"]["code"][0]
    print("codigo :")
    print(code)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'grant_type': 'authorization_code',
        # 'redirect_uri': "https://kc1jfn1yj9.execute-api.us-east-1.amazonaws.com/Test",
        # 'code': code,
        # 'scope': "ag1 ag2 ag3 eq1 eq2 org1 org2 files offline_access",
    }

    grant_type = 'authorization_code'
    redirect_uri = "https://kc1jfn1yj9.execute-api.us-east-1.amazonaws.com/Test"
    scope = "ag1 ag2 ag3 eq1 eq2 org1 org2 files offline_access"
    client_id = "0oa5ax230woZ3C2uN5d7"
    client_secret = "c88ea1ff782f4206aaf1eb39e7b4a755"

    res = requests.post(
        "https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/token?grant_type="+grant_type+"&code="+code+"&redirect_uri="+redirect_uri+"&scope="+scope+"&client_id="+client_id+"&client_secret="+client_secret, data=payload, headers=headers).json()
    print("code :")
    print(code)
    print("res normal :")
    print(res)

    return {"statusCode": 200, "body": json.dumps(res)}
