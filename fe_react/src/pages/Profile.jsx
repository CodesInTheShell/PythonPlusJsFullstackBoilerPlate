import { useAtom } from 'jotai';
import { usernameAtom } from '../atoms/usernameAtom';
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Profile() {
  const [username] = useAtom(usernameAtom);
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await axios.get('http://127.0.0.1:8000/api/user/me', {
          headers: { 'x-access-token': token },
        });
        setUserData(response.data);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container">
      <h2>Profile</h2>
      <p>Username: {username}</p>
      {userData && <pre>{JSON.stringify(userData, null, 2)}</pre>}
    </div>
  );
}
