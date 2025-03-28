import React, { useState } from 'react';
import axios from 'axios';

const Upload = ({ user }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [file, setFile] = useState(null);
    const [password, setPassword] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description);
        formData.append('file', file);
        formData.append('password', password);
        formData.append('user', user.username);

        try {
            await axios.post('/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log('Upload successful');
        } catch (error) {
            console.error('Upload failed:', error);
        }
    };

    return (
        <div className="card">
            <h2>Upload Work</h2>
            <input
                type="text"
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />
            <input
                type="text"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.docx"
                onChange={handleFileChange}
            />
            <input
                type="password"
                placeholder="Password (optional)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleUpload}>Upload</button>
        </div>
    );
};

export default Upload;    