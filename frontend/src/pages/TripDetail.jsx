import React, {useState, useEffect} from 'react';
import Sidebar from '../components/Sidebar';
import TripCard from '../components/TripCard';
import TripTable from '../components/TripTable';
import BudgetChart from '../components/BudgetChart';

const TripDetail = () => {
  const [activeMenu, setActiveMenu] = useState("本次旅游需求");
  const [trip, setTrip] = useState({});
  const [days, setDays] = useState([]);
  const [budget, setBudget] = useState([]);

  useEffect(()=>{
    // 示例 fetch，可替换为真实 API
    fetch('/api/trip-detail/1')
      .then(res=>res.json())
      .then(data=>{
        setTrip(data.trip);
        setDays(data.days);
        setBudget(data.budget);
      });
  },[]);

  return (
    <div className="flex">
      <Sidebar active={activeMenu} onSelect={setActiveMenu}/>
      <div className="ml-56 p-6 flex-1">
        <div className="mb-4">
          <img src={trip.cover || "/images/placeholder.png"} alt="封面" className="w-full h-64 object-cover rounded mb-2"/>
          <h1 className="text-3xl font-bold">{trip.name}</h1>
          <p>{trip.startDate} - {trip.endDate}</p>
        </div>
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">行程概述</h2>
          <p>{trip.overview}</p>
        </div>
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">行程核心亮点</h2>
          <ul>
            {trip.highlights?.map((h,i)=><li key={i}>{h}</li>)}
          </ul>
        </div>
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">行程地图</h2>
          <img src={trip.map || "/images/placeholder.png"} alt="行程地图" className="rounded w-full"/>
        </div>
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">行程总览</h2>
          <TripTable days={days}/>
        </div>
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">预算汇总</h2>
          <BudgetChart budget={budget}/>
        </div>
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">子行程</h2>
          <div className="flex flex-wrap gap-4">
            {trip.subTrips?.map(st=><TripCard key={st.id} trip={st}/>)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TripDetail;