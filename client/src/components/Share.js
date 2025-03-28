import React from 'react';
import axios from 'axios';

const Share = ({ user, isAdmin }) => {
    const [works, setWorks] = React.useState([]);

    React.useEffect(() => {
        const fetchWorks = async () => {
            try {
                const response = await axios.get('/api/works');
                setWorks(response.data);
            } catch (error) {
                console.error('Failed to fetch works:', error);
            }
        };
        fetchWorks();
    }, []);

    const generateShareLink = (workId) => {
        return `${window.location.origin}/share/${workId}`;
    };

    return (
        <div className="card">
            <h2>Share Works</h2>
            {works.map((work) => (
                <div key={work._id} className="card">
                    <h3>{work.title}</h3>
                    <p>{work.description}</p>
                    <input
                        type="text"
                        value={generateShareLink(work._id)}
                        readOnly
                    />
                </div>
            ))}
        </div>
    );
};

export default Share;    