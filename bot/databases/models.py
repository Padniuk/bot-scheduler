from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from databases import Base
from sqlalchemy.orm import relationship


class LessonOrder(Base):
    __tablename__ = 'lessons_order'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    teacher = Column(String)
    day = Column(String)

    order_id = Column(Integer, ForeignKey('lessons_order.id'))
    order = relationship('LessonOrder')