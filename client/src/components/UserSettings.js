import React, { useState } from 'react';
import axios from 'axios';

const UserSettings = ({ user, setUser }) => {
    const [newNickname, setNewNickname] = useState(user.nickname || '');
    const [newPassword, setNewPassword] = useState('');

    const updateNickname = async () => {
        try {
            const response = await axios.put(`/api/users/${user._id}`, {
                nickname: newNickname,
            });
            const updatedUser = response.data;
            localStorage.setItem('user', JSON.stringify(updatedUser));
            setUser(updatedUser);
        } catch (error) {
            console.error('Failed to update nickname:', error);
        }
    };

    const updatePassword = async () => {
        try {
            await axios.put(`/api/users/${user._id}`, {
                password: newPassword,
            });
            console.log('Password updated successfully');
        } catch (error) {
            console.error('Failed to update password:', error);
        }
    };

    const deleteAccount = async () => {
        try {
            await axios.delete(`/api/users/${user._id}`);
            localStorage.removeItem('user');
            setUser(null);
        } catch (error) {
            console.error('Failed to delete account:', error);
        }
    };

    return (
        <div className="card">
            <h2>User Settings</h2>
            <input
                type="text"
                placeholder="Nickname"
                value={newNickname}
                onChange={(e) => setNewNickname(e.target.value)}
            />
            <button onClick={updateNickname}>Update Nickname</button>
            <input
                type="password"
                placeholder="New Password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
            />
            <button onClick={updatePassword}>Update Password</button>
            <button onClick={deleteAccount}>Delete Account</button>
        </div>
    );
};

export default UserSettings;    