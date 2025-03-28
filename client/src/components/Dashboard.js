import React from 'react';
import axios from 'axios';

const Dashboard = ({ user, isAdmin }) => {
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

    return (
        <div className="card">
            <h2>Dashboard</h2>
            {works.map((work) => (
                <div key={work._id} className="card">
                    <h3>{work.title}</h3>
                    <p>{work.description}</p>
                    {isAdmin || work.password === '' ? (
                        <a href={work.link}>View</a>
                    ) : (
                        <input type="password" placeholder="Enter password" />
                    )}
                </div>
            ))}
        </div>
    );
};

export default Dashboard;    