from pydantic import BaseModel
from typing import List, Optional

class UserLogin(BaseModel):
    username: str
    password: str

# схема для создания брони (входящие данные)- user_id не передается, а берется из токена
class CreateBooking(BaseModel):
    room_id: int
    slot_id: int
    date: str

# схема для ответа с бронированием
class BookingResponse(BaseModel):
    id: int
    room_id: int
    date: str
    user_id: int
    slot_id: int

# схема для списка комнат
class RoomResponse(BaseModel):
    id: str
    name: str

#схема для одного слота в расписании
class AvailabilitySlotResponse(BaseModel):
    slot_id: int
    time: str    # "09:00-11:00"
    is_available: bool
    booked_by: Optional[str] # показывается только админу

# схема для одной комнаты в расписании
class RoomAvailability(BaseModel):
    room_id: int
    room_name: str
    slots: List[AvailabilitySlotResponse]

# схема для полного расписания на дату
class AvailabilityResponse(BaseModel):
    date: str
    rooms: List[RoomAvailability]