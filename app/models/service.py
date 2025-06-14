from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.booking_services import booking_services

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    live_video_url = Column(String, nullable=True)
    recorded_video_url = Column(String, nullable=True)
    temple_id = Column(Integer, ForeignKey("temples.id", ondelete="CASCADE"), nullable=False)

    bookings = relationship("Booking", secondary=booking_services, back_populates="services")
