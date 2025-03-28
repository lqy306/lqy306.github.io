import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [invitationCode, setInvitationCode] = useState('');

    const handleRegister = async () => {
        try {
            await axios.post('/api/register', { username, password, invitationCode });
            console.log('Registration successful');
        } catch (error) {
            console.error('Registration failed:', error);
        }
    };

    return (
        <div className="card">
            <h2>Register</h2>
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
            <input
                type="text"
                placeholder="Invitation Code"
                value={invitationCode}
                onChange={(e) => setInvitationCode(e.target.value)}
            />
            <button onClick={handleRegister}>Register</button>
        </div>
    );
};

export default Register;    