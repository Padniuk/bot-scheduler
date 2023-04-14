from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
from filters import ChatTypeFilter, AdminFilter
from databases import LessonOrder, Lesson
from middlewares import WeekendMessageMiddleware

router = Router()
router.message.middleware(WeekendMessageMiddleware())
scheduler = AsyncIOScheduler(timezone='Europe/Kiev')


@router.message(Command("on"), ChatTypeFilter(chat_type=["group", "supergroup"]), AdminFilter(chat_type="group"))
async def start_schedule(message: Message, session: AsyncSession):
    if not scheduler.running:
        sql = select(LessonOrder).order_by(LessonOrder.start_time)
        schedule_request = await session.execute(sql)
        schedule = schedule_request.scalars()
        for lesson in schedule:
            send_time = lesson.start_time - timedelta(minutes=5)
            scheduler.add_job(lesson_form,'cron', hour=send_time.hour, minute=send_time.minute, \
                kwargs={'lesson_id': lesson.id, 'session': session, 'message': message})
        scheduler.start()
    else:
        await message.answer("🔥🔥🔥 Сповіщення уже ввімкнені 🔥🔥🔥")

async def lesson_form(lesson_id, session: AsyncSession, message):
    now = datetime.now()
    current_day = now.strftime("%A")[:3]

    sql = select(Lesson, LessonOrder).join(Lesson).where(and_(Lesson.day == current_day, \
        LessonOrder.id == lesson_id))
    schedule_request = await session.execute(sql)
    schedule = schedule_request.scalars()

    for lesson in schedule:
        schedule_entries_text = f'{lesson.order.id}. <b>{lesson.name}</b>\n' \
                        f'<i>{lesson.teacher}</i>\n' \
                        f'{lesson.order.start_time.strftime("%H:%M")}-{lesson.order.end_time.strftime("%H:%M")}\n' \
                        f'🔗 {lesson.link}'

        await message.answer(schedule_entries_text, parse_mode='HTML')


@router.message(Command("off"), ChatTypeFilter(chat_type=["group", "supergroup"]), AdminFilter(chat_type="group"))
async def stop_schedule(message: Message):
    if scheduler.running:
        scheduler.shutdown()
    else:
        await message.answer("🛑🛑🛑 Сповіщення уже є вимненими 🛑🛑🛑")
