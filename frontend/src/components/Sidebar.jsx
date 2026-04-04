import React from 'react';

const Sidebar = ({active, onSelect}) => {
  const sections = [
    {title:"有关信息", items:["本次旅游需求","预算","每日交通详情","餐饮篇","住宿篇","景点篇","参考资料","实际开销"]},
    {title:"旅游准备", items:["本次物品清单","待办事项"]},
    {title:"后记", items:["游记","评估与回顾"]}
  ];

  return (
    <div className="w-56 bg-gray-800 text-white h-screen fixed overflow-y-auto p-4">
      {sections.map((section, idx)=>(
        <div key={idx} className="mb-6">
          <h3 className="text-yellow-400 uppercase font-bold mb-2">{section.title}</h3>
          <ul>
            {section.items.map(item=>(
              <li
                key={item}
                className={`p-2 cursor-pointer rounded ${active===item ? 'bg-yellow-400 text-gray-900 font-bold' : 'hover:bg-gray-700'}`}
                onClick={()=>onSelect(item)}
              >
                {item}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default Sidebar;