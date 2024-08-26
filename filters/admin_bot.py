from aiogram.filters import BaseFilter
from data.config import ADMINS
from aiogram import types


class IsBotAdmin():
    def __call__(self, message: types.Message):
        return str(message.from_user.id) in ADMINS
