import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="container">
      <h1>Welcome to My App</h1>
      <Link to="/login" className="btn btn-primary">Go to Login</Link>
    </div>
  );
}