from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from authx import AuthX, AuthXConfig
#from database import users_db, slots_db, bookings_db, next_booking_id
from schemas import UserLogin, RoomResponse, AvailabilityResponse, RoomAvailability, AvailabilitySlotResponse, CreateBooking, BookingResponse
from datetime import datetime, date
from database import engine
from models import User, Room, Slot, Booking
from database import get_db
from sqlalchemy.orm import Session



app = FastAPI(title="Meeting Room Booking")


config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_TOKEN_LOCATION = ['headers']
config.JWT_HEADER_NAME = 'Authorization'
config.JWT_ACCESS_TOKEN_EXPIRES = None


security = AuthX(config=config)
security_scheme = HTTPBearer()


@app.post("/login")
def login(credentials: UserLogin,  db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    # проверка пароля
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # создание токена
    token = security.create_access_token(
        uid=user.username, # user .sub
        data={"role": user.role}
    )
    return {"access_token": token}


@app.get("/rooms")
def read_rooms(db: Session = Depends(get_db), user = Depends(security.access_token_required)):
    rooms = db.query(Room).all()
    return rooms


@app.get("/availability")
def read_availability(date: str, user=Depends(security.access_token_required), db: Session = Depends(get_db)):
    rooms_list = []

    rooms_from_db = db.query(Room).all()
     #поиск комнаты
    for room in rooms_from_db:
        slots_list = []
        slots_from_db = db.query(Slot).filter(Slot.room_id == room.id).all()
        #поиск слотов в комнате
        for slot in slots_from_db:
            booking_exists = db.query(Booking).filter(
                Booking.room_id == room.id,
                Booking.slot_id == slot.id,
                Booking.date == date
            ).first()

            slot_time = f"{slot.start_time}-{slot.end_time}"
            #доступность слота и комнаты
            slot_response = AvailabilitySlotResponse(
                slot_id=slot.id,
                time=slot_time,
                is_available=booking_exists is None,
                booked_by=str(booking_exists.user_id) if booking_exists and user.role == "admin"
                else None #смотреть может только админ
            )
            slots_list.append(slot_response)

        room_availability = RoomAvailability(
            room_id=room.id,
            room_name=room.name,
            slots=slots_list
        )
        rooms_list.append(room_availability)

    return AvailabilityResponse(date=date, rooms=rooms_list)


@app.post("/bookings")
def create_booking(booking: CreateBooking, user=Depends(security.access_token_required), db: Session = Depends(get_db)):
    #получаем пользователя из токена
    username = user.sub
    user_from_db = db.query(User).filter(User.username == username).first()
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    #проверка существования комнаты
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    #проверка существования слота
    slot = db.query(Slot).filter(Slot.id == booking.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    if slot.room_id != room.id:
        raise HTTPException(status_code=404, detail="Slot doesn't belong to this room")

    #проверяем что даат не в прошлом
    booking_date = datetime.strptime(booking.date, "%Y-%m-%d").date()
    today = date.today()
    if booking_date < today:
        raise HTTPException(status_code=400, detail="Can't book past dates")

    #проверка что слот еще не забровнирован
    existing_booking = db.query(Booking).filter(
        Booking.room_id == room.id,
        Booking.slot_id == slot.id,
        Booking.date == booking.date
    ).first()
    if existing_booking:
        raise HTTPException(status_code=409, detail="Slot already booked")

    #новое бронирование
    new_booking = Booking(
        room_id=room.id,
        slot_id=slot.id,
        date=booking.date,
        user_id=user_from_db.id
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    #ответ
    return BookingResponse(
        id=new_booking.id,
        room_id=new_booking.room_id,
        date=new_booking.date,
        slot_id=new_booking.slot_id,
        user_id=new_booking.user_id
    )


@app.get("/bookings")
def get_my_bookings(user=Depends(security.access_token_required), db: Session = Depends(get_db)):
    # получаем пользователя из токена
    username = user.sub
    user_from_db = db.query(User).filter(User.username == username).first()
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    #проверка ролей
    if user_from_db.role == "admin":
        return db.query(Booking).all()

    if user_from_db.role == "employee":
        return db.query(Booking).filter(Booking.user_id == user_from_db.id).all()


@app.delete("/bookings/{id}")
def delete_booking(id: int, user=Depends(security.access_token_required), db: Session = Depends(get_db)):
    #получаем текущего пользователя из токена
    username = user.sub
    user_from_db = db.query(User).filter(User.username == username).first()

    # проверяем существует ли пользователь в бд
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    # поиск бронирования по id
    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    #права доступа (админ может удалить любое бронирование, employee только свое)
    if user_from_db.role != "admin" and booking.user_id != user_from_db.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this booking")

    # проверяем дату бронирования (нельзя отменить уже прошедшее бронирование)
    booking_date = datetime.strptime(booking.date, "%Y-%m-%d").date()
    if booking_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot cancel past booking")

    # Удаляем запись из бд
    db.delete(booking)
    db.commit()

    return {"message": "Booking deleted"}