from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class BookingPerson(Base):
    __tablename__ = "booking_persons"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    gothram = Column(String, nullable=False)
    rasi = Column(String, nullable=False)
    nakshatra = Column(String, nullable=False)

    booking = relationship("Booking", back_populates="persons")
