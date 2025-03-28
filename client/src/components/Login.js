import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setUser, setIsAdmin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async () => {
        try {
            const response = await axios.post('/api/login', { username, password });
            const { user } = response.data;
            localStorage.setItem('user', JSON.stringify(user));
            setUser(user);
            setIsAdmin(user.username === 'lqy');
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    return (
        <div className="card">
            <h2>Login</h2>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin}>Login</button>
        </div>
    );
};

export default Login;    