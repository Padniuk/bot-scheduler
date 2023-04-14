from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy import select, and_, insert, update, delete as delete_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from filters import AdminFilter, ChatTypeFilter
from databases import LessonOrder, Lesson
from keyboards import show_lessons
from .states import LessonStates, OrderStates


router = Router()

@router.message(Command("add"), ~ChatTypeFilter(chat_type=["group", "supergroup"]), AdminFilter(chat_type="group"))
async def schedule(message: Message, state: FSMContext):
    await state.set_state(LessonStates.name)
    await state.update_data(command="add")
    await message.answer("Назва предмету:")


@router.message(Command("update"), ~ChatTypeFilter(chat_type=["group", "supergroup"]), AdminFilter(chat_type="group"))
async def schedule(message: Message, session: AsyncSession):
    sql = select(Lesson, LessonOrder).join(Lesson)

    schedule_request = await session.execute(sql)
    schedule = schedule_request.scalars()

    schedule_entries = [(lesson.id, f'{lesson.name}') for lesson in schedule]
        
    text = "Оберіть предмет для виправлення:"
    await message.answer(text,reply_markup=show_lessons(schedule_entries,"update"))


@router.callback_query(Text(startswith="show_lesson_update"))
async def lesson_update(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    sql = select(Lesson, LessonOrder).join(Lesson).where(Lesson.id == int(callback.data.split('_')[3]))

    schedule_request = await session.execute(sql)
    schedule = schedule_request.scalars()

    for lesson in schedule:
        schedule_entries_text = f'Назва: `{lesson.name}`\n' \
                                f'Викладач: `{lesson.teacher}`\n' \
                                f'Посилання: `{lesson.link}`\n' \
                                f'День: `{lesson.day}`\n' \
                                f'Порядок: `{lesson.order.id}`'
        await callback.message.answer(schedule_entries_text, parse_mode='Markdown')
        await state.set_state(LessonStates.name)
        await state.update_data(command="update")
        await callback.message.answer("Назва предмету:")


@router.message(LessonStates.name, F.text)
async def name(message: Message, state: FSMContext): 
    await state.update_data(name=message.text)
    await message.answer("Викладач:")
    await state.set_state(LessonStates.teacher)


@router.message(LessonStates.teacher, F.text)
async def teacher(message: Message, state: FSMContext): 
    await state.update_data(teacher=message.text)
    await message.answer("Посилання:")
    await state.set_state(LessonStates.link)


@router.message(LessonStates.link, F.text)
async def link(message: Message, state: FSMContext): 
    await state.update_data(link=message.text)
    await message.answer("День:")
    await state.set_state(LessonStates.day)


@router.message(LessonStates.day, F.text)
async def day(message: Message, state: FSMContext): 
    await state.update_data(day=message.text)
    await message.answer("Порядок:")
    await state.set_state(LessonStates.order)


@router.message(LessonStates.order, F.text)
async def order(message: Message, state: FSMContext, session: AsyncSession): 
    print(LessonStates.command)
    await state.update_data(order=int(message.text))
    data = await state.get_data()
    await state.clear()


    if data['command'] == "update":
        await message.answer("Дякую за відповіді. Інформація оновлена")    
        stmt_upadate = update(Lesson).where(Lesson.name==data['name']). \
            values(name=data['name'],teacher=data['teacher'],day=data['day'],link=data['link'],order_id=data['order'])
        await session.execute(stmt_upadate)
    
    if data['command'] == "add":    
        await message.answer("Дякую за відповіді. Інформація додана")
        stml_add = insert(Lesson).values(name=data['name'],
                        teacher=data['teacher'],
                        link=data['link'],
                        day=data['day'],
                        order_id=data['order'])
        await session.execute(stml_add)
    
    await session.commit()


@router.message(Command("delete"), ~ChatTypeFilter(chat_type=["group", "supergroup"]), AdminFilter(chat_type="group"))
async def delete(message: Message, session: AsyncSession):
    sql = select(Lesson, LessonOrder).join(Lesson)

    schedule_request = await session.execute(sql)
    schedule = schedule_request.scalars()

    schedule_entries = [(lesson.id, f'{lesson.name}') for lesson in schedule]
        
    text = "Оберіть предмет для видалення:"
    await message.answer(text,reply_markup=show_lessons(schedule_entries,"delete"))


@router.callback_query(Text(startswith="show_lesson_delete"))
async def lesson_delete(callback: CallbackQuery, session: AsyncSession):
    stmt = delete_(Lesson).where(Lesson.id == int(callback.data.split('_')[3]))
    await session.execute(stmt)
    await session.commit()
    await callback.message.answer("Предмет видалено")


@router.message(Command("clear"), ~ChatTypeFilter(chat_type=["group", "supergroup"]), AdminFilter(chat_type="group"))
async def clear(message: Message, session: AsyncSession):
    stmt = delete_(Lesson)
    await session.execute(stmt)
    await session.commit()
    await message.answer("Список предметів тепер порожній")


@router.message(Command("change"), ~ChatTypeFilter(chat_type=["group", "supergroup"]), AdminFilter(chat_type="group"))
async def change(message: Message, state: FSMContext, session: AsyncSession):
    sql = select(LessonOrder)

    schedule_request = await session.execute(sql)
    schedule = schedule_request.scalars()

    schedule_entries = [f'{lesson.id}.`{lesson.start_time.strftime("%H:%M")}-' \
                        f'{lesson.end_time.strftime("%H:%M")}`' for lesson in schedule]

    schedule_entries_text = "\n".join(schedule_entries)
    await message.answer(schedule_entries_text, parse_mode='Markdown')
    
    await state.set_state(OrderStates.first)
    await message.answer("Перше заняття:")

@router.message(OrderStates.first, F.text)
async def first_lesson(message: Message, state: FSMContext): 
    await state.update_data(first=message.text)
    await message.answer("Друге заняття:")
    await state.set_state(OrderStates.second)

@router.message(OrderStates.second, F.text)
async def second_lesson(message: Message, state: FSMContext): 
    await state.update_data(second=message.text)
    await message.answer("Третє заняття:")
    await state.set_state(OrderStates.third)

@router.message(OrderStates.third, F.text)
async def third_lesson(message: Message, state: FSMContext): 
    await state.update_data(third=message.text)
    await message.answer("Четверте заняття:")
    await state.set_state(OrderStates.fourth)
    
@router.message(OrderStates.fourth, F.text)
async def fourth_lesson(message: Message, state: FSMContext, session: AsyncSession): 
    await state.update_data(fourth=message.text)
    data = await state.get_data()
    await state.clear()

    for lesson_order, time_interval in enumerate(data):
        stmt = update(LessonOrder).where(LessonOrder.id==lesson_order+1). \
            values(start_time=datetime.strptime(data[time_interval][0:-6], '%H:%M'), \
                end_time=datetime.strptime(data[time_interval][-5:], '%H:%M'))
        await session.execute(stmt)
    
    await session.commit()