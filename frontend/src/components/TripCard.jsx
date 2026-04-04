import React from 'react';

const TripCard = ({trip}) => (
  <div className="bg-white rounded-lg p-2 w-60 cursor-pointer shadow hover:shadow-lg">
    <img src={trip.cover || "/images/placeholder.png"} alt={trip.name} className="rounded mb-2" />
    <h3 className="text-lg font-semibold">{trip.name}</h3>
    <p className="text-gray-500 text-sm">{trip.startDate} - {trip.endDate} | {trip.city}</p>
  </div>
);

export default TripCard;