import json
import logging
import requests
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def listClients(organizationID, header):

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/clients", headers=header).json()
    # Check if the response is right
    try:
        if (response["faultcode"] is not None):
            logger.error("Error in response: " + response)
            return None
    except:
        pass
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
    # Check if the clientID parameter is not empty
    if (clientID == ""):
        logger.error("The clientID cannot be empty")
        return None

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/clients/"+clientID, headers=header).json()

    # Check if the response is right
    try:
        if (response["faultcode"] is not None):
            logger.error("Error in response: " + response)
            return None
    except:
        pass

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

    # Check if the response is right
    try:
        if (response["faultcode"] is not None):
            logger.error("Error in response: " + response)
            return None
    except:
        pass

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

    # Check if the fieldID parameter is not empty
    try:
        if (response["faultcode"] is not None):
            logger.error(response)
            return None
    except:
        pass

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields/"+fieldID, headers=header).json()

    # Check if the response is right
    try:
        if (response["faultcode"] is not None):
            logger.error("Error in response: " + response)
            return None
    except:
        pass

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

    # Check if the fieldID parameter is not empty
    if (fieldID == ""):
        logger.error("The fieldID cannot be empty")
        return None

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields/"+fieldID+"/    ", headers=header, auth={}).json()

    # Check if the response is right
    try:
        if (response["faultcode"] is not None):
            logger.error("Error in response: " + response)
            return None
    except:
        pass

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
        logger.debug("No boundaries found")
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

    # Check if the response is right
    try:
        if (response["faultcode"] is not None):
            logger.error("Error in response: " + response)
            return None
    except:
        pass

    organizationList = []
    try:
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
        # return organizationList
    except Exception as e:
        logging.error(
            "The follow error is found in the values of the response, error in prop: " + str(e))
        return None
    return organizationList


def listFarms(organizationID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/farms", headers=header).json()

    # Check if the response is right
    try:
        if (response["faultcode"] is not None):
            logger.error("Error in response: " + response)
            return None
    except:
        pass

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

    # Check if the farmID parameter is not empty
    if (farmID == ""):
        logger.error("The farmID cannot be empty")
        return None

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/farms/"+farmID, headers=header).json()

    # Check if the response is right
    try:
        if (response["faultcode"] is not None):
            logger.error("Error in response: " + response)
            return None
    except:
        pass

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
    try:
        authorization = os.environ['Authorization']
    except Exception as e:
        logger.error("Authorization is not set in the environment variables")
        return None

    header = {
        'Accept': 'application/vnd.deere.axiom.v3+json',
        'Content-Type': 'application/json',
        "Authorization": authorization
    }

    query = event["fieldName"]
    print("query: " + query)
    if (query != "listOrganizations"):
        organizationId = event['arguments']['organizationId']
        if (event['arguments']['organizationId'] == ""):
            logger.error("The organizationId cannot be empty")
            return None

    if query == "listClients":
        return listClients(organizationID=organizationId, header=header)

    if query == "getClient":
        return getClient(organizationID=organizationId, clientID=event['arguments']['clientId'], header=header)

    if query == "listFields":
        return listFields(organizationID=organizationId, header=header)

    if query == "getField":
        return getField(organizationID=organizationId, fieldID=event['arguments']['fieldId'], header=header)

    if query == "getBoundary":
        return getBoundary(organizationID=organizationId, fieldID=event['arguments']['fieldId'], header=header)

    if query == "listOrganizations":
        return listOrganizations(header=header)

    if query == "listFarms":
        return listFarms(organizationID=organizationId, header=header)

    if query == "getFarm":
        return getFarm(organizationID=organizationId, farmID=event['arguments']['farmId'], header=header)
