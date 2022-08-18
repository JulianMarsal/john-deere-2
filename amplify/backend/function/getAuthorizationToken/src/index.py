import json
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def handler(event, context):
    callback = "http://localhost:3000"
    if(event['arguments'].get('callback') is not None):
        callback = event['arguments']['callback']
    try:
        #code = event["multiValueQueryStringParameters"]["code"][0]
        code = event['arguments']['code']
    except Exception as e:
        logger.debug("Error getting code in: " + str(e))
        logger.error(e)
        return {
            'statusCode': 400,
            'body': {"error": "The multiValueQueryStringParameter not have a code param in it"}
        }

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
    redirect_uri = callback
    scope = "ag1 ag2 ag3 eq1 eq2 org1 org2 files offline_access"
    client_id = "0oa61s8jfn4JhYGK85d7"
    client_secret = "4svYWYP5w7lqyuzj3O0ge1Zo9j9FWRPa3lfu9EsP"

    res = requests.post(
        "https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/token?grant_type="+grant_type+"&code="+code+"&redirect_uri="+redirect_uri+"&scope="+scope+"&client_id="+client_id+"&client_secret="+client_secret, data=payload, headers=headers).json()
    print("code :")
    print(code)
    print("response :")
    print(res)

    return {"statusCode": 200, "body": json.dumps(res)}

# Datos de fran
#     * Auth URL: https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/authorize
# * Access Token URL: https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/token
# * Client ID: 0oa61s8jfn4JhYGK85d7
# * Client Secret: 4svYWYP5w7lqyuzj3O0ge1Zo9j9FWRPa3lfu9EsP

# Request que hace la librería del botón :
# https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/authorize?client_id=0oa61s8jfn4JhYGK85d7&redirect_uri=http%3A%2F%2Flocalhost%3A3000&_reactName=onClick&_targetInst=null&type=click&nativeEvent=%5Bobject%20PointerEvent%5D&target=%5Bobject%20HTMLButtonElement%5D&currentTarget=%5Bobject%20HTMLButtonElement%5D&eventPhase=3&bubbles=true&cancelable=true&timeStamp=1554.5999999940395&defaultPrevented=false&isTrusted=true&view=%5Bobject%20Window%5D&detail=1&screenX=748&screenY=204&clientX=680&clientY=92&pageX=680&pageY=92&ctrlKey=false&shiftKey=false&altKey=false&metaKey=false&getModifierState=function%20modifierStateGetter(keyArg)%20%7B%0A%20%20%20%20%20%20var%20syntheticEvent%20%3D%20this%3B%0A%20%20%20%20%20%20var%20nativeEvent%20%3D%20syntheticEvent.nativeEvent%3B%0A%0A%20%20%20%20%20%20if%20(nativeEvent.getModifierState)%20%7B%0A%20%20%20%20%20%20%20%20return%20nativeEvent.getModifierState(keyArg)%3B%0A%20%20%20%20%20%20%7D%0A%0A%20%20%20%20%20%20var%20keyProp%20%3D%20modifierKeyToProp%5BkeyArg%5D%3B%0A%20%20%20%20%20%20return%20keyProp%20%3F%20!!nativeEvent%5BkeyProp%5D%20%3A%20false%3B%0A%20%20%20%20%7D&button=0&buttons=0&relatedTarget=null&movementX=0&movementY=0&isDefaultPrevented=function%20functionThatReturnsFalse()%20%7B%0A%20%20%20%20%20%20return%20false%3B%0A%20%20%20%20%7D&isPropagationStopped=function%20functionThatReturnsFalse()%20%7B%0A%20%20%20%20%20%20return%20false%3B%0A%20%20%20%20%7D&scope=openid%20profile%20email&response_type=code&response_mode=query&state=dEIyOUdJRmNlck5jazQ5Y2ltSGF%2BRU00cjJBRWh2Mkd6WWtyWExxUHEubQ%3D%3D&nonce=MEEuUHNzN1VKenZCa0JQZzB3U254Z29yZjA2MWJTRW5ST2IuelFCUEZhdA%3D%3D&code_challenge=gRjbKd_iIq5WXq_Mh96HdLaLkbnN0fVdgVqvPz12IbY&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtcmVhY3QiLCJ2ZXJzaW9uIjoiMS4xMC4yIn0%3D
