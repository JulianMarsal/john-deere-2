/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const listOrganizations = /* GraphQL */ `
  query ListOrganizations {
    listOrganizations {
      type
      name
      member
      internal
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const listOrganizationGeometries = /* GraphQL */ `
  query ListOrganizationGeometries($organization_id: ID!) {
    listOrganizationGeometries(organization_id: $organization_id) {
      type
      name
      sourceType
      createdTime
      modifiedTime
      area {
        type
        valueAsDouble
        unit
      }
      workableArea {
        type
        valueAsDouble
        unit
      }
      geometry
      extent {
        type
        topLeft {
          lat
          lon
        }
        bottomRight {
          lat
          lon
        }
      }
      archived
      id
      active
      irrigated
    }
  }
`;
export const listFieldGeometries = /* GraphQL */ `
  query ListFieldGeometries($organization_id: ID!, $field_id: ID!) {
    listFieldGeometries(
      organization_id: $organization_id
      field_id: $field_id
    ) {
      type
      name
      sourceType
      createdTime
      modifiedTime
      area {
        type
        valueAsDouble
        unit
      }
      workableArea {
        type
        valueAsDouble
        unit
      }
      geometry
      extent {
        type
        topLeft {
          lat
          lon
        }
        bottomRight {
          lat
          lon
        }
      }
      archived
      id
      active
      irrigated
    }
  }
`;
export const listClients = /* GraphQL */ `
  query ListClients($organization_id: ID!) {
    listClients(organization_id: $organization_id) {
      name
      links {
        rel
        uri
      }
      id
      archived
    }
  }
`;
export const getClient = /* GraphQL */ `
  query GetClient($organization_id: ID!, $client_id: ID!) {
    getClient(organization_id: $organization_id, client_id: $client_id) {
      name
      links {
        rel
        uri
      }
      id
      archived
    }
  }
`;
export const listClientFarms = /* GraphQL */ `
  query ListClientFarms($organization_id: ID!, $client_id: ID!) {
    listClientFarms(organization_id: $organization_id, client_id: $client_id) {
      type
      name
      archived
      clientUri
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const listOrganizationFarms = /* GraphQL */ `
  query ListOrganizationFarms($organization_id: ID!) {
    listOrganizationFarms(organization_id: $organization_id) {
      type
      name
      archived
      clientUri
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const listFarmFields = /* GraphQL */ `
  query ListFarmFields($organization_id: ID!, $farm_id: ID!) {
    listFarmFields(organization_id: $organization_id, farm_id: $farm_id) {
      type
      name
      archived
      clientUri
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const getFarm = /* GraphQL */ `
  query GetFarm($organization_id: ID!, $farm_id: ID!) {
    getFarm(organization_id: $organization_id, farm_id: $farm_id) {
      type
      name
      archived
      clientUri
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const listOrganizationFields = /* GraphQL */ `
  query ListOrganizationFields($organization_id: ID!) {
    listOrganizationFields(organization_id: $organization_id) {
      type
      name
      archived
      id
      geometry
      links {
        rel
        uri
      }
    }
  }
`;
export const getField = /* GraphQL */ `
  query GetField($organization_id: ID!, $field_id: String!) {
    getField(organization_id: $organization_id, field_id: $field_id) {
      type
      name
      archived
      id
      geometry
      links {
        rel
        uri
      }
    }
  }
`;
export const getFieldOperations = /* GraphQL */ `
  query GetFieldOperations($operation_id: String!) {
    getFieldOperations(operation_id: $operation_id) {
      type
      fieldOperationType
      adaptMachineType
      cropSeason
      modifiedTime
      startDate
      endDate
      cropName
      orgId
      varieties {
        type
        productType
        name
        tankMix
      }
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const listFieldsOperations = /* GraphQL */ `
  query ListFieldsOperations($organization_id: ID!) {
    listFieldsOperations(organization_id: $organization_id) {
      type
      name
      archived
      id
      geometry
      links {
        rel
        uri
      }
    }
  }
`;
export const getGeometry = /* GraphQL */ `
  query GetGeometry($organization_id: ID!, $field_id: ID!, $boundary_id: ID!) {
    getGeometry(
      organization_id: $organization_id
      field_id: $field_id
      boundary_id: $boundary_id
    ) {
      type
      name
      sourceType
      createdTime
      modifiedTime
      area {
        type
        valueAsDouble
        unit
      }
      workableArea {
        type
        valueAsDouble
        unit
      }
      geometry
      extent {
        type
        topLeft {
          lat
          lon
        }
        bottomRight {
          lat
          lon
        }
      }
      archived
      id
      active
      irrigated
    }
  }
`;
export const listMachines = /* GraphQL */ `
  query ListMachines($organization_id: ID!) {
    listMachines(organization_id: $organization_id) {
      type
      visualizationCategory
      machineCategories
      telematicsState
      capabilities
      terminals
      displays
      guid
      contributionDefinitionID
      id
      name
      equipmentMake
      equipmentType
      equipmentApexType
      equipmentModel
      isSerialNumberCertified
      links {
        rel
        uri
      }
    }
  }
`;
export const listFiles = /* GraphQL */ `
  query ListFiles {
    listFiles {
      name
      type
      createdTime
      modifiedTime
      nativeSize
      source
      transferPending
      visibleViaShare
      shared
      new
      status
      archived
      format
      manufacturer
      delayProcessing
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const listOrganizationFiles = /* GraphQL */ `
  query ListOrganizationFiles($organization_id: ID!) {
    listOrganizationFiles(organization_id: $organization_id) {
      name
      type
      createdTime
      modifiedTime
      nativeSize
      source
      transferPending
      visibleViaShare
      shared
      new
      status
      archived
      format
      manufacturer
      delayProcessing
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const getFile = /* GraphQL */ `
  query GetFile($fileId: ID!) {
    getFile(fileId: $fileId) {
      name
      type
      createdTime
      modifiedTime
      nativeSize
      source
      transferPending
      visibleViaShare
      shared
      new
      status
      archived
      format
      manufacturer
      delayProcessing
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const getUserToken = /* GraphQL */ `
  query GetUserToken($id: ID!) {
    getUserToken(id: $id) {
      id
      userId
      provider
      name
      value
      createdAt
      updatedAt
    }
  }
`;
export const listUserTokens = /* GraphQL */ `
  query ListUserTokens(
    $filter: ModelUserTokenFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listUserTokens(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        userId
        provider
        name
        value
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
