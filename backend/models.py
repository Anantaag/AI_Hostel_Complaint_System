from sqlalchemy import Column, Integer, String
from backend.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    complaint = Column(String)
    category = Column(String)
    priority = Column(String)