import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Upload from './components/Upload';
import Share from './components/Share';
import Archive from './components/Archive';
import UserSettings from './components/UserSettings';
import './styles.css';

function App() {
    const [isAdmin, setIsAdmin] = useState(false);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            const parsedUser = JSON.parse(storedUser);
            setUser(parsedUser);
            setIsAdmin(parsedUser.username === 'lqy');
        }
    }, []);

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login setUser={setUser} setIsAdmin={setIsAdmin} />} />
                <Route path="/register" element={<Register />} />
                <Route
                    path="/dashboard"
                    element={<Dashboard user={user} isAdmin={isAdmin} />}
                />
                <Route path="/upload" element={<Upload user={user} />} />
                <Route path="/share" element={<Share user={user} isAdmin={isAdmin} />} />
                <Route path="/archive" element={<Archive user={user} isAdmin={isAdmin} />} />
                <Route path="/settings" element={<UserSettings user={user} setUser={setUser} />} />
            </Routes>
        </Router>
    );
}

export default App;    