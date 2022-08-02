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
  query GetBoundary($organizationId: ID!, $fieldId: ID!) {
    getBoundary(organizationId: $organizationId, fieldId: $fieldId) {
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
  query GetAuthorizationToken($code: String!) {
    getAuthorizationToken(code: $code)
  }
`;
