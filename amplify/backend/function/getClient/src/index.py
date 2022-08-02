import requests


def handler(event, context):
    organizationID = event['arguments']['organizationId']
    clientID = event['arguments']['clientId']
    header = {
        'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
        'Accept': 'application/vnd.deere.axiom.v3+json',
        'Content-Type': 'application/json',
        "Authorization": "Bearer eyJraWQiOiJFRm5BQWw5SE5xQm02LXQ1ZHJWWFB3dzg3ZWEzSndhRkUyQTVaM2xpNjIwIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmZhMkxieXJGU282X3YwWkxPdkNPZmRpYXhleDViVWpzNnFSdC1EMFNUb0kub2Fya3pxZTc0NUY0TmFYQzE1ZDYiLCJpc3MiOiJodHRwczovL3NpZ25pbi5qb2huZGVlcmUuY29tL29hdXRoMi9hdXM3OHRubGF5c01yYUZoQzF0NyIsImF1ZCI6ImNvbS5kZWVyZS5pc2cuYXhpb20iLCJpYXQiOjE2NTkwMjcyODUsImV4cCI6MTY1OTA3MDQ4NSwiY2lkIjoiMG9hNWF4MjMwd29aM0MydU41ZDciLCJ1aWQiOiIwMHU1YXJmcDl2OFNPV3FSMTVkNyIsInNjcCI6WyJhZzIiLCJhZzEiLCJvZmZsaW5lX2FjY2VzcyIsImZpbGVzIiwiYWczIiwib3JnMSIsIm9yZzIiLCJlcTIiLCJlcTEiXSwiYXV0aF90aW1lIjoxNjU4ODYzNDY4LCJzdWIiOiJqdWxpYW5tYXJzYWwiLCJ1c2VyVHlwZSI6IkN1c3RvbWVyIn0.Y6LJjJgobZgbpWD1Hk79tviJ-2-wcWop8hfdIE7fEYiYVRWnjU4AOjmuMsG8FbKYxvBuGbPDlKMAHgoffGTvBb40r8_-krnyO5v3vZmXPW0gRNoWEHB4DkfnxOpxRD8EfAiOkI0NIxEMLOLGaj6URCZGogWkgK3Pj3FrJVATAsrQgGf8fP4zBwjbnx7W3S83TzP-wRUA_ofVsQYMhwV6HahvwPjHrRd0cE_DJwgqvNj5ouPp_pBaok-8gQeOVru4HJkujrXzkftIF_jh2FgKpIMpa5stzOvpXcA4fioRfI03SPb9DbR_lGgjt05bepsxYWT3PuG9DhZSy_xPQfraPg"
    }
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/clients/"+clientID, headers=header).json()

    clientDict = {}
    clientDict.update({"name": response["name"]})
    clientDict.update({"archived": response["archived"]})
    clientDict.update({"id": response["id"]})
    clientLinks = []
    for link in response["links"]:
        clientLinks.append(link)
    clientDict.update({"links": clientLinks})
    return clientDict
