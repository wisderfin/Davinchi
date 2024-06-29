from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, func, BIGINT

from app.base.model import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(BIGINT, primary_key=True)
    name = Column(String, nullable=False)
    privilege = Column(Boolean, nullable=False, default=False)
    description = Column(String, nullable=True)
    gender = Column(Boolean, nullable=False)  # True = man
    age = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    photos = Column(String, nullable=False)
    rate = Column(Float, nullable=False, default=5.0)
    account = Column(String, unique=True, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    banned = Column(Boolean, nullable=False, default=False)
    create_at = Column(DateTime, nullable=False, default=func.now())
