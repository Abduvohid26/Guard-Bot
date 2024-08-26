from aiogram.filters import BaseFilter
from aiogram import types
from loader import bot


class IsGroupAdmin(BaseFilter):
    async def __call__(self, message: types.Message):
        user = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        return user.status.ADMINISTRATOR or user.status.CREATOR



