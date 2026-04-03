import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import TripPlanList from './pages/TripPlanList'
import TripPlanEntry from './pages/TripPlanEntry'

// 注意：这里不再需要引入 './App.css'，因为样式都在 index.css 中通过 Tailwind 注入了
// 如果你有一些特殊的全局 CSS 也可以保留

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-white text-slate-900">
        <Routes>
          {/* 1. 旅游攻略清单 (首页) */}
          <Route path="/" element={<TripPlanList />} />

          {/* 2. 单个旅游攻略入口页 (详情页) */}
          {/* :id 是动态参数，方便后续根据 ID 从后端获取数据 */}
          <Route path="/trip/:id" element={<TripPlanEntry />} />

          {/* 如果访问不存在的路径，可以导向首页 */}
          <Route path="*" element={<TripPlanList />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App