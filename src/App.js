import './App.css';
import { useAuth0 } from "@auth0/auth0-react";

function App() {
    const { loginWithRedirect, logout, user, isAuthenticated } = useAuth0();

    return (
        <div className="App">
            <h1>Conectar con myJD/Autorizar acceso</h1>
            <ul>
                <li><button onClick={loginWithRedirect}>Conectar con JD</button></li>
                {/* <li><button onClick={logout}>Logout</button></li> */}
            </ul>
            <h2>User is {isAuthenticated ? "Logged in" : "Not logged in"}</h2>
            {isAuthenticated && (
                <p>{JSON.stringify(user, null, 2)}</p>
            )}
        </div>
    );
}

export default App;