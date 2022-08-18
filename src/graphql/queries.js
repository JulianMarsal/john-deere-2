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
export const listOrganizationBoundaries = /* GraphQL */ `
  query ListOrganizationBoundaries($organizationId: ID!) {
    listOrganizationBoundaries(organizationId: $organizationId) {
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
      multipolygons {
        type
        rings {
          type
        }
      }
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
export const listFieldBoundaries = /* GraphQL */ `
  query ListFieldBoundaries($organizationId: ID!, $fieldId: ID!) {
    listFieldBoundaries(organizationId: $organizationId, fieldId: $fieldId) {
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
      multipolygons {
        type
        rings {
          type
        }
      }
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
  query ListClients($organizationId: ID!) {
    listClients(organizationId: $organizationId) {
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
  query GetClient($organizationId: ID!, $clientId: ID!) {
    getClient(organizationId: $organizationId, clientId: $clientId) {
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
export const listFarms = /* GraphQL */ `
  query ListFarms($organizationId: ID!) {
    listFarms(organizationId: $organizationId) {
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
  query GetFarm($organizationId: ID!, $farmId: ID!) {
    getFarm(organizationId: $organizationId, farmId: $farmId) {
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
export const listFields = /* GraphQL */ `
  query ListFields($organizationId: ID!) {
    listFields(organizationId: $organizationId) {
      type
      name
      archived
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const getField = /* GraphQL */ `
  query GetField($organizationId: ID!, $fieldId: String!) {
    getField(organizationId: $organizationId, fieldId: $fieldId) {
      type
      name
      archived
      id
      links {
        rel
        uri
      }
    }
  }
`;
export const getBoundary = /* GraphQL */ `
  query GetBoundary($organizationId: ID!, $fieldId: ID!, $boundaryId: ID!) {
    getBoundary(
      organizationId: $organizationId
      fieldId: $fieldId
      boundaryId: $boundaryId
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
      multipolygons {
        type
        rings {
          type
        }
      }
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
export const autenticationDeere = /* GraphQL */ `
  query AutenticationDeere {
    autenticationDeere
  }
`;
export const getAuthorizationToken = /* GraphQL */ `
  query GetAuthorizationToken($code: String!, $callback: String) {
    getAuthorizationToken(code: $code, callback: $callback)
  }
`;
export const listMachines = /* GraphQL */ `
  query ListMachines($organizationId: ID!) {
    listMachines(organizationId: $organizationId) {
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
  query ListOrganizationFiles($organizationId: ID!) {
    listOrganizationFiles(organizationId: $organizationId) {
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
