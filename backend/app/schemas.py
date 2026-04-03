from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Literal, Any
from decimal import Decimal
from datetime import datetime, date
from enum import Enum

# --- Attraction (景点) 字段完全对应 models.py ---

class AttractionBase(BaseModel):
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    name: str
    cover_image: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    recommend_level: Optional[str] = None
    open_time: Optional[str] = None
    duration: Optional[str] = None
    ticket_info: Optional[str] = None
    travel_tips: Optional[str] = None
    notice: Optional[str] = None
    note: Optional[str] = None
    sort_order: Optional[int] = 0

class AttractionCreate(AttractionBase):
    pass

class AttractionUpdate(BaseModel):
    # 所有字段设为可选，用于 PUT/PATCH 更新
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    name: Optional[str] = None
    cover_image: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    recommend_level: Optional[str] = None
    open_time: Optional[str] = None
    duration: Optional[str] = None
    ticket_info: Optional[str] = None
    travel_tips: Optional[str] = None
    notice: Optional[str] = None
    note: Optional[str] = None
    sort_order: Optional[int] = None

class AttractionResponse(AttractionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- BudgetItem (预算) ---
class BudgetItemBase(BaseModel):
    trip_id: int
    sub_trip_id: Optional[int] = None
    category: Optional[Literal['交通','住宿','餐饮','门票','购物','其他']] = None
    title: Optional[str] = None # 模型中是 title，不是 item_name
    city: Optional[str] = None
    amount: Optional[Decimal] = None
    date: Optional[date] = None
    status: Optional[Literal['estimated','spent','cancelled']] = 'estimated'
    notes: Optional[str] = None # 模型中是 notes，带 s
    sort_order: Optional[int] = 0

class BudgetItemCreate(BudgetItemBase):
    pass

class BudgetItemUpdate(BaseModel):
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    category: Optional[Literal['交通','住宿','餐饮','门票','购物','其他']] = None
    title: Optional[str] = None
    city: Optional[str] = None
    amount: Optional[Decimal] = None
    date: Optional[date] = None
    status: Optional[Literal['estimated','spent','cancelled']] = None
    notes: Optional[str] = None
    sort_order: Optional[int] = None

class BudgetItemResponse(BudgetItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- ExpenseItem (实际支出) ---

class ExpenseItemBase(BaseModel):
    trip_id: int
    sub_trip_id: Optional[int] = None
    budget_id: Optional[int] = None
    category: Optional[Literal['交通', '住宿', '餐饮', '门票', '购物', '其他']] = None
    title: Optional[str] = None
    city: Optional[str] = None
    amount: Optional[Decimal] = None
    budget_amount: Optional[Decimal] = None
    paid_at: Optional[date] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None  # 对应 models.py 中的 notes (复数)
    sort_order: Optional[int] = 0

class ExpenseItemCreate(ExpenseItemBase):
    """创建支出记录时使用"""
    pass

class ExpenseItemUpdate(BaseModel):
    """更新支出记录时使用（所有字段可选）"""
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    budget_id: Optional[int] = None
    category: Optional[Literal['交通', '住宿', '餐饮', '门票', '购物', '其他']] = None
    title: Optional[str] = None
    city: Optional[str] = None
    amount: Optional[Decimal] = None
    budget_amount: Optional[Decimal] = None
    paid_at: Optional[date] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None
    sort_order: Optional[int] = None

class ExpenseItemResponse(ExpenseItemBase):
    """返回给前端的数据模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- FoodItem (严格对照您提供的最新模型) ---

class FoodItemBase(BaseModel):
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    name: str
    # Enum('早餐','午餐','晚餐','小吃饮品')
    meal_type: Optional[Literal['早餐', '午餐', '晚餐', '小吃饮品']] = None
    cuisine_type: Optional[str] = None
    recommend_level: Optional[str] = None
    is_visited: Optional[bool] = False
    dishes: Optional[str] = None
    price: Optional[float] = None
    address: Optional[str] = None
    open_time: Optional[str] = None
    image_1: Optional[str] = None
    image_2: Optional[str] = None
    image_3: Optional[str] = None
    note: Optional[str] = None
    sort_order: Optional[int] = 0

class FoodItemCreate(FoodItemBase):
    """创建记录时使用"""
    pass

class FoodItemUpdate(BaseModel):
    """更新记录时使用，所有字段可选"""
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    name: Optional[str] = None
    meal_type: Optional[Literal['早餐', '午餐', '晚餐', '小吃饮品']] = None
    cuisine_type: Optional[str] = None
    recommend_level: Optional[str] = None
    is_visited: Optional[bool] = None
    dishes: Optional[str] = None
    price: Optional[float] = None
    address: Optional[str] = None
    open_time: Optional[str] = None
    image_1: Optional[str] = None
    image_2: Optional[str] = None
    image_3: Optional[str] = None
    note: Optional[str] = None
    sort_order: Optional[int] = None

class FoodItemResponse(FoodItemBase):
    """返回数据时使用"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Hotel (住宿表) ---

class HotelBase(BaseModel):
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    price: Optional[float] = None
    checkin_date: Optional[date] = None
    checkout_date: Optional[date] = None
    image: Optional[str] = None
    note: Optional[str] = None
    sort_order: Optional[int] = None

class HotelCreate(HotelBase):
    pass

class HotelUpdate(HotelBase):
    pass

class HotelResponse(HotelBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- PackingItem (物品清单表) ---

class PackingItemBase(BaseModel):
    trip_id: int  # 模型中 nullable=False
    name: Optional[str] = None
    category: Optional[str] = None
    is_done: Optional[bool] = False

class PackingItemCreate(PackingItemBase):
    pass

class PackingItemUpdate(BaseModel):
    trip_id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    is_done: Optional[bool] = None

class PackingItemResponse(PackingItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- PackingTemplateItem (标准物品模板) ---

class PackingTemplateItemBase(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    trip_type: Optional[Literal['国内游', '出国游']] = '国内游'

class PackingTemplateItemCreate(PackingTemplateItemBase):
    pass

class PackingTemplateItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    trip_type: Optional[Literal['国内游', '出国游']] = None

class PackingTemplateItemResponse(PackingTemplateItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- ReferenceItem (参考资料) ---

class ReferenceItemBase(BaseModel):
    trip_id: int
    sub_trip_id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[Literal['攻略', '美食', '视频素材']] = '攻略'
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    note: Optional[str] = None

class ReferenceItemCreate(ReferenceItemBase):
    pass

class ReferenceItemUpdate(BaseModel):
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[Literal['攻略', '美食', '视频素材']] = None
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    note: Optional[str] = None

class ReferenceItemResponse(ReferenceItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- RequirementItem (旅游需求) ---

class RequirementItemBase(BaseModel):
    trip_id: Optional[int] = None
    purpose: Optional[str] = None
    num_people: Optional[int] = None
    date_range: Optional[str] = None
    budget_limit: Optional[Decimal] = None
    style_preference: Optional[str] = None
    transport_preference: Optional[str] = None
    hotel_preference: Optional[str] = None
    food_preference: Optional[str] = None
    avoid_items: Optional[str] = None
    other_requirements: Optional[str] = None

class RequirementItemCreate(RequirementItemBase):
    pass

class RequirementItemUpdate(RequirementItemBase):
    pass

class RequirementItemResponse(RequirementItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- 通用枚举 ---
class MealType(str, Enum):
    breakfast = "早餐"
    lunch = "午餐"
    dinner = "晚餐"
    snack = "小吃"
    drink = "饮品"

# --- 19. 评估回顾表 (ReviewItem) ---
class ReviewItemBase(BaseModel):
    trip_id: int
    satisfaction_score: Optional[int] = None
    highlights: Optional[str] = None
    issues: Optional[str] = None
    over_budget_reason: Optional[str] = None
    next_optimization: Optional[str] = None
    recommendation: Optional[str] = None

class ReviewItemCreate(ReviewItemBase):
    pass

class ReviewItemUpdate(BaseModel):
    satisfaction_score: Optional[int] = None
    highlights: Optional[str] = None
    issues: Optional[str] = None
    over_budget_reason: Optional[str] = None
    next_optimization: Optional[str] = None
    recommendation: Optional[str] = None

class ReviewItem(ReviewItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- 6. 餐饮表 (SubTripDayMeal) ---
class SubTripDayMealBase(BaseModel):
    day_schedule_id: int
    meal_type: Optional[MealType] = None
    restaurant_name: Optional[str] = None
    note: Optional[str] = None

class SubTripDayMealCreate(SubTripDayMealBase):
    pass

class SubTripDayMealUpdate(BaseModel):
    meal_type: Optional[MealType] = None
    restaurant_name: Optional[str] = None
    note: Optional[str] = None

class SubTripDayMeal(SubTripDayMealBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- 4. 子行程每日安排表 (SubTripDaySchedule) ---
class SubTripDayScheduleBase(BaseModel):
    sub_trip_id: int
    date: date
    summary: Optional[str] = None

class SubTripDayScheduleCreate(SubTripDayScheduleBase):
    pass

class SubTripDayScheduleUpdate(BaseModel):
    date: Optional[date] = None
    summary: Optional[str] = None

class SubTripDaySchedule(SubTripDayScheduleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- 3. 子行程表 (SubTrip) ---
class SubTripBase(BaseModel):
    trip_id: int
    title: Optional[str] = None
    card_cover_image: Optional[str] = None
    hero_image: Optional[str] = None
    map_image_1: Optional[str] = None
    map_image_2: Optional[str] = None
    map_image_3: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    city: Optional[str] = None
    summary: Optional[str] = None
    sort_order: int = 0

class SubTripCreate(SubTripBase):
    pass

class SubTripUpdate(BaseModel):
    title: Optional[str] = None
    card_cover_image: Optional[str] = None
    hero_image: Optional[str] = None
    map_image_1: Optional[str] = None
    map_image_2: Optional[str] = None
    map_image_3: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    city: Optional[str] = None
    summary: Optional[str] = None
    sort_order: Optional[int] = None

class SubTrip(SubTripBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- 通用基础类 ---
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# --- 5. 时间轴表 (SubTripDayTimeline) ---
class TimelineBase(BaseModel):
    day_schedule_id: int
    time_range: Optional[str] = None
    place_name: Optional[str] = None
    place_url: Optional[str] = None
    note: Optional[str] = None

class TimelineCreate(TimelineBase):
    pass

class TimelineUpdate(BaseModel):
    time_range: Optional[str] = None
    place_name: Optional[str] = None
    place_url: Optional[str] = None
    note: Optional[str] = None

class Timeline(TimelineBase):
    id: int
    created_at: datetime
    updated_at: datetime

# --- 7. 子行程每日交通表 (SubTripDayTransport) ---
class DayTransportBase(BaseModel):
    day_schedule_id: int
    start_location: Optional[str] = None
    transport_mode: Optional[str] = None
    cost: Optional[float] = None
    note: Optional[str] = None

class DayTransportCreate(DayTransportBase):
    pass

class DayTransportUpdate(BaseModel):
    start_location: Optional[str] = None
    transport_mode: Optional[str] = None
    cost: Optional[float] = None
    note: Optional[str] = None

class DayTransport(DayTransportBase):
    id: int
    created_at: datetime
    updated_at: datetime

# --- 11. 交通表 (Transport) ---
class TransportBase(BaseModel):
    trip_id: Optional[int] = None
    sub_trip_id: Optional[int] = None
    transport_type: Optional[str] = None
    train_no: Optional[str] = None
    start_place: Optional[str] = None
    end_place: Optional[str] = None
    depart_time: Optional[datetime] = None
    arrive_time: Optional[datetime] = None
    duration: Optional[str] = None
    price: Optional[float] = None
    image_1: Optional[str] = None
    image_2: Optional[str] = None
    image_3: Optional[str] = None
    note: Optional[str] = None
    sort_order: int = 0

class TransportCreate(TransportBase):
    pass

class TransportUpdate(BaseModel):
    transport_type: Optional[str] = None
    train_no: Optional[str] = None
    start_place: Optional[str] = None
    end_place: Optional[str] = None
    depart_time: Optional[datetime] = None
    arrive_time: Optional[datetime] = None
    duration: Optional[str] = None
    price: Optional[float] = None
    image_1: Optional[str] = None
    image_2: Optional[str] = None
    image_3: Optional[str] = None
    note: Optional[str] = None
    sort_order: Optional[int] = None

class TransportRead(TransportBase):
    id: int

# --- 17. 待办事项表 (TodoItem) ---
class TodoStatus(str, Enum):
    not_started = "未开始"
    in_progress = "进行中"
    finished = "已完成"

class TodoBase(BaseModel):
    trip_id: int
    title: Optional[str] = None
    category: Optional[str] = None
    action_date: Optional[date] = None
    use_date: Optional[date] = None
    status: TodoStatus = TodoStatus.not_started
    note: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    action_date: Optional[date] = None
    use_date: Optional[date] = None
    status: Optional[TodoStatus] = None
    note: Optional[str] = None

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime


# 定义行程状态枚举
class TripStatus(str, Enum):
    planned = "planned"
    finished = "finished"

# --- TravelNote (游记) ---
class TravelNoteBase(BaseModel):
    trip_id: int
    sub_trip_id: Optional[int] = None
    date: Optional[date] = None
    content: Optional[str] = None
    images: Optional[Any] = None  # 对应 JSON 字段

class TravelNoteCreate(TravelNoteBase):
    pass

class TravelNoteUpdate(BaseModel):
    sub_trip_id: Optional[int] = None
    date: Optional[date] = None
    content: Optional[str] = None
    images: Optional[Any] = None

class TravelNote(TravelNoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- TripOverview (行程总览) ---
class TripOverviewBase(BaseModel):
    trip_id: int
    day_number: Optional[int] = None
    date: Optional[date] = None
    city: Optional[str] = None
    transport: Optional[str] = None
    attractions: Optional[str] = None
    food: Optional[str] = None
    note: Optional[str] = None
    sort_order: Optional[int] = None

class TripOverviewCreate(TripOverviewBase):
    pass

class TripOverviewUpdate(BaseModel):
    day_number: Optional[int] = None
    date: Optional[date] = None
    city: Optional[str] = None
    transport: Optional[str] = None
    attractions: Optional[str] = None
    food: Optional[str] = None
    note: Optional[str] = None
    sort_order: Optional[int] = None

class TripOverview(TripOverviewBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- TripPlan (旅游攻略主表) ---
class TripPlanBase(BaseModel):
    title: str
    card_cover_image: Optional[str] = None
    hero_image: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: TripStatus = TripStatus.planned
    summary: Optional[str] = None
    highlights: Optional[str] = None
    route_map_image: Optional[str] = None

class TripPlanCreate(TripPlanBase):
    pass

class TripPlanUpdate(BaseModel):
    title: Optional[str] = None
    card_cover_image: Optional[str] = None
    hero_image: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[TripStatus] = None
    summary: Optional[str] = None
    highlights: Optional[str] = None
    route_map_image: Optional[str] = None

class TripPlan(TripPlanBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- User (用户) ---
class UserBase(BaseModel):
    username: str
    role: Optional[str] = "user"
    status: Optional[int] = 1

class UserCreate(UserBase):
    password_hash: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None
    status: Optional[int] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)