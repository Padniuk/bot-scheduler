from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from databases import Lesson, LessonOrder
from middlewares import WeekendMessageMiddleware

router = Router()
router.message.middleware(WeekendMessageMiddleware())

@router.message(Command("start"))
async def schedule(message: Message):
    text = "Usage:\n" \
            "/start - describes all commands\n" \
            "/schedule - gives schedule for current day"
    await message.answer(text)

@router.message(Command("schedule"))
async def schedule(message: Message, session: AsyncSession):
    now = datetime.now()
    current_day = now.strftime("%A")[:3]
    
    sql = select(Lesson, LessonOrder).join(LessonOrder).where(Lesson.day == current_day).order_by(LessonOrder.start_time)
    schedule_request = await session.execute(sql)
    schedule = schedule_request.scalars()

    schedule_entries = [f'{lesson.order.id}. <b>{lesson.name}</b>\n'
                        f'<i>{lesson.teacher}</i>\n'
                        f'{lesson.order.start_time.strftime("%H:%M")}-{lesson.order.end_time.strftime("%H:%M")}\n'
                        f'🔗 {lesson.link}' for lesson in schedule]
        
    schedule_entries_text ="\n\n".join(schedule_entries)
    try:
        await message.answer(schedule_entries_text, parse_mode='HTML')
    except TelegramBadRequest:
        await message.answer("💃💃💃 Cьогодні нема занять 💃💃💃", parse_mode='HTML')
