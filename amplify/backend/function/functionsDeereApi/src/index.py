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

    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

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
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

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
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

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
    if (fieldID == ""):
        logger.error("The fieldID cannot be empty")
        return None

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields/"+fieldID, headers=header).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

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


def getBoundary(organizationID, fieldID, boundaryID, header):

    # Check if the fieldID parameter is not empty
    if (fieldID == ""):
        logger.error("The fieldID cannot be empty")
        return None

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields/"+fieldID+"/boundaries/" + boundaryID, headers=header).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

    name = response["name"]
    Type = response["@type"]
    area = response["area"]
    workeableArea = response["workableArea"]
    sourceType = response["sourceType"]
    multipolygons = response["multipolygons"]
    extent = response["extent"]
    active = response["active"]
    archived = response["archived"]
    Id = response["id"]
    modifiedTime = response["modifiedTime"]
    createdTime = response["createdTime"]
    irrigated = response["irrigated"]

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


def listOrganizationBoundaries(organizationID, header):

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/boundaries", headers=header).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

    boundaryList = []
    for boundary in response["values"]:
        boundaryDict = {}
        boundaryDict["type"] = boundary["@type"]
        boundaryDict["name"] = boundary["name"]
        boundaryDict["area"] = boundary["area"]
        boundaryDict["workableArea"] = boundary["workableArea"]
        boundaryDict["sourceType"] = boundary["sourceType"]
        boundaryDict["multipolygons"] = boundary["multipolygons"]
        boundaryDict["extent"] = boundary["extent"]
        boundaryDict["active"] = boundary["active"]
        boundaryDict["archived"] = boundary["archived"]
        boundaryDict["id"] = boundary["id"]
        boundaryDict["modifiedTime"] = boundary["modifiedTime"]
        boundaryDict["createdTime"] = boundary["createdTime"]
        boundaryDict["irrigated"] = boundary["irrigated"]
        boundaryLinks = []
        for link in boundary["links"]:
            boundaryLinks.append(link)
        boundaryDict["links"] = boundaryLinks
        boundaryList.append(boundaryDict)
    return boundaryList


def listFieldBoundaries(organizationID, fieldID, header):

    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/fields/"+fieldID+"/boundaries", headers=header).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

    boundaryList = []
    for boundary in response["values"]:
        boundaryDict = {}
        boundaryDict["type"] = boundary["@type"]
        boundaryDict["name"] = boundary["name"]
        boundaryDict["area"] = boundary["area"]
        boundaryDict["workableArea"] = boundary["workableArea"]
        boundaryDict["sourceType"] = boundary["sourceType"]
        boundaryDict["multipolygons"] = boundary["multipolygons"]
        boundaryDict["extent"] = boundary["extent"]
        boundaryDict["active"] = boundary["active"]
        boundaryDict["archived"] = boundary["archived"]
        boundaryDict["id"] = boundary["id"]
        boundaryDict["modifiedTime"] = boundary["modifiedTime"]
        boundaryDict["createdTime"] = boundary["createdTime"]
        boundaryDict["irrigated"] = boundary["irrigated"]
        boundaryLinks = []
        for link in boundary["links"]:
            boundaryLinks.append(link)
        boundaryDict["links"] = boundaryLinks
        boundaryList.append(boundaryDict)
    return boundaryList


def listOrganizations(header):
    print("Variable de Auth: ")
    print(os.environ['Authorization'])
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/", headers=header).json()

    # Check if the response is right
    # try:
    #     if (response["faultcode"] is not None):
    #         logger.error("Error in response: " + response)
    #         return None
    # except:
    #     pass
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

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
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

    farmList = []
    for farm in response["values"]:
        farmType = farm["@type"]
        name = farm["name"]
        archived = farm["archived"]
        farmId = farm["id"]
        farmLinks = []
        clientUri = ""
        internal = ""
        for link in farm["links"]:
            farmLinks.append(link)
        print("")

        farmDict = {
            "type": farmType,
            "name": name,
            "archived": archived,
            "id": farmId,
            "links": farmLinks,
            "clientUri": clientUri,
            "internal": internal
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
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

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


def listMachines(organizationID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/machines", headers=header).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

    MachineList = []
    for machine in response["values"]:
        machineDict = {}
        # ver que onda esta nomenglatura
        machineDict["type"] = machine["@type"]
        machineDict["visualizationCategory"] = machine["visualizationCategory"]
        machineDict["machineCategories"] = machine["machineCategories"]
        machineDict["telematicsState"] = machine["telematicsState"]
        machineDict["capabilities"] = machine["capabilities"]
        machineDict["terminals"] = machine["terminals"]
        machineDict["displays"] = machine["displays"]
        machineDict["guid"] = machine["GUID"]
        machineDict["contributionDefinitionID"] = machine["contributionDefinitionID"]
        machineDict["id"] = machine["id"]
        machineDict["name"] = machine["name"]
        machineDict["equipmentMake"] = machine["equipmentMake"]
        machineDict["equipmentType"] = machine["equipmentType"]
        machineDict["equipmentApexType"] = machine["equipmentApexType"]
        machineDict["equipmentModel"] = machine["equipmentModel"]
        machineDict["isSerialNumberCertified"] = machine["isSerialNumberCertified"]
        machineLinks = []
        for link in machine["links"]:
            machineLinks.append(link)
        machineDict["links"] = machine["links"]
        MachineList.append(machineDict)

    Type = "String"
    visualizationCategory = "String"
    machineCategories = "AWSJSON"
    telematicsState = "String"
    capabilities = "String"  # Este es una lista de anda a saber que
    terminals = "AWSJSON"
    displays = "AWSJSON"
    guid = "String"  # GuID
    contributionDefinitionID = "ID"  # O string, anda a saber
    Id = "ID"
    name = "String"
    equipmentMake = "AWSJSON"
    equipmentType = "AWSJSON"
    equipmentApexType = "AWSJSON"
    equipmentModel = "AWSJSON"
    isSerialNumberCertified = "Boolean"
    links = "[Link]"
    return MachineList


def getFile(fileID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/files/" +
                            fileID, headers=header).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

    fileDict = {}
    fileDict["name"] = response["name"]
    fileDict["type"] = response["type"]
    fileDict["createdTime"] = response["createdTime"]
    fileDict["modifiedTime"] = response["modifiedTime"]
    fileDict["nativeSize"] = response["nativeSize"]
    fileDict["source"] = response["source"]
    fileDict["transferPending"] = response["transferPending"]
    fileDict["visibleViaShare"] = response["visibleViaShare"]
    fileDict["shared"] = response["shared"]
    fileDict["new"] = response["new"]
    fileDict["status"] = response["status"]
    fileDict["archived"] = response["archived"]
    fileDict["format"] = response["format"]
    fileDict["manufacturer"] = response["manufacturer"]
    fileDict["delayProcessing"] = response["delayProcessing"]
    fileDict["id"] = response["id"]
    fileDict["links"] = response["links"]
    return fileDict


def listFiles(header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/files", headers=header).json()
    # Check if the response is right
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

    fileList = []
    for fileItem in response["values"]:
        fileDict = {}
        fileDict["name"] = fileItem["name"]
        fileDict["type"] = fileItem["type"]
        fileDict["createdTime"] = fileItem["createdTime"]
        fileDict["modifiedTime"] = fileItem["modifiedTime"]
        fileDict["nativeSize"] = fileItem["nativeSize"]
        fileDict["source"] = fileItem["source"]
        fileDict["transferPending"] = fileItem["transferPending"]
        fileDict["visibleViaShare"] = fileItem["visibleViaShare"]
        fileDict["shared"] = fileItem["shared"]
        fileDict["new"] = fileItem["new"]
        fileDict["status"] = fileItem["status"]
        fileDict["archived"] = fileItem["archived"]
        fileDict["format"] = fileItem["format"]
        fileDict["manufacturer"] = fileItem["manufacturer"]
        fileDict["delayProcessing"] = fileItem["delayProcessing"]
        fileDict["id"] = fileItem["id"]
        fileDict["links"] = fileItem["links"]
        fileList.append(fileDict)

    return fileList


def listOrganizationFiles(organizationID, header):
    response = requests.get("https://sandboxapi.deere.com/platform/organizations/" +
                            organizationID+"/files", headers=header).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error("Error in response: " + response)
        return None

    fileList = []
    for fileItem in response["values"]:
        fileDict = {}
        fileDict["name"] = fileItem["name"]
        fileDict["type"] = fileItem["type"]
        fileDict["createdTime"] = fileItem["createdTime"]
        fileDict["modifiedTime"] = fileItem["modifiedTime"]
        fileDict["nativeSize"] = fileItem["nativeSize"]
        fileDict["source"] = fileItem["source"]
        fileDict["transferPending"] = fileItem["transferPending"]
        fileDict["visibleViaShare"] = fileItem["visibleViaShare"]
        fileDict["shared"] = fileItem["shared"]
        fileDict["new"] = fileItem["new"]
        fileDict["status"] = fileItem["status"]
        fileDict["archived"] = fileItem["archived"]
        fileDict["format"] = fileItem["format"]
        fileDict["manufacturer"] = fileItem["manufacturer"]
        fileDict["delayProcessing"] = fileItem["delayProcessing"]
        fileDict["id"] = fileItem["id"]
        fileDict["links"] = fileItem["links"]
        fileList.append(fileDict)

    return fileList


def handler(event, context):
    print()
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
    if (query != "getFile" and query != "listOrganizations" and query != "listFiles"):
        organizationId = event['arguments'].get("organizationId")
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

    if query == "listOrganizationBoundaries":
        return listOrganizationBoundaries(organizationID=organizationId, header=header)

    if query == "listFieldBoundaries":
        return listFieldBoundaries(organizationID=organizationId, fieldID=event['arguments']['fieldId'], header=header)

    if query == "getBoundary":
        return getBoundary(organizationID=organizationId, fieldID=event['arguments']['fieldId'], boundaryID=event['arguments']['boundaryId'], header=header)

    if query == "listOrganizations":
        return listOrganizations(header=header)

    if query == "listFarms":
        return listFarms(organizationID=organizationId, header=header)

    if query == "getFarm":
        return getFarm(organizationID=organizationId, farmID=event['arguments']['farmId'], header=header)

    if query == "listMachines":
        return listMachines(organizationID=organizationId, header=header)

    if query == "getFile":
        return getFile(fileID=event['arguments']['fileId'], header=header)

    if query == "listFiles":
        return listFiles(header=header)

    if query == "listOrganizationFiles":
        return listOrganizationFiles(organizationID=organizationId, header=header)
