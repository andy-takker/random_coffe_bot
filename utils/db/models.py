import json

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, BigInteger, sql
from sqlalchemy.orm import declarative_base, relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255))
    phone_number = Column(String(255))
    is_registration_completed = Column(Boolean, default=False)

    position_id = Column(Integer, ForeignKey('position.id'), index=True)
    position = relationship('Position', backref='user_position', foreign_keys=[position_id])

    workplace_id = Column(Integer, ForeignKey('workplace.id'), index=True)
    workplace = relationship('Workplace', backref='user_workplace', foreign_keys=[workplace_id])

    query: sql.Select

    def __repr__(self):
        return f'<User {self.id}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'


class Position(Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    query: sql.select


class Workplace(Base):
    __tablename__ = 'workplace'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    city = Column(String(255))
    query: sql.select


class Meeting(Base):
    __tablename__ = 'meeting'
    id = Column(Integer, primary_key=True)

    request_user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    second_user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)

    date = Column(DateTime(timezone=True), default=False)
    place = Column(String(255))
    location = Column(String(255))
    purpose = Column(String(255), nullable=False)
    request_id = Column(Integer, ForeignKey('request.id'), index=True, nullable=False)
    is_successful = Column(Boolean, default=False)

    query: sql.select

    request = relationship('Request', backref='meeting_request', foreign_keys=[request_id])
    request_user = relationship('User', backref='meeting_request_user', foreign_keys=[request_user_id])
    second_user = relationship('User', backref='meeting_second_user', foreign_keys=[second_user_id])

    @property
    def to_msg(self):
        place = f"Место: {self.place}\n" if self.place is not None else ""
        return f"Дата и время: {self.date.strftime('%d.%m.%Y %H:%M')}\n" \
               f"Инициатор: {self.request_user.name} @{self.request_user.username}\n" \
               f"Приглашенный: {self.second_user.name} @{self.second_user.username}\n{place}" \
               f"Цель: {self.purpose}\n"

    def get_location(self):
        return json.loads(self.location)


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    date = Column(DateTime(timezone=True), default=False)
    place = Column(String(255))
    location = Column(String(255))
    purpose = Column(String(255), nullable=False)
    comment = Column(String(255))
    active = Column(Boolean, default=True)

    query: sql.select

    user = relationship('User', backref='request_user', foreign_keys=[user_id])

    def __repr__(self):
        return f'<Request {self.id}>'

    def __str__(self):
        return f'<Request {self.id}>'

    @property
    def to_msg(self):
        place = f"Место: {self.place}\n" if self.place is not None else ""
        return f"Дата и время: {self.date.strftime('%d.%m.%Y %H:%M')}\nИнициатор: {self.user.name}\n{place}" \
               f"Цель: {self.purpose}\n" \
               f"Комментарий: {self.comment}"

    def get_location(self):
        return json.loads(self.location)
