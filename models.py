from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


# Таблица пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)  #уникальный логин
    password = Column(String)
    role = Column(String) # admin / employee


# Таблица переговорной комнаты
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String)


# Таблица временного слота
class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True)
    start_time = Column(String)   # "09:00"
    end_time = Column(String)    # "11:00"
    room_id = Column(Integer, ForeignKey("rooms.id"))


# Таблица бронирования
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    slot_id = Column(Integer, ForeignKey("slots.id"))
    date = Column(String)      # "2026-06-10"
    user_id = Column(Integer, ForeignKey("users.id"))
