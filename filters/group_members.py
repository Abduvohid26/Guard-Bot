from aiogram import types
from loader import bot
from aiogram.filters import BaseFilter


class GroupMembers(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        try:
            user = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            return user.status == 'member'
        except Exception as e:
            print(f"Error in GroupMembers filter: {e}")
            return False
