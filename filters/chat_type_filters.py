from aiogram import types
from aiogram.filters import BaseFilter
from loader import bot

class IsGroup(BaseFilter):
    async def __call__(self, message: types.Message):
        return message.chat.type in (
            'group',
            'supergroup'
        )


class GroupMembers(BaseFilter):
    async def __call__(self, message: types.Message) ->bool:
        user = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        return user.status.MEMBER
