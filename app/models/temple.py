from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base
from sqlalchemy.orm import relationship

class Temple(Base):
    __tablename__ = "temples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    image_url = Column(String, nullable=True)  # Store image as URL
    about = Column(Text, nullable=True)
    history = Column(Text, nullable=True)
    attraction = Column(Text, nullable=True)
    significance = Column(Text, nullable=True)

    bookings = relationship("Booking", back_populates="temple")