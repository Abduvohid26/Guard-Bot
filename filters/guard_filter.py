from aiogram.filters import Filter
from aiogram import types
from loader import bot
class MyFilter(Filter):
    def __init__(self, my_text: list):
        self.urls = my_text
    async def __call__(self, message: types.Message) ->bool:
        for i in self.urls:
            if i in message.text:
                return True
            if message.entities:
                for entities in message.entities:
                    if entities.type in ['text_link', 'url']:
                        return True
            else:
                return False

