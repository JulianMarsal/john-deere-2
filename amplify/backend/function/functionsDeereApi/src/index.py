from ast import Not
import json
import logging
from pickle import FALSE
import requests
import os
import time
import boto3
import uuid


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def return_error(error_message, error_type):
    errors = {
        "errorType": error_type,
        "errorMessage": error_message,
        "errorInfo": "error_type",
    }
    return errors


def upload_json_s3(geojson, bucket="johndeere-upload-file-info"):
    id = str(uuid.uuid4())
    s3_client = boto3.client("s3", region_name="us-west-2")
    try:
        response = s3_client.put_object(Bucket=bucket, Body=geojson, Key=id + ".json")
    except Exception as e:
        logging.info("No se pudo subir el archivo al bucket")
        return False
    return f"{id}.json"


# str_geojson_region = upload_json_s3(json_geometry)
#     if str_geojson_region:
#         str_geojson_region = f"https://geojson-api-gateway.s3.us-west-2.amazonaws.com/{str_geojson_region}"


def list_clients(organization_id, header):

    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/clients",
        headers=header,
    ).json()
    # Check if the response is right

    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    client_list = []
    for cliente in response["values"]:
        client_dict = {}
        client_dict.update({"name": cliente["name"]})
        client_dict.update({"archived": cliente["archived"]})
        client_dict.update({"id": cliente["id"]})
        client_links = []
        for link in cliente["links"]:
            client_links.append(link)
        client_dict.update({"links": client_links})
        client_list.append(client_dict)
    return client_list


def get_client(organization_id, client_id, header):
    # Check if the client_id parameter is not empty
    if client_id == "":
        logger.error("The client_id cannot be empty")
        return None

    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/clients/"
        + client_id,
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    client_dict = {}
    client_dict.update({"name": response["name"]})
    client_dict.update({"archived": response["archived"]})
    client_dict.update({"id": response["id"]})
    client_links = []
    for link in response["links"]:
        client_links.append(link)
    client_dict.update({"links": client_links})
    return client_dict


def list_organization_fields(organization_id, header):

    errors = {
        "errorType": "MUTATION_ERROR",
        "errorMessage": "error_message",
        "errorInfo": "error_type",
    }
    # return return_error("error", "error")
    print("Primer check")
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/fields?embed=activeBoundary",
        headers=header,
    ).json()
    # Check if the response is right
    print("Segundo check")
    error = response
    print(f"segundo intento {error}")

    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        print("gatio")
        return "none"

    if response.get("@type") == "Errors":
        logger.error(f"Error in response:  {response}")
        return return_error(
            response["errors"][0]["message"], response["errors"][0]["@type"]
        )

    field_list = []
    print(f"la response de list organization field es: {response}")
    for field in response["values"]:

        field_dict = {}
        field_dict["type"] = field["@type"]
        field_dict["name"] = field["name"]
        field_dict["archived"] = field["archived"]
        field_dict["id"] = field["id"]
        field_links = []

        if field.get("boundaries"):
            field_dict["geometry"] = json.loads(
                multi_polygon_transformer(
                    field["boundaries"][0]["multipolygons"][0]["rings"]
                )
            )

        for link in field["links"]:
            field_links.append(link)

        field_dict["links"] = field_links
        field_list.append(field_dict)
    return field_list


def list_farm_fields(organization_id, farm_id, header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/farms/"
        + farm_id
        + "/fields",
        headers=header,
    ).json()

    # Check if the response is right
    print(f"La response pre error de farm f es : {response}")
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None
    print(f"La response post error farm f es : {response}")
    field_list = []
    for field in response["values"]:
        print(f"el field actuale es {field}")
        field_dict = {}
        field_dict["type"] = field["@type"]
        field_dict["name"] = field["name"]
        field_dict["archived"] = field["archived"]
        field_dict["id"] = field["id"]
        field_links = []
        fieldPrint = field["id"]
        print(f"el id del field es : {fieldPrint}")
        geometry = list_field_geometries(organization_id, field["id"], header)
        print(f"geometry response : {geometry}")

        # boundary_id = list_field_geometries(organization_id, field["id"], header)[0][
        #    "id"
        # ]
        for link in field["links"]:
            field_links.append(link)
            if link["rel"] == "boundaries" and len(geometry) != 0:
                boundary_id = list_field_geometries(
                    organization_id, field["id"], header
                )[0]["id"]
                field_dict["geometry"] = get_geometry(
                    organization_id, field["id"], boundary_id, header
                )
        field_dict["links"] = field_links
        field_list.append(field_dict)
    return field_list


def checkIfDownloadIsReady(list_fields, header):
    # This code will run in loop until all the responses return a 200 response o
    # The time is running out
    fields_in_query = list_fields
    fields_ready = []
    while len(fields_ready) != len(fields_in_query):
        for field in fields_in_query:
            response = requests.get(field.get("downloadLink"), headers=header)
            # Insertar la lógica de poop y push
            # response = requests.get(field.get("uri"), headers=header).json()

            print(
                f"Quedan {(len(fields_in_query) - len(fields_ready))} links pendientes. Y fields_ready tiene {len(fields_ready)} links listos"
            )
            # This was supossed to be a 202 code but in practice the app return a 200
            # Maybe in tha case of the 307 response return a 202 latter
            if response.status_code == 200:
                fields_ready.append(
                    [n for n in fields_in_query if n["name"] == field["name"]][0]
                )
                # fields_in_query.remove( field["name"])
            elif response.status_code == 406:
                # This response code is not supply necessary but in order to take some
                # precautions I wrote it just in case.
                print(f"Response code :{response.status_code}")
    print(
        f"Quedan {(len(fields_in_query) - len(fields_ready))} links pendientes Y fields_ready tiene: {len(fields_ready)} links listos"
    )
    time.sleep(2)
    return fields_ready


def list_fieldsOperations(organization_id, header):

    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/fields",
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    field_operation_list = []
    for field in response["values"]:
        field_dict = {}
        field_dict["name"] = field["name"]
        field_dict["id"] = field["id"]
        field_dict["downloadLink"] = {}
        for link in field["links"]:
            if link["rel"] == "fieldOperation":
                field_dict["downloadLink"] = link["uri"]
        field_operation_list.append(field_dict)
        # Mandar fieldOperationLinks y consultar por su estado 202.

    # uploadFileWithInfo(file, info, bucket)

    return checkIfDownloadIsReady(field_operation_list, header)

    return "fieldOperationDict"


def uploadFileWithInfo(file, info, bucket):

    return "Ok or not okey"


def get_field(organization_id, field_id, header):

    # Check if the field_id parameter is not empty
    if field_id == "":
        logger.error("The field_id cannot be empty")
        return None

    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/fields/"
        + field_id,
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    field_dict = {}
    field_dict["type"] = response["@type"]
    field_dict["name"] = response["name"]
    field_dict["archived"] = response["archived"]
    field_dict["id"] = response["id"]
    field_links = []
    geometry = list_field_geometries(organization_id, field_id, header)

    if len(geometry) != 0:
        boundary_id = list_field_geometries(organization_id, field_id, header)[0]["id"]

    for link in response["links"]:
        field_links.append(link)
        if link["rel"] == "boundaries" and len(geometry) != 0:
            field_dict["geometry"] = get_geometry(
                organization_id, field_dict["id"], boundary_id, header
            )["geometry"]

    field_dict["links"] = field_links
    return field_dict


def get_field_operations(operation_id, header):

    # Check if the field_id parameter is not empty
    if operation_id == "":
        logger.error("The operation_id cannot be empty")
        return None

    response = requests.get(
        "https://sandboxapi.deere.com/platform/fieldOperations/" + operation_id,
        headers=header,
    ).json()
    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None
    operations_dict = {}
    operations_dict["type"] = response["@type"]
    operations_dict["fieldOperationType"] = response["fieldOperationType"]
    operations_dict["adaptMachineType"] = response["adaptMachineType"]
    operations_dict["cropSeason"] = response["cropSeason"]
    operations_dict["modifiedTime"] = response["modifiedTime"]
    operations_dict["startDate"] = response["startDate"]
    operations_dict["endDate"] = response["endDate"]
    operations_dict["cropName"] = response["cropName"]
    operations_dict["orgId"] = response["orgId"]
    operations_dict["varieties"] = response["varieties"]
    operations_dict["id"] = response["id"]
    field_links = []
    for link in response["links"]:
        field_links.append(link)
    operations_dict["links"] = field_links
    return operations_dict


# def getHarvestResult(organization_id, field_id, header):

#     # Check if the field_id parameter is not empty
#     if (field_id == ""):
#         logger.error("The field_id cannot be empty")
#         return None

#     response = requests.get(
#         "https://sandboxapi.deere.com/platform/fieldOperations/NTg3NDU2XzYyZjUxMGNiZmYxZGFhZjI1YTJhOGJhMw/measurementTypes/HarvestYieldResult", headers=header).json()
#     print(f"response bla bla {response}")
#     # Check if the response is right
#     if response.get("faultcode"):
#         logger.error(f"Error in response:  {response}")
#         return None

#     operations_dict = {}
#     operations_dict["type"] = response["@type"]
#     operations_dict["measurementName"] = response["measurementName"]
#     operations_dict["measurementCategory"] = response["measurementCategory"]
#     operations_dict["area"] = response["area"]
#     operations_dict["yield"] = response["yield"]
#     operations_dict["averageYield"] = response["averageYield"]
#     operations_dict["averageMoisture"] = response["averageMoisture"]
#     operations_dict["wetMass"] = response["wetMass"]
#     operations_dict["averageWetMass"] = response["averageWetMass"]
#     operations_dict["averageSpeed"] = response["averageSpeed"]
#     operations_dict["varietyTotals"] = response["varietyTotals"]
#     operations_dict["productTotals"] = response["productTotals"]
#     field_links = []
#     for link in response["links"]:
#         field_links.append(link)
#     operations_dict["links"] = field_links
#     return operations_dict


def multi_polygon_transformer(multi_polygons):
    featureCollection = {"type": "FeatureCollection", "features": []}

    for polygon in multi_polygons:

        geometry = {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Polygon", "coordinates": []},
        }
        multi_polygon = []
        for point in polygon["points"]:
            multi_polygon.append([point["lon"], point["lat"]])

        geometry["geometry"]["coordinates"].append(multi_polygon)
        geometry["properties"].update(
            {"type": polygon["type"], "passable": polygon["passable"]}
        )

        featureCollection["features"].append(geometry)

    return json.dumps(featureCollection)


def get_geometry(organization_id, field_id, boundary_id, header):

    # Check if the field_id parameter is not empty
    if field_id == "":
        logger.error("The field_id cannot be empty")
        return None

    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/fields/"
        + field_id
        + "/boundaries/"
        + boundary_id,
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    name = response["name"]
    Type = response["@type"]
    area = response["area"]
    workeableArea = response["workableArea"]
    sourceType = response["sourceType"]
    # Takes the multipolygon field in the response and transforms it into another format. It then returns it as a string.
    geometry = multi_polygon_transformer(response["multipolygons"][0]["rings"])
    extent = response["extent"]
    active = response["active"]
    archived = response["archived"]
    Id = response["id"]
    modifiedTime = response["modifiedTime"]
    createdTime = response["createdTime"]
    irrigated = response["irrigated"]

    boundary_dict = {
        "type": Type,
        "id": Id,
        "name": name,
        "area": area,
        "workableArea": workeableArea,
        "sourceType": sourceType,
        "geometry": geometry,
        "extent": extent,
        "active": active,
        "archived": archived,
        "modifiedTime": modifiedTime,
        "createdTime": createdTime,
        "irrigated": irrigated,
    }

    return boundary_dict


def list_organization_geometries(organization_id, header):

    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/boundaries",
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    boundary_list = []
    for boundary in response["values"]:
        boundary_dict = {}
        boundary_dict["type"] = boundary["@type"]
        boundary_dict["name"] = boundary["name"]
        boundary_dict["area"] = boundary["area"]
        boundary_dict["workableArea"] = boundary["workableArea"]
        boundary_dict["sourceType"] = boundary["sourceType"]
        boundary_dict["multipolygons"] = boundary["multipolygons"]
        boundary_dict["extent"] = boundary["extent"]
        boundary_dict["active"] = boundary["active"]
        boundary_dict["archived"] = boundary["archived"]
        boundary_dict["id"] = boundary["id"]
        boundary_dict["modifiedTime"] = boundary["modifiedTime"]
        boundary_dict["createdTime"] = boundary["createdTime"]
        boundary_dict["irrigated"] = boundary["irrigated"]
        boundary_links = []
        for link in boundary["links"]:
            boundary_links.append(link)
        boundary_dict["links"] = boundary_links
        boundary_list.append(boundary_dict)

    return boundary_list


def list_field_geometries(organization_id, field_id, header):

    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/fields/"
        + field_id
        + "/boundaries",
        headers=header,
    ).json()

    # Check if the response is right
    print(f"La response pre error es de list_field_geometries  : {response}")
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None
    print(f"La response es de list_field_geometries: {response}")
    boundary_list = []
    for boundary in response["values"]:
        boundary_dict = {}
        boundary_dict["type"] = boundary["@type"]
        boundary_dict["name"] = boundary["name"]
        boundary_dict["area"] = boundary["area"]
        boundary_dict["workableArea"] = boundary["workableArea"]
        boundary_dict["sourceType"] = boundary["sourceType"]
        # Ver si esta bien puesto el dumps o sacarlo y ponerlo en multi
        boundary_dict["geometry"] = multi_polygon_transformer(
            boundary["multipolygons"][0]["rings"]
        )

        boundary_dict["extent"] = boundary["extent"]
        boundary_dict["active"] = boundary["active"]
        boundary_dict["archived"] = boundary["archived"]
        boundary_dict["id"] = boundary["id"]
        boundary_dict["modifiedTime"] = boundary["modifiedTime"]
        boundary_dict["createdTime"] = boundary["createdTime"]
        boundary_dict["irrigated"] = boundary["irrigated"]
        boundary_links = []
        for link in boundary["links"]:
            boundary_links.append(link)
        boundary_dict["links"] = boundary_links
        boundary_list.append(boundary_dict)
        print(f"El boundary list es: {boundary_list}")
    return boundary_list


def list_organizations(header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/", headers=header
    )

    # Check if the response is right
    # try:
    #     if (response["faultcode"] is not None):
    #         logger.error(f"Error in response:  {response}")
    #         return None
    # except:
    #     pass
    status_code = response.status_code
    response = response.json()
    if response.get("faultcode") or status_code != 200:
        logger.error("Error in response: {response}")
        return None

    organization_list = []
    try:
        for organization in response["values"]:
            organization_dict = {}
            organization_dict.update({"type": organization["type"]})
            organization_dict.update({"name": organization["name"]})
            organization_dict.update({"member": organization["member"]})
            organization_dict.update({"internal": organization["internal"]})
            organization_dict.update({"id": organization["id"]})
            organization_dict.update({"isConected": True})
            organization_links = []
            for link in organization["links"]:
                organization_links.append(link)
            organization_dict.update({"links": organization_links})
            organization_list.append(organization_dict)

    except Exception as e:
        logging.error(
            "The follow error is found in the values of the response, error in prop: "
            + str(e)
        )
        return None
    return organization_list


def list_organization_farms(organization_id, header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/farms",
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    farmList = []
    for farm in response["values"]:
        farmType = farm["@type"]
        name = farm["name"]
        archived = farm["archived"]
        farm_id = farm["id"]
        farm_links = []
        clientUri = ""
        internal = ""
        for link in farm["links"]:
            farm_links.append(link)

        farmDict = {
            "type": farmType,
            "name": name,
            "archived": archived,
            "id": farm_id,
            "links": farm_links,
            "clientUri": clientUri,
            "internal": internal,
        }
        farmList.append(farmDict)
    return farmList


def list_client_farms(organization_id, client_id, header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/clients/"
        + client_id
        + "/farms",
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    farmList = []
    for farm in response["values"]:
        farmType = farm["@type"]
        name = farm["name"]
        archived = farm["archived"]
        farm_id = farm["id"]
        farm_links = []
        clientUri = ""
        internal = ""
        for link in farm["links"]:
            farm_links.append(link)

        farmDict = {
            "type": farmType,
            "name": name,
            "archived": archived,
            "id": farm_id,
            "links": farm_links,
            "clientUri": clientUri,
            "internal": internal,
        }
        farmList.append(farmDict)
    return farmList


def get_farm(organization_id, farm_id, header):

    # Check if the farm_id parameter is not empty
    if farm_id == "":
        logger.error("The farm_id cannot be empty")
        return None

    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/farms/"
        + farm_id,
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    farmType = response["@type"]
    name = response["name"]
    archived = response["archived"]
    farm_id = response["id"]
    farm_links = []
    for link in response["links"]:
        farm_links.append(link)

    farmDict = {
        "type": farmType,
        "name": name,
        "archived": archived,
        "id": farm_id,
        "links": farm_links,
    }
    return farmDict


def list_machines(organization_id, header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/machines",
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    machine_list = []
    for machine in response["values"]:
        machine_dict = {}
        machine_dict["type"] = machine["@type"]
        machine_dict["visualizationCategory"] = machine["visualizationCategory"]
        machine_dict["machineCategories"] = machine["machineCategories"]
        machine_dict["telematicsState"] = machine["telematicsState"]
        machine_dict["capabilities"] = machine["capabilities"]
        machine_dict["terminals"] = machine["terminals"]
        machine_dict["displays"] = machine["displays"]
        machine_dict["guid"] = machine["GUID"]
        machine_dict["contributionDefinitionID"] = machine["contributionDefinitionID"]
        machine_dict["id"] = machine["id"]
        machine_dict["name"] = machine["name"]
        machine_dict["equipmentMake"] = machine["equipmentMake"]
        machine_dict["equipmentType"] = machine["equipmentType"]
        machine_dict["equipmentApexType"] = machine["equipmentApexType"]
        machine_dict["equipmentModel"] = machine["equipmentModel"]
        machine_dict["isSerialNumberCertified"] = machine["isSerialNumberCertified"]
        machine_links = []
        for link in machine["links"]:
            machine_links.append(link)
        machine_dict["links"] = machine["links"]
        machine_list.append(machine_dict)

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
    return machine_list


def get_file(file_id, header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/files/" + file_id, headers=header
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    file_dict = {}
    file_dict["name"] = response["name"]
    file_dict["type"] = response["type"]
    file_dict["createdTime"] = response["createdTime"]
    file_dict["modifiedTime"] = response["modifiedTime"]
    file_dict["nativeSize"] = response["nativeSize"]
    file_dict["source"] = response["source"]
    file_dict["transferPending"] = response["transferPending"]
    file_dict["visibleViaShare"] = response["visibleViaShare"]
    file_dict["shared"] = response["shared"]
    file_dict["new"] = response["new"]
    file_dict["status"] = response["status"]
    file_dict["archived"] = response["archived"]
    file_dict["format"] = response["format"]
    file_dict["manufacturer"] = response["manufacturer"]
    file_dict["delayProcessing"] = response["delayProcessing"]
    file_dict["id"] = response["id"]
    file_dict["links"] = response["links"]
    return file_dict


def list_files(header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/files", headers=header
    ).json()
    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    file_list = []
    for file_item in response["values"]:
        file_dict = {}
        file_dict["name"] = file_item["name"]
        file_dict["type"] = file_item["type"]
        file_dict["createdTime"] = file_item["createdTime"]
        file_dict["modifiedTime"] = file_item["modifiedTime"]
        file_dict["nativeSize"] = file_item["nativeSize"]
        file_dict["source"] = file_item["source"]
        file_dict["transferPending"] = file_item["transferPending"]
        file_dict["visibleViaShare"] = file_item["visibleViaShare"]
        file_dict["shared"] = file_item["shared"]
        file_dict["new"] = file_item["new"]
        file_dict["status"] = file_item["status"]
        file_dict["archived"] = file_item["archived"]
        file_dict["format"] = file_item["format"]
        file_dict["manufacturer"] = file_item["manufacturer"]
        file_dict["delayProcessing"] = file_item["delayProcessing"]
        file_dict["id"] = file_item["id"]
        file_dict["links"] = file_item["links"]
        file_list.append(file_dict)

    return file_list


def list_organization_files(organization_id, header):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/organizations/"
        + organization_id
        + "/files",
        headers=header,
    ).json()

    # Check if the response is right
    if response.get("faultcode"):
        logger.error(f"Error in response:  {response}")
        return None

    file_list = []
    for file_item in response["values"]:
        file_dict = {}
        file_dict["name"] = file_item["name"]
        file_dict["type"] = file_item["type"]
        file_dict["createdTime"] = file_item["createdTime"]
        file_dict["modifiedTime"] = file_item["modifiedTime"]
        file_dict["nativeSize"] = file_item["nativeSize"]
        file_dict["source"] = file_item["source"]
        file_dict["transferPending"] = file_item["transferPending"]
        file_dict["visibleViaShare"] = file_item["visibleViaShare"]
        file_dict["shared"] = file_item["shared"]
        file_dict["new"] = file_item["new"]
        file_dict["status"] = file_item["status"]
        file_dict["archived"] = file_item["archived"]
        file_dict["format"] = file_item["format"]
        file_dict["manufacturer"] = file_item["manufacturer"]
        file_dict["delayProcessing"] = file_item["delayProcessing"]
        file_dict["id"] = file_item["id"]
        file_dict["links"] = file_item["links"]
        file_list.append(file_dict)

    return file_list


def validate_request_with_deere(token):
    response = requests.get(
        "https://sandboxapi.deere.com/platform/",
        headers={
            "Authorization": token,
            "Accept": "application/vnd.deere.axiom.v3+json",
        },
    )
    print(f"Y el status code de la response es: {response.status_code}")
    # .Ok check and return true if the status code is lesser than 400. oterwhise return false.
    return response.ok


def evaluate_request(event):
    # Redundant code, refactor near
    token = event["request"]["headers"]["authorizationtoken"]
    # Return true or false depending of the validation result
    return validate_request_with_deere(token)


def handler(event, context):
    print(f"event:  {event}")
    # Check if the AuthorizationToken exist in the headers
    if event.get("request").get("headers").get("authorizationtoken"):
        # Evaluate if the accessToken is still valid
        if evaluate_request(event):

            authorization = event["request"]["headers"]["authorizationtoken"]
        else:
            logger.error(
                "The accessToken is invalid or not found in the AuthorizationHeader"
            )
            return return_error(
                "The accessToken is invalid or not found in the AuthorizationHeader",
                "authorization error",
            )
    else:
        try:
            authorization = os.environ["Authorization"]
            if not validate_request_with_deere(authorization):
                logger.error(
                    "The bearer token in the env variables is not work or has expired "
                )
                return return_error(
                    "The bearer token in the env variables is not work or has expired ",
                    "authorization error",
                )
        except Exception as e:
            logger.error(
                "Authorization is not set in the environment variables",
            )
            return return_error(
                "Authorization is not set in the environment variables",
                "authorization error",
            )

    header = {
        "Accept": "application/vnd.deere.axiom.v3+json",
        "Content-Type": "application/json",
        "Authorization": authorization,
    }

    query = event["fieldName"]
    print(f"query:  {query}")
    if (
        query != "getFile"
        and query != "listOrganizations"
        and query != "listFiles"
        and query != "getFieldOperations"
    ):
        organization_id = event["arguments"].get("organization_id")
        if event["arguments"]["organization_id"] == "":
            logger.error("The organization_id cannot be empty")
            return None

    if query == "listClients":
        return list_clients(organization_id, header=header)

    if query == "getClient":
        return get_client(
            organization_id,
            client_id=event["arguments"]["client_id"],
            header=header,
        )

    if query == "listOrganizationFields":
        return list_organization_fields(organization_id, header=header)

    if query == "listFieldsOperations":
        return list_fieldsOperations(organization_id, header=header)

    if query == "getField":
        return get_field(
            organization_id,
            field_id=event["arguments"]["field_id"],
            header=header,
        )

    if query == "getFieldOperations":
        return get_field_operations(
            operation_id=event["arguments"]["operation_id"], header=header
        )

    if query == "listOrganizationGeometries":
        return list_organization_geometries(organization_id, header=header)

    if query == "listFieldGeometries":
        return list_field_geometries(
            organization_id,
            field_id=event["arguments"]["field_id"],
            header=header,
        )

    if query == "getGeometry":
        return get_geometry(
            organization_id,
            field_id=event["arguments"]["field_id"],
            boundary_id=event["arguments"]["boundary_id"],
            header=header,
        )

    if query == "listOrganizations":
        return list_organizations(header=header)

    if query == "listOrganizationFarms":
        return list_organization_farms(organization_id, header=header)

    if query == "listClientFarms":
        return list_client_farms(
            organization_id,
            client_id=event["arguments"]["client_id"],
            header=header,
        )

    if query == "listFarmFields":
        return list_farm_fields(
            organization_id,
            farm_id=event["arguments"]["farm_id"],
            header=header,
        )

    if query == "getFarm":
        return get_farm(
            organization_id,
            farm_id=event["arguments"]["farm_id"],
            header=header,
        )

    if query == "listMachines":
        return list_machines(organization_id, header=header)

    if query == "getFile":
        return get_file(file_id=event["arguments"]["file_id"], header=header)

    if query == "listFiles":
        return list_files(header=header)

    if query == "listOrganizationFiles":
        return list_organization_files(organization_id, header=header)
