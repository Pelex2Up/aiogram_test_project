from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, VARCHAR, Integer, Boolean, Text, ForeignKey, CHAR, BigInteger, SmallInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UsersBooking(Base):
    __tablename__: str = "users_booking"

    id = Column(Integer, primary_key=True)
    f_name = Column(Text, nullable=True)
    l_name = Column(Text, nullable=True)
    date = Column(TIMESTAMP, nullable=False)
    time = Column(Text, nullable=True)
    num_of_people = Column(Text, nullable=True)