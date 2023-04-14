from configs import config
from aiogram.filters import BaseFilter
from aiogram.types import Message, Chat


class AdminFilter(BaseFilter):
    def __init__(self, chat_type):
        self.chat_type = chat_type

    async def __call__(self, message: Message):
        user = message.from_user
        chat = Chat(id=config.chat_id, type=self.chat_type)
        chat_member = await chat.get_member(user.id)
        
        if chat_member.status not in ('administrator', 'creator'):
            await message.answer("💂‍♂️💂‍♂️💂‍♂️ Ви не є адміністратором чи власником групи 💂‍♂️💂‍♂️💂‍♂️")
        
        return chat_member.status in ('administrator', 'creator')