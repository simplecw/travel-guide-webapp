-- 1. 主表：旅游攻略
CREATE TABLE trip_plan (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',

    title VARCHAR(255) NOT NULL COMMENT '行程标题',

    card_cover_image VARCHAR(500) 
        COMMENT '列表卡片封面图',

    hero_image VARCHAR(500) 
        COMMENT '详情页顶部主题图',

    start_date DATE COMMENT '开始日期',
    end_date DATE COMMENT '结束日期',

    status ENUM('planned','finished') 
        DEFAULT 'planned' COMMENT '行程状态',

    summary TEXT COMMENT '行程简介',

    highlights TEXT COMMENT '行程亮点',

    route_map_image VARCHAR(500) 
        COMMENT '整体路线图',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_trip_date (start_date, end_date),
    INDEX idx_trip_status (status)

) COMMENT='旅游攻略主表';

-- 2. 行程总览表（首页表格）
CREATE TABLE trip_overview (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    trip_id BIGINT NOT NULL COMMENT '行程ID',

    day_number INT COMMENT '第几天',

    date DATE COMMENT '日期',

    city VARCHAR(255) COMMENT '城市',

    transport VARCHAR(255) COMMENT '交通',

    attractions TEXT COMMENT '景点',

    food TEXT COMMENT '餐饮',

    note TEXT COMMENT '备注',

    sort_order INT COMMENT '排序',

    INDEX idx_overview_trip (trip_id),
    INDEX idx_overview_sort (trip_id, sort_order)

) COMMENT='行程总览';


-- 3. 子行程表
CREATE TABLE sub_trip (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',

    trip_id BIGINT NOT NULL COMMENT '所属行程ID',

    title VARCHAR(255) COMMENT '子行程标题',

    card_cover_image VARCHAR(500) 
        COMMENT '子行程卡片封面图（入口页卡片使用）',

    hero_image VARCHAR(500) 
        COMMENT '子行程主题图（子行程页顶部大图）',

    map_image_1 VARCHAR(500) 
        COMMENT '景点分布图1',

    map_image_2 VARCHAR(500) 
        COMMENT '景点分布图2',

    map_image_3 VARCHAR(500) 
        COMMENT '景点分布图3',

    start_date DATE COMMENT '开始日期',
    end_date DATE COMMENT '结束日期',

    city VARCHAR(255) COMMENT '城市',

    summary TEXT COMMENT '子行程简介',

    sort_order INT DEFAULT 0 COMMENT '排序',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
        COMMENT '创建时间',

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP 
        COMMENT '更新时间',

    INDEX idx_sub_trip_trip (trip_id),
    INDEX idx_sub_trip_sort (trip_id, sort_order),
    INDEX idx_sub_trip_date (start_date),

    CONSTRAINT fk_sub_trip_trip
        FOREIGN KEY (trip_id) REFERENCES trip_plan(id)
        ON DELETE CASCADE

) COMMENT='子行程表';


-- 4. 子行程每日安排表
CREATE TABLE sub_trip_day_schedule (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '每日安排ID',
    sub_trip_id BIGINT NOT NULL COMMENT '所属子行程ID',
    date DATE NOT NULL COMMENT '具体日期',
    summary TEXT COMMENT '全天安排概要',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    CONSTRAINT fk_day_subtrip FOREIGN KEY (sub_trip_id)
        REFERENCES sub_trip(id)
        ON DELETE CASCADE
) COMMENT='子行程每日安排表，记录每天的概览';


-- 5. 时间轴表
CREATE TABLE sub_trip_day_timeline (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '时间轴ID',
    day_schedule_id BIGINT NOT NULL COMMENT '所属每日安排ID',
    time_range VARCHAR(50) COMMENT '时间段，例如：08:00-09:00',
    place_name VARCHAR(255) COMMENT '景点/地点名称',
    place_url VARCHAR(500) COMMENT '景点页面超链接',
    note TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    CONSTRAINT fk_timeline_day FOREIGN KEY (day_schedule_id)
        REFERENCES sub_trip_day_schedule(id)
        ON DELETE CASCADE
) COMMENT='子行程时间轴表，每天按时间顺序记录景点安排';


-- 6. 餐饮表
CREATE TABLE sub_trip_day_meal (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '餐饮ID',
    day_schedule_id BIGINT NOT NULL COMMENT '所属每日安排ID',
    meal_type ENUM('早餐','午餐','晚餐','小吃','饮品') NOT NULL COMMENT '餐别',
    restaurant_name VARCHAR(255) COMMENT '餐厅名称',
    note TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    CONSTRAINT fk_meal_day FOREIGN KEY (day_schedule_id)
        REFERENCES sub_trip_day_schedule(id)
        ON DELETE CASCADE
) COMMENT='子行程每日餐饮安排表';


-- 7. 交通表
CREATE TABLE sub_trip_day_transport (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '交通ID',
    day_schedule_id BIGINT NOT NULL COMMENT '所属每日安排ID',
    start_location VARCHAR(255) COMMENT '起止位置',
    transport_mode VARCHAR(50) COMMENT '交通方式，例如：高铁/地铁/公交/出租/自驾',
    cost DECIMAL(10,2) COMMENT '费用（元）',
    note TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    CONSTRAINT fk_transport_day FOREIGN KEY (day_schedule_id)
        REFERENCES sub_trip_day_schedule(id)
        ON DELETE CASCADE
) COMMENT='子行程每日交通安排表';


-- 8. 景点表 attraction
CREATE TABLE attraction (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',

    trip_id BIGINT COMMENT '所属行程ID',
    sub_trip_id BIGINT COMMENT '所属子行程ID',

    name VARCHAR(255) NOT NULL COMMENT '景点名称',

    cover_image VARCHAR(500) COMMENT '景点封面图',

    category VARCHAR(100) COMMENT '景点分类',

    description TEXT COMMENT '景点简介',

    recommend_level VARCHAR(100) COMMENT '推荐程度',

    open_time VARCHAR(255) COMMENT '开放时间',

    duration VARCHAR(100) COMMENT '预计游玩时长',

    ticket_info VARCHAR(255) COMMENT '门票信息',

    travel_tips LONGTEXT COMMENT '游玩建议（富文本）',

    notice LONGTEXT COMMENT '注意事项（富文本）',

    note TEXT COMMENT '备注',

    sort_order INT DEFAULT 0 COMMENT '排序',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_attr_trip (trip_id),
    INDEX idx_attr_day (sub_trip_id),
    INDEX idx_attr_sort (sub_trip_id, sort_order),
    INDEX idx_attr_name (name)

) COMMENT='景点表';


-- 9. 餐饮表
CREATE TABLE food_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',

    trip_id BIGINT COMMENT '所属行程ID',
    sub_trip_id BIGINT COMMENT '所属子行程ID',

    name VARCHAR(255) NOT NULL COMMENT '餐厅名称',

    meal_type ENUM('早餐','午餐','晚餐','小吃饮品') 
        COMMENT '餐别',

    cuisine_type VARCHAR(100) 
        COMMENT '餐厅种类（中餐/日餐/法餐等）',

    recommend_level VARCHAR(50) 
        COMMENT '推荐等级（必吃/推荐/可选/不推荐等）',

    is_visited BOOLEAN DEFAULT FALSE 
        COMMENT '是否已吃',

    dishes TEXT 
        COMMENT '推荐菜品',

    price DECIMAL(10,2) 
        COMMENT '人均价格',

    address VARCHAR(500) 
        COMMENT '地址',

    open_time VARCHAR(255) 
        COMMENT '营业时间',

    image_1 VARCHAR(500) 
        COMMENT '餐厅图片1',

    image_2 VARCHAR(500) 
        COMMENT '餐厅图片2',

    image_3 VARCHAR(500) 
        COMMENT '餐厅图片3',

    note TEXT 
        COMMENT '备注',

    sort_order INT DEFAULT 0 
        COMMENT '排序',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
        COMMENT '创建时间',

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP 
        COMMENT '更新时间',

    INDEX idx_food_trip (trip_id),
    INDEX idx_food_day (sub_trip_id),
    INDEX idx_food_meal (meal_type),
    INDEX idx_food_recommend (recommend_level),
    INDEX idx_food_cuisine (cuisine_type),
    INDEX idx_food_sort (sub_trip_id, sort_order)

) COMMENT='餐饮表';

-- 10. 酒店表
CREATE TABLE hotel (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    trip_id BIGINT,
    sub_trip_id BIGINT,

    name VARCHAR(255) COMMENT '酒店名称',

    address VARCHAR(500),

    price DECIMAL(10,2),

    checkin_date DATE,
    checkout_date DATE,

    image VARCHAR(500),

    note TEXT,

    sort_order INT,

    INDEX idx_hotel_trip (trip_id),
    INDEX idx_hotel_day (sub_trip_id)

) COMMENT='酒店表';


-- 11. 交通表
CREATE TABLE transport (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',

    trip_id BIGINT COMMENT '所属行程ID',

    sub_trip_id BIGINT COMMENT '所属子行程ID',

    transport_type VARCHAR(50) 
        COMMENT '交通方式（飞机/高铁/地铁/公交/打车等）',

    train_no VARCHAR(100) 
        COMMENT '车次/班次（航班号/车次号等）',

    start_place VARCHAR(255) 
        COMMENT '起点',

    end_place VARCHAR(255) 
        COMMENT '终点',

    depart_time DATETIME 
        COMMENT '出发时间',

    arrive_time DATETIME 
        COMMENT '到达时间',

    duration VARCHAR(100) 
        COMMENT '时长',

    price DECIMAL(10,2) 
        COMMENT '票价',

    image_1 VARCHAR(500) 
        COMMENT '交通图片1',

    image_2 VARCHAR(500) 
        COMMENT '交通图片2',

    image_3 VARCHAR(500) 
        COMMENT '交通图片3',

    note TEXT 
        COMMENT '备注',

    sort_order INT DEFAULT 0 
        COMMENT '排序',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
        COMMENT '创建时间',

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP 
        COMMENT '更新时间',

    INDEX idx_transport_trip (trip_id),

    INDEX idx_transport_day (sub_trip_id),

    INDEX idx_transport_depart (depart_time),

    INDEX idx_transport_sort (sub_trip_id, sort_order)

) COMMENT='交通信息表';




-- 12. 预算表
CREATE TABLE budget_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    trip_id BIGINT NOT NULL COMMENT '所属攻略ID',
    sub_trip_id BIGINT COMMENT '所属子行程ID',
    category ENUM('交通','住宿','餐饮','门票','购物','其他') COMMENT '分类',
    title VARCHAR(255) COMMENT '项目名称',
    city VARCHAR(255) COMMENT '城市',
    amount DECIMAL(12,2) COMMENT '预算金额',
    date DATE COMMENT '预算日期',
    status ENUM('estimated','spent','cancelled') DEFAULT 'estimated' COMMENT '状态',
    notes TEXT COMMENT '备注',
    sort_order INT DEFAULT 0 COMMENT '排序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_budget_trip (trip_id),
    CONSTRAINT fk_budget_trip FOREIGN KEY (trip_id) REFERENCES trip_plan(id) ON DELETE CASCADE,
    CONSTRAINT fk_budget_day FOREIGN KEY (sub_trip_id) REFERENCES sub_trip(id) ON DELETE SET NULL
) COMMENT='预算表';


-- 13. 实际支出
CREATE TABLE expense_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    trip_id BIGINT NOT NULL COMMENT '所属攻略ID',
    sub_trip_id BIGINT COMMENT '所属子行程ID',
    budget_id BIGINT COMMENT '关联预算项ID',
    category ENUM('交通','住宿','餐饮','门票','购物','其他') COMMENT '分类',
    title VARCHAR(255) COMMENT '项目名称',
    city VARCHAR(255) COMMENT '城市',
    amount DECIMAL(12,2) COMMENT '实际花费',
    budget_amount DECIMAL(12,2) COMMENT '预算金额',
    paid_at DATE COMMENT '支付日期',
    payment_method VARCHAR(50) COMMENT '支付方式',
    notes TEXT COMMENT '备注',
    sort_order INT DEFAULT 0 COMMENT '排序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_expense_trip (trip_id),
    CONSTRAINT fk_expense_trip FOREIGN KEY (trip_id) REFERENCES trip_plan(id) ON DELETE CASCADE,
    CONSTRAINT fk_expense_day FOREIGN KEY (sub_trip_id) REFERENCES sub_trip(id) ON DELETE SET NULL,
    CONSTRAINT fk_expense_budget FOREIGN KEY (budget_id) REFERENCES budget_item(id) ON DELETE SET NULL
) COMMENT='实际开销表';


-- 14. 参考资料表
CREATE TABLE reference_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    
    trip_id BIGINT NOT NULL COMMENT '所属旅游攻略ID',
    sub_trip_id BIGINT COMMENT '所属子行程ID，可为空',

    title VARCHAR(255) NOT NULL COMMENT '参考资料名称/标题',
    type ENUM('攻略','美食','视频素材') DEFAULT '攻略' COMMENT '资料类型',
    url VARCHAR(1000) COMMENT '外部链接地址',
    thumbnail VARCHAR(500) COMMENT '缩略图',
    note TEXT COMMENT '备注或额外说明',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_reference_trip (trip_id),
    INDEX idx_reference_sub_trip (sub_trip_id),

    CONSTRAINT fk_reference_trip FOREIGN KEY (trip_id)
        REFERENCES trip_plan(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reference_sub_trip FOREIGN KEY (sub_trip_id)
        REFERENCES sub_trip(id)
        ON DELETE SET NULL
) COMMENT='旅游攻略参考资料表';

-- 15. 物品清单表
CREATE TABLE packing_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    
    trip_id BIGINT NOT NULL COMMENT '所属旅游攻略ID',
    
    name VARCHAR(255) NOT NULL COMMENT '物品名称',
    category VARCHAR(255) COMMENT '分类，例如：衣物/洗漱/电子/药品等',
    is_done BOOLEAN DEFAULT FALSE COMMENT '是否已勾选完成',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_packing_trip (trip_id),

    CONSTRAINT fk_packing_trip FOREIGN KEY (trip_id)
        REFERENCES trip_plan(id)
        ON DELETE CASCADE
) COMMENT='旅游物品打包清单表';

-- 16. 标准物品模板表
CREATE TABLE packing_template_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    
    name VARCHAR(255) NOT NULL COMMENT '物品名称',
    category VARCHAR(255) COMMENT '分类，例如：衣物/洗漱/电子/药品等',
    trip_type ENUM('国内游','出国游') NOT NULL DEFAULT '国内游' COMMENT '适用行程类型：国内游/出国游',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT='标准物品模板表，用于国内游或出国游的打包清单';

-- 17. 待办事项表
CREATE TABLE todo_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    
    trip_id BIGINT NOT NULL COMMENT '所属旅游攻略ID',
    
    title VARCHAR(255) NOT NULL COMMENT '待办标题',
    category VARCHAR(255) COMMENT '分类',
    action_date DATE COMMENT '计划执行日期',
    use_date DATE COMMENT '实际使用日期',
    status ENUM('未开始','进行中','已完成') DEFAULT '未开始' COMMENT '待办状态',
    note TEXT COMMENT '备注或渠道信息',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_todo_trip (trip_id),

    CONSTRAINT fk_todo_trip FOREIGN KEY (trip_id)
        REFERENCES trip_plan(id)
        ON DELETE CASCADE
) COMMENT='旅行待办事项表';

-- 18. 游记表
CREATE TABLE travel_note (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    
    trip_id BIGINT NOT NULL COMMENT '所属旅游攻略ID',
    sub_trip_id BIGINT COMMENT '所属子行程ID，可为空',
    
    date DATE COMMENT '游记日期',
    content TEXT COMMENT '游记内容，富文本',
    images JSON COMMENT '图片数组，存储上传的图片路径或URL',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_travel_note_trip (trip_id),
    INDEX idx_travel_note_sub_trip (sub_trip_id),

    CONSTRAINT fk_travel_note_trip FOREIGN KEY (trip_id)
        REFERENCES trip_plan(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_travel_note_sub_trip FOREIGN KEY (sub_trip_id)
        REFERENCES sub_trip(id)
        ON DELETE SET NULL
) COMMENT='旅行游记表';

-- 19. 评估回顾表
CREATE TABLE review_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    
    trip_id BIGINT NOT NULL COMMENT '所属旅游攻略ID',
    
    satisfaction_score TINYINT COMMENT '满意度评分，1-5分',
    highlights TEXT COMMENT '行程亮点',
    issues TEXT COMMENT '行程问题',
    over_budget_reason TEXT COMMENT '超预算原因',
    next_optimization TEXT COMMENT '下次优化建议',
    recommendation TEXT COMMENT '值得推荐与不推荐项',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_review_trip (trip_id),

    CONSTRAINT fk_review_trip FOREIGN KEY (trip_id)
        REFERENCES trip_plan(id)
        ON DELETE CASCADE
) COMMENT='旅行评估与回顾表';

-- 20. 旅游需求表
CREATE TABLE requirement_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    
    trip_id BIGINT NOT NULL UNIQUE COMMENT '所属旅游攻略ID（1:1关系）',
    
    purpose TEXT COMMENT '出行目的',
    num_people INT COMMENT '人数',
    date_range VARCHAR(50) COMMENT '时间范围',
    budget_limit DECIMAL(10,2) COMMENT '预算上限',
    style_preference TEXT COMMENT '偏好风格',
    transport_preference TEXT COMMENT '交通偏好',
    hotel_preference TEXT COMMENT '酒店偏好',
    food_preference TEXT COMMENT '饮食偏好',
    avoid_items TEXT COMMENT '需要避开的事项',
    other_requirements TEXT COMMENT '其他要求',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    CONSTRAINT fk_requirement_trip FOREIGN KEY (trip_id)
        REFERENCES trip_plan(id)
        ON DELETE CASCADE
) COMMENT='旅游需求表';

-- 21. 用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希值',
    role VARCHAR(20) DEFAULT 'user' COMMENT '用户角色：user/admin',
    status TINYINT DEFAULT 1 COMMENT '状态：0=禁用,1=正常',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT='用户表';