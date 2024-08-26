from aiogram.utils.keyboard import InlineKeyboardBuilder

def group_add():
    btn = InlineKeyboardBuilder()
    btn.button(text='♻️ Guruhga qo\'shish', url='https://t.me/super_guard_robot?startgroup=true')
    btn.adjust(1)
    return btn.as_markup()

