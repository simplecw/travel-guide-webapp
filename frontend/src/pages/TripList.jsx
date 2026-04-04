import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import TripCard from '../components/TripCard';
import { useNavigate } from 'react-router-dom'; // React Router v6

const TripList = () => {
  const [activeMenu, setActiveMenu] = useState("本次旅游需求");
  const [trips, setTrips] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // 示例 fetch，可替换为真实 API
    fetch('/api/trip-list')
      .then(res => res.json())
      .then(data => {
        setTrips(data.trips);
      });
  }, []);

  const handleCardClick = (id) => {
    navigate(`/trip-detail/${id}`);
  };

  return (
    <div className="flex">
      <Sidebar active={activeMenu} onSelect={setActiveMenu} />
      <div className="ml-56 p-6 flex-1">
        <h1 className="text-3xl font-bold mb-6">我的旅游攻略</h1>
        <div className="flex flex-wrap gap-6">
          {trips.map(trip => (
            <div key={trip.id} onClick={() => handleCardClick(trip.id)}>
              <TripCard trip={trip} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TripList;