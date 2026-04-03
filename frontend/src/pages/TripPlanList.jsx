import React from 'react';
import { Plus, Calendar, MapPin, MoreVertical, Clock, CheckCircle2 } from 'lucide-react';

const TripPlanList = () => {
  // 模拟静态数据
  const mockTrips = [
    {
      id: 1,
      title: "2024 川西大环线：追寻雪山与草地",
      cover: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=1000",
      start_date: "2024-10-10",
      end_date: "2024-10-20",
      status: "planned",
      summary: "从成都出发，经康定、新都桥至稻城亚丁，全程自驾。"
    },
    {
      id: 2,
      title: "日本关西深度游：京都与奈良的古都祭",
      cover: "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&q=80&w=1000",
      start_date: "2023-05-12",
      end_date: "2023-05-20",
      status: "finished",
      summary: "体验和服，品尝地道怀石料理，感受枯山水美学。"
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* 顶部标题栏 */}
        <div className="flex justify-between items-end mb-10">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight">我的旅游攻略</h1>
            <p className="text-slate-500 mt-2 text-sm">共有 {mockTrips.length} 个旅行计划</p>
          </div>
          <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg font-medium transition-all shadow-sm">
            <Plus size={18} />
            <span>开始新旅行</span>
          </button>
        </div>

        {/* 列表网格 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {mockTrips.map((trip) => (
            <div key={trip.id} className="group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-xl hover:border-blue-200 transition-all cursor-pointer">
              {/* 卡片封面 */}
              <div className="relative h-48 overflow-hidden">
                <img 
                  src={trip.cover} 
                  alt={trip.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute top-4 left-4">
                  <span className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold shadow-sm ${
                    trip.status === 'finished' ? 'bg-green-500 text-white' : 'bg-blue-500 text-white'
                  }`}>
                    {trip.status === 'finished' ? <CheckCircle2 size={12}/> : <Clock size={12}/>}
                    {trip.status === 'finished' ? '已完成' : '规划中'}
                  </span>
                </div>
              </div>

              {/* 卡片内容 */}
              <div className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-lg font-bold text-slate-800 leading-snug group-hover:text-blue-600 transition-colors">
                    {trip.title}
                  </h3>
                  <button className="text-slate-400 hover:text-slate-600">
                    <MoreVertical size={18} />
                  </button>
                </div>
                
                <div className="flex items-center gap-2 text-slate-500 text-sm mb-4">
                  <Calendar size={14} />
                  <span>{trip.start_date} ~ {trip.end_date}</span>
                </div>

                <p className="text-slate-600 text-sm line-clamp-2 leading-relaxed">
                  {trip.summary}
                </p>
              </div>
            </div>
          ))}

          {/* 快速添加空位 */}
          <div className="border-2 border-dashed border-slate-200 rounded-2xl flex flex-col items-center justify-center p-8 hover:bg-white hover:border-blue-300 transition-all group cursor-pointer text-slate-400 hover:text-blue-500">
             <Plus size={32} className="mb-2 group-hover:scale-110 transition-transform" />
             <span className="font-medium">添加更多目的地</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TripPlanList;