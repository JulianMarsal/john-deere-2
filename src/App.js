import React from "react";
import { useQuery, gql } from "@apollo/client";
import './App.css';
//import { OauthPopup } from "react-oauth-popup";
//const axios = require('axios');


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
  }
`;

// let headers = {
//   'Accept': 'application/vnd.deere.axiom.v3+json',
//   'Content-Type': 'application/vnd.deere.axiom.v3+json',
//   'x-api-key': 'da2-54xou2rprjhyxlirj5zmwdds74'
// }

const onCode = (code, params) => {
  console.log("wooooo a code", code);
  console.log("alright! the URLSearchParams interface from the popup url", params);
}

const onClose = () => console.log("closed!");



function App() {

  // <OauthPopup
  //   url="http://FriendlyMultiNationalTechConglomerate.com"
  //   onCode={onCode}
  //   onClose={onClose}
  // >
  //   <div>Click me to open a Popup</div>
  // </OauthPopup>

  const { data, loading, error } = useQuery(FILMS_QUERY);

  if (loading) return "Loading...";
  if (error) return <pre>Error:{error.message}</pre>
  return (
    <div>
      <h1>listFields</h1>
      <ul>
        {data.listFields.map((org) => (
          <li >
            <div >Name: {org.name}</div>
            <div >Type: {org.type}</div>
            <div >ID: {org.id}</div>
            <div >Archived: {org.archived}</div>

            {org.links.map((link) => (
              <div key={link.rel + 1}>
                <div >Rel: {link.rel}</div>
                <div >URI: {link.uri}</div>
              </div>
            ))}
            <br />
          </li>
        ))}
      </ul>
      <h1>listOrganizations</h1>
      <ul>
        {data.listOrganizations.map((org) => (
          <li key={org.id}>
            <div>Name: {org.name}</div>
            <div>ID: {org.id}</div>
            <div>Internal: {org.internal}</div>
            <div>Member: {org.member}</div>
            <div>Type: {org.type}</div>
            <br />
            {org.links.map((link) => (
              <div>
                <div key={link.rel}>Rel: {link.rel}</div>
                <div key={link.uri}>URI: {link.uri}</div>
              </div>
            ))}
            <text>{`${""}\n`}</text>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
