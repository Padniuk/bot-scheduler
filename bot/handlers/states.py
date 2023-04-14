from aiogram.fsm.state import StatesGroup, State

class LessonStates(StatesGroup):
    command = State()
    name = State()
    teacher = State()
    link = State()
    day = State()
    order = State()

class OrderStates(StatesGroup):
    first = State()
    second = State()
    third = State()
    fourth = State()    