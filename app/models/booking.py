from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.booking_services import booking_services
from enum import Enum as PyEnum

class BookingStatusEnum(PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "FAILED"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    temple_id = Column(Integer, ForeignKey("temples.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    total_price = Column(Integer, nullable=False)
    video_type = Column(String, nullable=False)
    status = Column(Enum(BookingStatusEnum), default=BookingStatusEnum.PENDING)
    payment_id = Column(String, nullable=True)

    temple = relationship("Temple", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
    services = relationship("Service", secondary=booking_services, back_populates="bookings")
    persons = relationship("BookingPerson", back_populates="booking")
