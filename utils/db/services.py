import json
from typing import List, Optional

from sqlalchemy import select, func, and_, or_

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
                    select(Request).filter(Request.id == request_id))
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
                    select(Request).filter(Request.user == user).filter(Request.active == True))
                requests = result.scalars().all()
        return requests

    @staticmethod
    async def get_random_request(user: User) -> Optional[Request]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Request).filter(and_(Request.user != user, Request.active == True)).order_by(func.random()))
                request = result.scalars().first()
            return request

    @staticmethod
    async def create_meeting_from_request(request_id: int, user_id: int) -> int:
        async with async_session() as session:
            async with session.begin():
                user = await DbCommands.get_user(user_id=user_id)
                result = await session.execute(select(Request).filter(Request.id == request_id))
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
                result = await session.execute(select(Meeting).filter(Meeting.id == meeting_id))
                return result.scalars().first()

    @staticmethod
    async def get_meetings_by_user(user: User) -> List[Meeting]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Meeting).filter(or_(Meeting.request_user_id == user.id, Meeting.second_user_id == user.id)))
                meetings = result.scalars().all()
        return meetings

online
сегодня
Артемий
Артемий 20:25

    Или это можно без скрипта?

Сергей
Сергей 20:28

    Это можем с сервера делать

Артемий
Артемий 20:40

    Но тогда не будет такого представления в таблицах?

Сергей
Сергей 20:41

    Представление исходных данных перенесём в бд, а производные таблицы оставим в гугл
    Ну или можем реально попробовать собрать и таблицы на сервере и оттуда если надо выгружать типа как срм

Артемий
Артемий 20:47

    Это решит проблему?

Сергей
Сергей 20:49

    Сергей Наталенко
    Представление исходных данных перенесём в бд, а производные таблицы оставим в гугл
    Да, но скрипты на питоне надо будет переписать все

Артемий
Артемий 20:49

    Можно будет новичку поручить

Сергей
Сергей 20:57

    Предлагаю пойти немного дальше и сделать свой сервис для удобной выгрузки данных гк по запросу для остальных приложений

Артемий
Артемий 20:57

    А имеет ли это смысл учитывая уход с геткурса?

Сергей
Сергей 20:58

    То есть один сервис обращается к гк и все из него выкачивает в две таблицы - пользователей и заказов. Потом когда надо к этому сервису обращается ерп или текущий сервер в виде нормального запроса с параметрами и мы их вертим потом как хотим в остальных приложениях

Сергей
Сергей 20:59

    Артемий Пыстогов
    А имеет ли это смысл учитывая уход с геткурса?
    Да, потому что когда мы с него уйдём например на платформу или срм, то перепишем код только этого одного сервиса, который по сути будет выступать прослойкой

Сергей
Сергей 21:04

    В перспективе одной единой платформы это не целесообразно да, а в контексте уже трех различных сервисов стоит подумать

Артемий
Артемий 21:06

    Насколько сложно такое сделать?

Сергей
Сергей 21:07

    Все зависит только от того насколько сложные ответы такой сервис должен отдавать
    Если начать просто с выгрузки n-пользователей и заказов по id геткурса, то за день-два можно поднять такой

сегодня
Сергей
Сергей 1:43

    Нужен совет: в нашем задании вылезло осложнение, которое было не очевидно при постановке ТЗ и строго говоря его полное решение находится за рамками описанными в ТЗ и оговоренными при собеседовании.

    Вопрос: что делать с кандидатами?

    Тот, который работал на другой работе с доп отсрочкой пропал, второй, который первый прислал решение, сделал задание процентов на 40-50%, третий задавал сегодня очень много вопросов, видно, что пытается разобраться, но прям совсем местами тупит. У них еще есть время до крайнего срока, и, надеюсь, еще что-то пришлют вменяемое посмотреть, но пока расклад такой. Про второе задание даже еще не спрашивал, но, подозреваю, что никто даже не пробовал

Артемий
Артемий 7:44

    Ты же сказал что кто то первое сделал?

Артемий
Артемий 9:48

    Первому надо написать
    Третьему надо помочь обязательно

Артемий
Артемий 10:09

    Пересланные сообщения
    Ещё чуть-чуть — и соточка! | Академия А
    Ещё чуть-чуть — и соточка! | Академия А 27 мар в 10:59
        Привет! К сожалению, у тебя закончился оплаченный период доступа к курсу :(

        Если ты вернешься в течение 24 часов после отчисления, стоимость останется прежней и все материалы сохранятся :)

        Если у тебя возникли вопросы, пиши сюда https://vk.me/ege_soch

        Надеемся на твоё возвращение!
    Ещё чуть-чуть — и соточка! | Академия А
    Ещё чуть-чуть — и соточка! | Академия А сегодня в 10:04
        Привет, Zarina!

        К сожалению, у тебя все еще выполнено менее 30% обязательных тестовых заданий курса, поэтому мы вынуждены выдать тебе первое предупреждение.
        Если в следующем месяце ты получишь второе предупреждение за неуспеваемость, то не сможешь продлить доступ к курсу и продолжить заниматься :(

        Твоя успеваемость – 0%
    Должна быть проверка на отчислен человек или нет

Сергей
Сергей 10:11

    Артемий Пыстогов
    Ты же сказал что кто то первое сделал?
    Сделал я его проверил, а там выполнение на половину где-то, потому что проблемы появились

Сергей
Сергей 10:12

    Артемий Пыстогов
    Должна быть проверка на отчислен человек или нет
    Она есть, но почему-то эта девочка не отчислена на сервере

Артемий
Артемий 10:13

    Сергей Наталенко
    Сделал я его проверил, а там выполнение на половину где-то, потому что проблемы появились
    А ты ему написал

Артемий
Артемий 10:13

    Сергей Наталенко
    Она есть, но почему-то эта девочка не отчислена на сервере
    Что нужно сделать?

Сергей
Сергей 10:14

    Артемий Пыстогов
    Что нужно сделать?
    Уже ничего, я отчислил вручную сейчас

Артемий
Артемий 10:14

    Ок

Сергей
Сергей 10:14

    Артемий Пыстогов
    А ты ему написал
    Да, он пообещал доделать

Артемий
Артемий 11:34

    Ты знаешь как импортировать заказы и пользователей в геткурс?

Сергей
Сергей 11:36

    да, у них в апи описано
    обновление данных пользователя, которое мы уже используем, это по сути импорт, если имейл не найден

Артемий
Артемий 11:37

    Хорошо, просто надо будет внести пользователей с геткурсов партнеров

Сергей
Сергей 11:39

    получается, что новые предметы будут на отдельных геткурс аккаунтах, а мы их у себя будем собирать просто?

Артемий
Артемий 11:39

    Нет
    Всё будет у нас
    Просто когда будем начинать надо будет перенести

Сергей
Сергей 11:40

    а разве они не появятся сами при регистрации?

Артемий
Артемий 11:40

    Нужна база с котороц можно работать
    И история заказов для подсчета ltv

Сергей
Сергей 11:42

    по идее нам нужны тогда их предложения все

Артемий
Артемий 11:43

    А их разве можно импортировать?

Сергей
Сергей 11:43

    и тогда реально база раздуется капец как если их пользователей и заказы за все время начнем переносить

Сергей
Сергей 11:43

    Артемий Пыстогов
    А их разв