import json
import logging
from typing import List, Optional

from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from utils.db import async_session
from utils.db.models import User, Position, Workplace, Request, Meeting


class DbCommands:
    @staticmethod
    async def create_user(user_id: int, first_name: str, last_name: str, username: str, ) -> User:
        async with async_session() as session:
            async with session.begin():
                user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username)
                session.add(user)
            await session.commit()
            return user

    @staticmethod
    async def get_user(user_id: int) -> User:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(User).filter(User.user_id == user_id))
                return result.scalars().first()

    @staticmethod
    async def get_request(request_id: int) -> Request:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Request).options(selectinload(Request.user)).filter(Request.id == request_id))
                return result.scalars().first()

    @staticmethod
    async def update_user(user_id: int, data: dict):
        async with async_session() as session:
            result = await session.execute(select(User).filter(User.user_id == user_id))
            user = result.scalars().first()
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.position_id = data['position_id']
            user.workplace_id = data['workplace_id']
            user.is_registration_completed = True
            await session.commit()

    @staticmethod
    async def create_position(name: str) -> Position:
        async with async_session() as session:
            async with session.begin():
                position = Position(name=name)
                session.add(position)
            await session.commit()
            return position

    @staticmethod
    async def get_position(name: str) -> Position:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Position).filter(Position.name == name))
                return result.scalars().first()

    @staticmethod
    async def create_workplace(name: str) -> Workplace:
        async with async_session() as session:
            async with session.begin():
                workplace = Workplace(name=name)
                session.add(workplace)
            await session.commit()
            return workplace

    @staticmethod
    async def get_workplace(name: str) -> Workplace:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Workplace).filter(Workplace.name == name))
                return result.scalars().first()

    @staticmethod
    async def create_request(user_id: int, data: dict) -> Request:
        async with async_session() as session:
            async with session.begin():
                user = await DbCommands.get_user(user_id=user_id)
                request = Request(
                    user=user,
                    date=data['date'],
                    place=data['place'],
                    purpose=data['purpose'],
                    comment=data['comment'],
                    location=json.dumps(data['location']) if data['location'] is not None else None,
                )
                session.add(request)
            await session.commit()
            return request

    @staticmethod
    async def get_requests_by_user(user: User) -> List[Request]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Request).options(selectinload(Request.user)).filter(Request.user == user).filter(Request.active == True))
                requests = result.scalars().all()
                # str_requests = []
                # for req in requests:
                #     str_requests.append(req.to_msg)
        return requests

    @staticmethod
    async def get_random_request(user: User) -> Optional[Request]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Request).options(selectinload(Request.user)).filter(
                        and_(Request.user != user, Request.active == True)).order_by(
                        func.random()))
                request = result.scalars().first()
            return request

    @staticmethod
    async def create_meeting_from_request(request_id: int, user_id: int) -> int:
        async with async_session() as session:
            async with session.begin():
                user = await DbCommands.get_user(user_id=user_id)
                result = await session.execute(
                    select(Request).options(selectinload(Request.user)).filter(Request.id == request_id))
                request = result.scalars().first()
                meeting = Meeting(
                    request_user_id=request.user_id,
                    second_user_id=user.id,
                    date=request.date,
                    request_id=request.id,
                    place=request.place,
                    location=request.location,
                    purpose=request.purpose,
                )
                request.active = False
                session.add(meeting)
            await session.commit()
            return meeting.id

    @staticmethod
    async def get_meeting(meeting_id: int) -> Meeting:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Meeting).options(selectinload(Meeting.second_user)).options(
                        selectinload(Meeting.request_user)).filter(Meeting.id == meeting_id))
                return result.scalars().first()

    @staticmethod
    async def get_meetings_by_user(user: User) -> List[Meeting]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Meeting).options(selectinload(Meeting.second_user)).options(
                        selectinload(Meeting.request_user)).filter(
                        or_(Meeting.request_user_id == user.id, Meeting.second_user_id == user.id)))
                meetings = result.scalars().all()
                # str_meetings = []
                # for meet in meetings:
                #     str_meetings.append(meet.to_msg)
        return meetings
