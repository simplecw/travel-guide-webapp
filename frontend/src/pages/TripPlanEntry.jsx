import React from 'react';
import { useParams, Link } from 'react-router-dom';
// 导入所有需要的图标，修复之前的 ReferenceError
import { 
  MapPin, 
  CalendarDays, 
  ListChecks, 
  NotebookText, 
  DollarSign, 
  Clock, 
  Utensils, 
  BusFront, 
  PlusCircle, 
  Search, 
  ChevronRight, 
  Download,
  DatabaseBackup
} from 'lucide-react';

// 模拟数据 (后续将通过后端 API 获取)
const mockTripData = {
  id: "1",
  title: "2026 河南走廊",
  subtitle: "丝路长歌：河西走廊五城寻味与揽胜之旅",
  coverImage: "https://images.unsplash.com/photo-1623869273418-e39d48689539?q=80&w=2000", // 替换为莫高窟或沙漠大图
  mapIllustration: "https://i.imgur.com/k9b6B4z.png", // 替换为你设计图中的插画地图 URL
  sections: [
    { id: 'transport', title: '相关线路', icon: BusFront },
    { id: 'lodging', title: '住宿酒店', icon: NotebookText },
    { id: 'notes', title: '游玩笔记', icon: ListChecks },
    { id: 'budget', title: '费用支出', icon: DollarSign },
  ],
  schedule: [
    { day: 1, date: '08-15', location: '兰州', activity: '抵达兰州，中山桥夜景，正宁路夜市' },
    { day: 2, date: '08-16', location: '武威', activity: '雷台汉墓 (马踏飞燕)，雷台公馆' },
    { day: 3, date: '08-17', location: '张掖', activity: '七彩丹霞 (日落)，大佛寺' },
    { day: 4, date: '08-18', location: '嘉峪关', activity: '嘉峪关关城，长城第一墩' },
    { day: 5, date: '08-19', location: '敦煌', activity: '莫高窟，鸣沙山月牙泉 (日落)' },
    { day: 6, date: '08-20', location: '敦煌', activity: '雅丹魔鬼城，玉门关' },
  ],
  gallery: [
    { id: 1, title: '七彩丹霞', url: 'https://images.unsplash.com/photo-1596120409252-92b0c34547d2?q=80&w=600' },
    { id: 2, title: '马踏飞燕', url: 'https://images.unsplash.com/photo-1624823183311-6677f37f374c?q=80&w=600' },
    { id: 3, title: '嘉峪关城楼', url: 'https://images.unsplash.com/photo-1616110300976-59114d59040a?q=80&w=600' },
    { id: 4, title: '莫高窟九层楼', url: 'https://images.unsplash.com/photo-1632766343054-f897f26c2e36?q=80&w=600' },
  ]
};

function TripPlanEntry() {
  const { id } = useParams(); // 获取 URL 中的 ID (例如 /trip/1)
  
  // 在实际开发中，这里会有一个 useEffect 调用后端接口
  // const [trip, setTrip] = useState(null);
  const trip = mockTripData; // 暂时使用模拟数据

  if (!trip) return <div className="p-10 text-slate-500">正在加载...</div>;

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* 1. 顶部大图 (封面) */}
      <div className="h-[28vh] w-full relative overflow-hidden">
        <img 
          src={trip.coverImage} 
          alt="封面图" 
          className="w-full h-full object-cover object-center"
        />
        <div className="absolute inset-0 bg-black/10"></div> {/* 遮罩层，增加文字可读性 */}
      </div>

      <div className="flex-grow flex">
        {/* 2. Notion 风格侧边栏 */}
        <aside className="w-64 border-r border-slate-100 p-6 flex flex-col gap-10 sticky top-0 h-[72vh]">
          {/* 返回首页和图标 */}
          <div className="flex items-center gap-3">
            <Link to="/" className="text-slate-400 hover:text-sky-600">
              <DatabaseBackup size={20} />
            </Link>
            <span className="text-4xl">🏛️</span>
          </div>

          {/* 页面目录 */}
          <nav className="space-y-1">
            <h2 className="text-sm font-semibold text-slate-400 px-3 mb-2">目录</h2>
            {trip.sections.map(section => (
              <a href={`#${section.id}`} key={section.id} className="group flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-50 text-slate-700">
                <section.icon size={18} className="text-slate-400 group-hover:text-sky-600" />
                <span className="group-hover:text-sky-700">{section.title}</span>
              </a>
            ))}
          </nav>

          {/* 快捷操作 */}
          <div className="mt-auto space-y-3">
            <button className="w-full flex items-center gap-2 justify-center bg-sky-600 text-white py-2 rounded-md hover:bg-sky-700 text-sm font-medium">
              <Download size={16} />
              导出 PDF
            </button>
          </div>
        </aside>

        {/* 3. 主内容区域 */}
        <main className="flex-1 p-12">
          {/* 标题区 */}
          <header className="mb-10">
            <p className="text-sm text-sky-700 font-medium mb-1">TRIP ID: #{id}</p>
            <h1 className="text-5xl font-extrabold text-slate-950 mb-3">{trip.title}</h1>
            <p className="text-xl text-slate-600 font-light max-w-2xl">{trip.subtitle}</p>
          </header>

          {/* 4. 插画地图区 */}
          <div className="mb-12 border border-slate-100 rounded-2xl p-6 bg-slate-50/50">
            <img 
              src={trip.mapIllustration} 
              alt="河西走廊插画地图" 
              className="w-full h-auto rounded-xl shadow-sm"
            />
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-10">
            {/* 左侧：详细行程列表 (占 2 列) */}
            <div className="xl:col-span-2 space-y-12">
              <section id="transport">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-3 bg-sky-100 text-sky-700 rounded-xl">
                    <CalendarDays size={24} />
                  </div>
                  <h2 className="text-3xl font-bold">每日详细行程</h2>
                </div>
                
                <div className="space-y-4">
                  {trip.schedule.map((day, index) => (
                    <div key={index} className="flex gap-4 p-5 border border-slate-100 rounded-xl hover:border-sky-100 hover:bg-sky-50/30 transition-all cursor-pointer group">
                      <div className="w-16 flex-shrink-0 text-center border-r border-slate-100 pr-4">
                        <div className="text-2xl font-black text-sky-700">D{day.day}</div>
                        <div className="text-sm text-slate-400 font-mono">{day.date}</div>
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <MapPin size={16} className="text-slate-400" />
                          <h4 className="text-lg font-semibold text-slate-900">{day.location}</h4>
                        </div>
                        <p className="text-slate-600 text-sm">{day.activity}</p>
                      </div>
                      <ChevronRight size={20} className="text-slate-300 group-hover:text-sky-500 self-center" />
                    </div>
                  ))}
                </div>
              </section>

              {/* 5. 景点美图墙 (根据图片 0 调整) */}
              <section id="gallery">
                <h3 className="text-2xl font-semibold mb-6 text-slate-800">景点图集</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {trip.gallery.map(img => (
                    <div key={img.id} className="relative group overflow-hidden rounded-xl h-40 shadow-inner">
                      <img src={img.url} alt={img.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300" />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent p-3 flex items-end">
                        <p className="text-xs text-white/90 font-medium">{img.title}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            </div>

            {/* 右侧：统计块和清单 */}
            <div className="space-y-10 sticky top-12 h-fit">
              {/* 预算统计 (设计图右侧块) */}
              <div className="p-7 bg-slate-950 text-white rounded-2xl shadow-xl space-y-6">
                <div className="flex justify-between items-center">
                  <h3 className="text-xl font-bold">预算总览</h3>
                  <DollarSign size={22} className="text-sky-400" />
                </div>
                <div className="text-5xl font-extrabold text-sky-400">¥ 7,850</div>
                <div className="w-full h-3 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full bg-sky-500 rounded-full" style={{width: '65%'}}></div>
                </div>
                <div className="flex justify-between text-sm text-slate-400">
                  <span>已支出: ¥5,100</span>
                  <span>剩余: ¥2,750</span>
                </div>
              </div>

              {/* 住宿酒店块 */}
              <div id="lodging" className="p-6 border border-slate-100 rounded-2xl bg-white shadow-sm space-y-4">
                <div className="flex items-center gap-2 text-slate-800 font-semibold">
                  <NotebookText size={20} className="text-amber-500" />
                  <h4>住宿安排</h4>
                </div>
                <ul className="text-sm text-slate-600 space-y-2 list-disc list-inside">
                  <li>兰州: 黄河丽景酒店 (1晚)</li>
                  <li>敦煌: 沙漠帐篷露营 (1晚)</li>
                  <li>其他: 速8酒店 (3晚)</li>
                </ul>
              </div>

              {/* 后续可以扩展 AI 生成建议块 */}
            </div>
          </div>

          {/* 页脚 */}
          <footer className="mt-24 border-t border-slate-100 pt-10 text-center text-slate-400 text-xs">
            Travel Planner Pro | © 2026 基于 React + FastAPI + Docker 构建
          </footer>
        </main>
      </div>
    </div>
  );
}

export default TripPlanEntry;