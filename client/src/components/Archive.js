import React, { useState } from 'react';
import axios from 'axios';

const Archive = ({ user, isAdmin }) => {
    const [archives, setArchives] = useState([]);
    const [newArchiveName, setNewArchiveName] = useState('');

    const fetchArchives = async () => {
        try {
            const response = await axios.get('/api/archives');
            setArchives(response.data);
        } catch (error) {
            console.error('Failed to fetch archives:', error);
        }
    };

    const createArchive = async () => {
        try {
            await axios.post('/api/archives', { name: newArchiveName });
            fetchArchives();
            setNewArchiveName('');
        } catch (error) {
            console.error('Failed to create archive:', error);
        }
    };

    React.useEffect(() => {
        fetchArchives();
    }, []);

    return (
        <div className="card">
            <h2>Archive</h2>
            <input
                type="text"
                placeholder="New Archive Name"
                value={newArchiveName}
                onChange={(e) => setNewArchiveName(e.target.value)}
            />
            <button onClick={createArchive}>Create Archive</button>
            {archives.map((archive) => (
                <div key={archive._id} className="card">
                    <h3>{archive.name}</h3>
                    {/* 子归档逻辑可以在这里添加 */}
                </div>
            ))}
        </div>
    );
};

export default Archive;    