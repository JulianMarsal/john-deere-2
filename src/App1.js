import React from "react";
import { useQuery, gql } from "@apollo/client";
import './App.css';
//import { OauthPopup } from "react-oauth-popup";
//const axios = require('axios');
import { useState } from "react";



const FILMS_QUERY = gql`
{

  listFields(organizationId: "578354") {
    archived
    id
    links {
      rel
      uri
    }
    name
    type
  }
  listOrganizations {
    id
    internal
    links {
      uri
      rel
    }
    member
    name
    type
  }
  listFarms(organizationId: "578354") {
    archived
    clientUri
    id
    links {
      rel
      uri
    }
    name
    type
  }
  listClients(organizationId: "578354") {
    archived
    id
    links {
      rel
      uri
    }
    name
  }
  getClient(clientId: "545d2b1e-0000-1000-7ff0-e1e1e1257010", organizationId: "578354") {
    archived
    id
    links {
      rel
      uri
    }
    name
  }
}
`;

// let headers = {
//   'Accept': 'application/vnd.deere.axiom.v3+json',
//   'Content-Type': 'application/vnd.deere.axiom.v3+json',
//   'x-api-key': 'da2-54xou2rprjhyxlirj5zmwdds74'
// }


function App() {
  const [currentQuery, setCurrentQuery] = useState("");
  //const [showFields, setShowFields] = useState(false);
  const { data, loading, error } = useQuery(FILMS_QUERY);
  //const [listOrganizations, setListOrganizations] = useState(data.listOrganizations);


  if (loading) return "Loading...";
  if (error) return `Error getting response! ${error.message}`;

  return (

    <div>
      <button onClick={() => setCurrentQuery("listOrganizations")}> listOrganizations </button>
      <button onClick={() => setCurrentQuery("listFields")}>listFields</button>
      <button onClick={() => setCurrentQuery("listFarms")}> listFarms </button>
      <button onClick={() => setCurrentQuery("listClients")}>listClients</button>
      <button onClick={() => setCurrentQuery("getClient")}>getClient f9052cfa-e006-4d24-af59-a39f3239a3e3</button>
      {currentQuery === "listOrganizations" && <div>
        <h1>listOrganizations</h1>
        <ul>
          {data.listOrganizations.map((org) => (
            <li key={org.id}>
              <div>Name: {org.name}</div>
              <div>ID: {org.id}</div>
              <div>Internal: {org.internal ? "True" : "False"}</div>
              <div>Member: {org.member ? "True" : "False"}</div>
              <div>Type: {org.type}</div>
              <br />
              {org.links.map((link) => (
                <div>
                  <div key={link.rel}>Rel: {link.rel}</div>
                  <div key={link.uri}>URI: {link.uri}</div>
                </div>
              ))}
              <text>{`${""} \n`}</text>
            </li>
          ))}
        </ul>

      </div>
      }

      {currentQuery === "listFields" && <div>
        <h1>listFields</h1>
        <ul>
          {data.listFields.map((org) => (
            <li>
              <div>Name: {org.name}</div>
              <div>Type: {org.type}</div>
              <div>ID: {org.id}</div>
              <div>Archived: {org.archived ? "True" : "False"}</div>

              {org.links.map((link) => (
                <div key={link.rel + 1}>
                  <div>Rel: {link.rel}</div>
                  <div>URI: {link.uri}</div>
                </div>
              ))}
              <br />
            </li>
          ))}
        </ul>
      </div>
      }

      {
        currentQuery === "listFarms" && <div>
          <h1>listFarms</h1>
          <ul>
            {data.listFarms.map((farm) => (
              <li key={farm.id}>
                <div>Name: {farm.name}</div>
                <div>ID: {farm.id}</div>
                <div>Internal: {farm.internal}</div>
                <div>Archived: {farm.archived ? "True" : "False"}</div>
                <div>Type: {farm.type}</div>
                <div>ClientUri: {farm.clientUri}</div>
                <br />
                {farm.links.map((link) => (
                  <div>
                    <div key={link.rel}>Rel: {link.rel}</div>
                    <div key={link.uri}>URI: {link.uri}</div>
                  </div>
                ))}
                <text>{`${""} \n`}</text>
              </li>
            ))}
          </ul>



        </div>
      }

      {currentQuery === "listClients" && <div>
        <h1>listClients</h1>
        <ul>
          {data.listClients.map((client) => (
            <li >
              <di>Name: {client.name}</di>
              <di>ID: {client.id}</di>
              <di>Archived: {client.archived ? "True" : "False"}</di>
              {client.links.map((link) => (
                <div key={link.rel + 1}>
                  <di>Rel: {link.rel}</di>
                  <di>URI: {link.uri}</di>
                </div>
              ))}
              <br />
            </li>
          ))}
        </ul>
      </div>
      }

      {currentQuery === "getClient" && <div>
        <h1>getClient with id: 545d2b1e-0000-1000-7ff0-e1e1e1257010</h1>

        <li >
          <div>Name: {data.getClient.name}</div>
          <div>ID: {data.getClient.id}</div>
          <div>Archived: {data.getClient.archived ? "True" : "False"}</div>
          {data.getClient.links.map((link) => (
            <div key={link.rel + 1}>
              <div >Rel: {link.rel}</div>
              <div >URI: {link.uri}</div>
            </div>
          ))}
          <br />
        </li>
      </div>
      }
    </div>



  )

}
// eslint-disable-next-line
//const [listFields, setlistFields] = useState("");
// const [listOrganizations, setlistOrganizations] = useState("");

// const getOrganizations = () => {
//   const {data, loading, error} = useQuery(list_Fields_query);

// }
// eslint-disable-next-line
//const {data, loading, error} = useQuery(list_organizations_query);
//setCurrentQuery("listFields")
//setCurrentQuery("listFields")
//const currentQuery = "listFields";

export default App;

// const { data, loading, error } = useQuery(FILMS_QUERY);

//   if (loading) return "Loading...";
//   if (error) return <pre>Error:{error.message}</pre>
//   return (
//     <div>
//       <h1>listFields</h1>
//       <ul>
//         {data.listFields.map((org) => (
//           <li >
//             <div >Name: {org.name}</div>
//             <div >Type: {org.type}</div>
//             <div >ID: {org.id}</div>
//             <div >Archived: {org.archived}</div>

//             {org.links.map((link) => (
//               <div key={link.rel + 1}>
//                 <div >Rel: {link.rel}</div>
//                 <div >URI: {link.uri}</div>
//               </div>
//             ))}
//             <br />
//           </li>
//         ))}
//       </ul>
//       <h1>listOrganizations</h1>
//       <ul>
//         {data.listOrganizations.map((org) => (
//           <li key={org.id}>
//             <div>Name: {org.name}</div>
//             <div>ID: {org.id}</div>
//             <div>Internal: {org.internal}</div>
//             <div>Member: {org.member}</div>
//             <div>Type: {org.type}</div>
//             <br />
//             {org.links.map((link) => (
//               <div>
//                 <div key={link.rel}>Rel: {link.rel}</div>
//                 <div key={link.uri}>URI: {link.uri}</div>
//               </div>
//             ))}
//             <text>{`${""} \n`}</text>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }