from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def show_lessons(schedule_entries, mode):
    keyboard = InlineKeyboardBuilder()
    for id, entry in schedule_entries:
        keyboard.row(InlineKeyboardButton(
        text=entry, 
        callback_data=f"show_lesson_{mode}_{id}")
        )
    return keyboard.as_markup()

