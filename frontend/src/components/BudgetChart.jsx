import React from 'react';

const BudgetChart = ({budget}) => (
  <div>
    {budget.map(item=>(
      <div className="flex items-center mb-2" key={item.name}>
        <div className="w-20">{item.name}</div>
        <div className="flex-grow bg-blue-400 h-5 rounded mr-2" style={{width: `${item.percent}%`}}></div>
        <div className="w-16 text-right font-bold">¥{item.amount}</div>
      </div>
    ))}
  </div>
);

export default BudgetChart;