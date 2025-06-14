from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.database import Base

booking_services = Table(
    'booking_services',
    Base.metadata,
    Column('booking_id', Integer, ForeignKey('bookings.id', ondelete="CASCADE"), primary_key=True),
    Column('service_id', Integer, ForeignKey('services.id', ondelete="CASCADE"), primary_key=True)
)
