import { useAtom } from 'jotai';
import { usernameAtom } from './atoms/usernameAtom';
import { Route, Routes, Navigate, Link, useNavigate } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Profile from './pages/Profile';
import 'bootstrap/dist/css/bootstrap.min.css';
import Dashboard from './pages/Dashboard';

function isAuthenticated() {
  return localStorage.getItem('isAuthenticated') === 'true';
}

function ProtectedRoute({ element }) {
  return isAuthenticated() ? element : <Navigate to="/login" />;
}

function PublicRoute({ element }) {
  return isAuthenticated() ? <Navigate to="/dashboard" /> : element;
}

function App() {
  const [, setUsername] = useAtom(usernameAtom);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('isAuthenticated');
    setUsername(''); // Clear username from Jotai
    navigate('/login');
  };

  return (
    
    <div className="app">
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container">
          <Link className="navbar-brand" to="/">My App</Link>
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">Home</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/profile">Profile</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/dashboard">Dashboard</Link>
            </li>
            <li className="nav-item">
              {!isAuthenticated() ? (
                <Link className="nav-link" to="/login">Login</Link>
              ) : (
                <button className="btn btn-link nav-link" onClick={handleLogout}>Logout</button>
              )}
            </li>
          </ul>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<PublicRoute element={<Home />} />} />
        <Route path="/login" element={<PublicRoute element={<Login />} />} />
        <Route path="/dashboard" element={<ProtectedRoute element={<Dashboard />} />} />
        <Route path="/profile" element={<ProtectedRoute element={<Profile />} />} />
      </Routes>
    </div>
  );
}

export default App;
