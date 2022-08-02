import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ApolloProvider, ApolloClient, createHttpLink, InMemoryCache } from "@apollo/client";
import { setContext } from '@apollo/client/link/context';


const httpLink = createHttpLink({
  uri: 'https://w7ozev7n2nd2fkzmh623e5suy4.appsync-api.us-east-1.amazonaws.com/graphql',
});


const authLink = setContext((_, { headers }) => {

  // return the headers to the context so httpLink can read them
  return {
    headers: {
      ...headers,
      'Accept': 'application/vnd.deere.axiom.v3+json',
      'x-api-key': "da2-54xou2rprjhyxlirj5zmwdds74",
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
