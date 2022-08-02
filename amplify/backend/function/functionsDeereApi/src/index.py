import json
import requests
import os


def listClients(organizationID, header):

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/clients", headers=header).json()

    clientList = []
    for cliente in response["values"]:
        clientDict = {}
        clientDict.update({"name": cliente["name"]})
        clientDict.update({"archived": cliente["archived"]})
        clientDict.update({"id": cliente["id"]})
        clientLinks = []
        for link in cliente["links"]:
            clientLinks.append(link)
        clientDict.update({"links": clientLinks})
        clientList.append(clientDict)
    return clientList


def getClient(organizationID, clientID, header):
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


def listFields(organizationID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields", headers=header).json()

    fieldList = []
    for field in response["values"]:
        fieldDict = {}
        fieldDict["type"] = field["@type"]  # ver que onda esta nomenglatura
        fieldDict["name"] = field["name"]
        fieldDict["archived"] = field["archived"]
        fieldDict["id"] = field["id"]
        fieldLinks = []
        for link in field["links"]:
            fieldLinks.append(link)
        fieldDict["links"] = fieldLinks
        fieldList.append(fieldDict)
    return fieldList


def getField(organizationID, fieldID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields/"+fieldID, headers=header).json()
    fieldDict = {}
    fieldDict["type"] = response["@type"]
    fieldDict["name"] = response["name"]
    fieldDict["archived"] = response["archived"]
    fieldDict["id"] = response["id"]
    fieldLinks = []
    for link in response["links"]:
        fieldLinks.append(link)
    fieldDict["links"] = fieldLinks
    return fieldDict


def getBoundary(organizationID, fieldID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields/"+fieldID+"/boundaries", headers=header, auth={}).json()
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


def listOrganizations(header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/", headers=header).json()

    organizationList = []
    for organization in response["values"]:
        organizationDict = {}
        organizationDict.update({"type": organization["type"]})
        organizationDict.update({"name": organization["name"]})
        organizationDict.update({"member": organization["member"]})
        organizationDict.update({"internal": organization["internal"]})
        organizationDict.update({"id": organization["id"]})
        organizationLinks = []
        for link in organization["links"]:
            organizationLinks.append(link)
        organizationDict.update({"links": organizationLinks})
        organizationList.append(organizationDict)
    return organizationList


def listFarms(organizationID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/farms", headers=header).json()

    farmList = []
    for farm in response["values"]:
        farmType = farm["@type"]
        name = farm["name"]
        archived = farm["archived"]
        farmId = farm["id"]
        farmLinks = []
        for link in farm["links"]:
            farmLinks.append(link)

        farmDict = {
            "type": farmType,
            "name": name,
            "archived": archived,
            "id": farmId,
            "links": farmLinks
        }
        farmList.append(farmDict)
    return farmList


def getFarm(organizationID, farmID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/farms/"+farmID, headers=header).json()

    farmType = response["@type"]
    name = response["name"]
    archived = response["archived"]
    farmId = response["id"]
    farmLinks = []
    for link in response["links"]:
        farmLinks.append(link)

    farmDict = {
        "type": farmType,
        "name": name,
        "archived": archived,
        "id": farmId,
        "links": farmLinks
    }
    return farmDict


def handler(event, context):
    if(os.environ.get('Authorization') is not None):
        authorization = os.environ['Authorization']

    header = {
        'Accept': 'application/vnd.deere.axiom.v3+json',
        'Content-Type': 'application/json',
        "Authorization": authorization
    }

    query = event["fieldName"]

    if query == "listClients":
        return listClients(organizationID=event['arguments']['organizationId'], header=header)

    if query == "getClient":
        return getClient(organizationID=event['arguments']['organizationId'], clientID=event['arguments']['clientId'], header=header)

    if query == "listFields":
        return listFields(organizationID=event['arguments']['organizationId'], header=header)

    if query == "getField":
        return getField(organizationID=event['arguments']['organizationId'], fieldID=event['arguments']['fieldId'], header=header)

    if query == "getBoundary":
        return getBoundary(organizationID=event['arguments']['organizationId'], fieldID=event['arguments']['fieldId'], header=header)

    if query == "listOrganizations":
        return listOrganizations(header=header)

    if query == "listFarms":
        return listFarms(organizationID=event['arguments']['organizationId'], header=header)

    if query == "getFarm":
        return getFarm(organizationID=event['arguments']['organizationId'], farmID=event['arguments']['farmId'], header=header)
