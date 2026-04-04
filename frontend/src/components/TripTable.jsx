import React from 'react';

const TripTable = ({days}) => (
  <table className="w-full border-collapse">
    <thead>
      <tr className="bg-blue-500 text-white">
        <th className="p-2">第几天</th>
        <th>日期</th>
        <th>城市</th>
        <th>交通</th>
        <th>主要景点</th>
        <th>主要餐饮</th>
        <th>备注</th>
      </tr>
    </thead>
    <tbody>
      {days.map(day=>(
        <tr key={day.id} className="hover:bg-gray-100">
          <td className="p-2">{day.day}</td>
          <td>{day.date}</td>
          <td>{day.city}</td>
          <td>{day.transport}</td>
          <td>{day.spot}</td>
          <td>{day.food}</td>
          <td>{day.note}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default TripTable;