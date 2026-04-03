from sqlalchemy import Column, String, Integer, BigInteger, Float, Text, Date, DateTime, Boolean, Enum, JSON, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime # 必须确保有这一行
from sqlalchemy import JSON

Base = declarative_base()

# 1. 旅游攻略主表
class TripPlan(Base):
    __tablename__ = "trip_plan"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    card_cover_image = Column(String(500))
    hero_image = Column(String(500))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum('planned','finished', name='trip_status'), default='planned')
    summary = Column(Text)
    highlights = Column(Text)
    route_map_image = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sub_trips = relationship("SubTrip", back_populates="trip", cascade="all, delete-orphan")
    overviews = relationship("TripOverview", back_populates="trip", cascade="all, delete-orphan")
    budget_items = relationship("BudgetItem", back_populates="trip", cascade="all, delete-orphan")
    expense_items = relationship("ExpenseItem", back_populates="trip", cascade="all, delete-orphan")
    references = relationship("ReferenceItem", back_populates="trip", cascade="all, delete-orphan")
    packing_items = relationship("PackingItem", back_populates="trip", cascade="all, delete-orphan")
    todos = relationship("TodoItem", back_populates="trip", cascade="all, delete-orphan")
    travel_notes = relationship("TravelNote", back_populates="trip", cascade="all, delete-orphan")
    reviews = relationship("ReviewItem", back_populates="trip", cascade="all, delete-orphan")
    requirement = relationship("RequirementItem", back_populates="trip", uselist=False, cascade="all, delete-orphan")

# 2. 行程总览表
class TripOverview(Base):
    __tablename__ = "trip_overview"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    day_number = Column(Integer)
    date = Column(Date)
    city = Column(String(255))
    transport = Column(String(255))
    attractions = Column(Text)
    food = Column(Text)
    note = Column(Text)
    sort_order = Column(Integer)

    trip = relationship("TripPlan", back_populates="overviews")

# 3. 子行程表
class SubTrip(Base):
    __tablename__ = "sub_trip"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    title = Column(String(255))
    card_cover_image = Column(String(500))
    hero_image = Column(String(500))
    map_image_1 = Column(String(500))
    map_image_2 = Column(String(500))
    map_image_3 = Column(String(500))
    start_date = Column(Date)
    end_date = Column(Date)
    city = Column(String(255))
    summary = Column(Text)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="sub_trips")
    day_schedules = relationship("SubTripDaySchedule", back_populates="sub_trip", cascade="all, delete-orphan")
    attractions = relationship("Attraction", back_populates="sub_trip", cascade="all, delete-orphan")
    foods = relationship("FoodItem", back_populates="sub_trip", cascade="all, delete-orphan")
    hotels = relationship("Hotel", back_populates="sub_trip", cascade="all, delete-orphan")
    transports = relationship("Transport", back_populates="sub_trip", cascade="all, delete-orphan")
    budget_items = relationship("BudgetItem", back_populates="sub_trip", cascade="all, delete-orphan")
    expense_items = relationship("ExpenseItem", back_populates="sub_trip", cascade="all, delete-orphan")
    references = relationship("ReferenceItem", back_populates="sub_trip", cascade="all, delete-orphan")
    travel_notes = relationship("TravelNote", back_populates="sub_trip", cascade="all, delete-orphan")

# 4. 子行程每日安排表
class SubTripDaySchedule(Base):
    __tablename__ = "sub_trip_day_schedule"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"), nullable=False)
    date = Column(Date, nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sub_trip = relationship("SubTrip", back_populates="day_schedules")
    timelines = relationship("SubTripDayTimeline", back_populates="day_schedule", cascade="all, delete-orphan")
    meals = relationship("SubTripDayMeal", back_populates="day_schedule", cascade="all, delete-orphan")
    transports = relationship("SubTripDayTransport", back_populates="day_schedule", cascade="all, delete-orphan")

# 5. 时间轴表
class SubTripDayTimeline(Base):
    __tablename__ = "sub_trip_day_timeline"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    day_schedule_id = Column(BigInteger, ForeignKey("sub_trip_day_schedule.id"), nullable=False)
    time_range = Column(String(50))
    place_name = Column(String(255))
    place_url = Column(String(500))
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    day_schedule = relationship("SubTripDaySchedule", back_populates="timelines")

# 6. 餐饮表
class SubTripDayMeal(Base):
    __tablename__ = "sub_trip_day_meal"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    day_schedule_id = Column(BigInteger, ForeignKey("sub_trip_day_schedule.id"), nullable=False)
    meal_type = Column(Enum('早餐','午餐','晚餐','小吃','饮品', name='meal_type'))
    restaurant_name = Column(String(255))
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    day_schedule = relationship("SubTripDaySchedule", back_populates="meals")

# 7. 子行程每日交通表
class SubTripDayTransport(Base):
    __tablename__ = "sub_trip_day_transport"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    day_schedule_id = Column(BigInteger, ForeignKey("sub_trip_day_schedule.id"), nullable=False)
    start_location = Column(String(255))
    transport_mode = Column(String(50))
    cost = Column(Float)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    day_schedule = relationship("SubTripDaySchedule", back_populates="transports")

# 8. 景点表
class Attraction(Base):
    __tablename__ = "attraction"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"))
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"))
    name = Column(String(255), nullable=False)
    cover_image = Column(String(500))
    category = Column(String(100))
    description = Column(Text)
    recommend_level = Column(String(100))
    open_time = Column(String(255))
    duration = Column(String(100))
    ticket_info = Column(String(255))
    travel_tips = Column(Text)
    notice = Column(Text)
    note = Column(Text)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sub_trip = relationship("SubTrip", back_populates="attractions")

# 9. 餐饮表
class FoodItem(Base):
    __tablename__ = "food_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"))
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"))
    name = Column(String(255), nullable=False)
    meal_type = Column(Enum('早餐','午餐','晚餐','小吃饮品', name='food_meal_type'))
    cuisine_type = Column(String(100))
    recommend_level = Column(String(50))
    is_visited = Column(Boolean, default=False)
    dishes = Column(Text)
    price = Column(Float)
    address = Column(String(500))
    open_time = Column(String(255))
    image_1 = Column(String(500))
    image_2 = Column(String(500))
    image_3 = Column(String(500))
    note = Column(Text)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sub_trip = relationship("SubTrip", back_populates="foods")

# 10. 住宿表
class Hotel(Base):
    __tablename__ = "hotel"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"))
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"))
    name = Column(String(255))
    address = Column(String(500))
    price = Column(Float)
    checkin_date = Column(Date)
    checkout_date = Column(Date)
    image = Column(String(500))
    note = Column(Text)
    sort_order = Column(Integer)

    sub_trip = relationship("SubTrip", back_populates="hotels")

# 11. 交通表
class Transport(Base):
    __tablename__ = "transport"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"))
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"))
    transport_type = Column(String(50))
    train_no = Column(String(100))
    start_place = Column(String(255))
    end_place = Column(String(255))
    depart_time = Column(DateTime)
    arrive_time = Column(DateTime)
    duration = Column(String(100))
    price = Column(Float)
    image_1 = Column(String(500))
    image_2 = Column(String(500))
    image_3 = Column(String(500))
    note = Column(Text)
    sort_order = Column(Integer, default=0)

    sub_trip = relationship("SubTrip", back_populates="transports")

# 12. 预算表
class BudgetItem(Base):
    __tablename__ = "budget_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"), nullable=True)
    category = Column(Enum('交通','住宿','餐饮','门票','购物','其他', name='budget_category'))
    title = Column(String(255))
    city = Column(String(255))
    amount = Column(DECIMAL(12,2))
    date = Column(Date)
    status = Column(Enum('estimated','spent','cancelled', name='budget_status'), default='estimated')
    notes = Column(Text)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="budget_items")
    sub_trip = relationship("SubTrip", back_populates="budget_items")
    expenses = relationship("ExpenseItem", back_populates="budget")

# 13. 实际支出
class ExpenseItem(Base):
    __tablename__ = "expense_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"), nullable=True)
    budget_id = Column(BigInteger, ForeignKey("budget_item.id"), nullable=True)
    category = Column(Enum('交通','住宿','餐饮','门票','购物','其他', name='expense_category'))
    title = Column(String(255))
    city = Column(String(255))
    amount = Column(DECIMAL(12,2))
    budget_amount = Column(DECIMAL(12,2))
    paid_at = Column(Date)
    payment_method = Column(String(50))
    notes = Column(Text)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="expense_items")
    sub_trip = relationship("SubTrip", back_populates="expense_items")
    budget = relationship("BudgetItem", back_populates="expenses")

# 14. 参考资料表
class ReferenceItem(Base):
    __tablename__ = "reference_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"), nullable=True)
    title = Column(String(255))
    type = Column(Enum('攻略','美食','视频素材', name='reference_type'), default='攻略')
    url = Column(String(1000))
    thumbnail = Column(String(500))
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="references")
    sub_trip = relationship("SubTrip", back_populates="references")

# 15. 物品清单表
class PackingItem(Base):
    __tablename__ = "packing_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    name = Column(String(255))
    category = Column(String(255))
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="packing_items")

# 16. 标准物品模板表
class PackingTemplateItem(Base):
    __tablename__ = "packing_template_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    category = Column(String(255))
    trip_type = Column(Enum('国内游','出国游', name='packing_trip_type'), default='国内游')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 17. 待办事项表
class TodoItem(Base):
    __tablename__ = "todo_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    title = Column(String(255))
    category = Column(String(255))
    action_date = Column(Date)
    use_date = Column(Date)
    status = Column(Enum('未开始','进行中','已完成', name='todo_status'), default='未开始')
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="todos")

# 18. 游记表
class TravelNote(Base):
    __tablename__ = "travel_note"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    sub_trip_id = Column(BigInteger, ForeignKey("sub_trip.id"), nullable=True)
    date = Column(Date)
    content = Column(Text)
    images = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="travel_notes")
    sub_trip = relationship("SubTrip", back_populates="travel_notes")

# 19. 评估回顾表
class ReviewItem(Base):
    __tablename__ = "review_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), nullable=False)
    satisfaction_score = Column(Integer)
    highlights = Column(Text)
    issues = Column(Text)
    over_budget_reason = Column(Text)
    next_optimization = Column(Text)
    recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="reviews")

# 20. 旅游需求表
class RequirementItem(Base):
    __tablename__ = "requirement_item"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey("trip_plan.id"), unique=True)
    purpose = Column(Text)
    num_people = Column(Integer)
    date_range = Column(String(50))
    budget_limit = Column(DECIMAL(10,2))
    style_preference = Column(Text)
    transport_preference = Column(Text)
    hotel_preference = Column(Text)
    food_preference = Column(Text)
    avoid_items = Column(Text)
    other_requirements = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("TripPlan", back_populates="requirement")

# 21. 用户表
class User(Base):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user')
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)