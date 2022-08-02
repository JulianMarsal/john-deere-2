import requests
import os


def handler(event, context):

    # For the test environment
    # if(os.environ.get('Authorization') is not None):
    #     authorization = os.environ.get('Authorization')
    # else:
    #     Here we use a harcoding of the authorization token or we can use the function one passed as parameter in the headers like this
    # headers["Authorization"] = "Bearer {token}" así se podría hacer para no pasar el "bearer" también
    organizationID = event['arguments']['organizationId']
    fieldId = event['arguments']['fieldId']
    header = {
        'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
        'Accept': 'application/vnd.deere.axiom.v3+json',
        'Content-Type': 'application/json',
        # In the near future, we will be in the environment variable
        "Authorization": "Bearer eyJraWQiOiJFRm5BQWw5SE5xQm02LXQ1ZHJWWFB3dzg3ZWEzSndhRkUyQTVaM2xpNjIwIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmZhMkxieXJGU282X3YwWkxPdkNPZmRpYXhleDViVWpzNnFSdC1EMFNUb0kub2Fya3pxZTc0NUY0TmFYQzE1ZDYiLCJpc3MiOiJodHRwczovL3NpZ25pbi5qb2huZGVlcmUuY29tL29hdXRoMi9hdXM3OHRubGF5c01yYUZoQzF0NyIsImF1ZCI6ImNvbS5kZWVyZS5pc2cuYXhpb20iLCJpYXQiOjE2NTkwMjcyODUsImV4cCI6MTY1OTA3MDQ4NSwiY2lkIjoiMG9hNWF4MjMwd29aM0MydU41ZDciLCJ1aWQiOiIwMHU1YXJmcDl2OFNPV3FSMTVkNyIsInNjcCI6WyJhZzIiLCJhZzEiLCJvZmZsaW5lX2FjY2VzcyIsImZpbGVzIiwiYWczIiwib3JnMSIsIm9yZzIiLCJlcTIiLCJlcTEiXSwiYXV0aF90aW1lIjoxNjU4ODYzNDY4LCJzdWIiOiJqdWxpYW5tYXJzYWwiLCJ1c2VyVHlwZSI6IkN1c3RvbWVyIn0.Y6LJjJgobZgbpWD1Hk79tviJ-2-wcWop8hfdIE7fEYiYVRWnjU4AOjmuMsG8FbKYxvBuGbPDlKMAHgoffGTvBb40r8_-krnyO5v3vZmXPW0gRNoWEHB4DkfnxOpxRD8EfAiOkI0NIxEMLOLGaj6URCZGogWkgK3Pj3FrJVATAsrQgGf8fP4zBwjbnx7W3S83TzP-wRUA_ofVsQYMhwV6HahvwPjHrRd0cE_DJwgqvNj5ouPp_pBaok-8gQeOVru4HJkujrXzkftIF_jh2FgKpIMpa5stzOvpXcA4fioRfI03SPb9DbR_lGgjt05bepsxYWT3PuG9DhZSy_xPQfraPg"
    }
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields/"+fieldId+"/boundaries", headers=header, auth={}).json()

    name = response["values"][0]["name"]
    Type = response["values"][0]["@type"]
    area = response["values"][0]["area"]
    workeableArea = response["values"][0]["workableArea"]
    sourceType = response["values"][0]["sourceType"]
    multipolygons = response["values"][0]["multipolygons"]
    extent = response["values"][0]["extent"]
    active = response["values"][0]["active"]
    archived = response["values"][0]["archived"]
    Id = response["values"][0]["id"]
    modifiedTime = response["values"][0]["modifiedTime"]
    createdTime = response["values"][0]["createdTime"]
    irrigated = response["values"][0]["irrigated"]

    # boundaryDict = {
    #     "id": "",
    #     "name": "",
    #     "area": "",
    #     "workableArea": "",
    #     "sourceType": "",
    #     "multipolygons": [],
    #     "type": "",
    #     "extent": "",
    #     "active": None,
    #     "archived": None,
    #     "modifiedTime": "",
    #     "createdTime": "",
    #     "irrigated": None
    # }

    if (response["total"] == 0):
        # "No boundaries found"
        print("No boundaries found")
        return None

    boundaryDict = {
        "type": Type,
        "id": Id,
        "name": name,
        "area": area,
        "workableArea": workeableArea,
        "sourceType": sourceType,
        "multipolygons": multipolygons,
        "extent": extent,
        "active": active,
        "archived": archived,
        "modifiedTime": modifiedTime,
        "createdTime": createdTime,
        "irrigated": irrigated
    }

    return boundaryDict
