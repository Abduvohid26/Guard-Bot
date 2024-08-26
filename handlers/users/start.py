from aiogram.filters import CommandStart
from loader import dp, db, bot
from aiogram import types, html
from filters.guard_filter import MyFilter
from filters.chat_type_filters import IsGroup
from filters.private_chat import IsPrivate
from filters.group_members import GroupMembers
from keyboards.inline.buttons import group_add


@dp.message(CommandStart(), IsPrivate())
async def start_bot(message:types.Message):
    current_user = message.from_user.id
    try:
        if db.select_user(id=current_user):

            await message.answer(
                f"Salom 👋  "
                f" {html.link(link=f'http://t.me/{message.from_user.username}', value=f'{message.from_user.full_name}')} ! \n\n"
                f"Men silkalarni va linklarni guruhdan o'chririb beraman\n"
                f"Guruhga 3 martdan kop link yuborgan odamni ketiga tepaman",
            reply_markup=group_add(), disable_web_page_preview=True)
        else:
            db.add_user(id=current_user, fullname=message.from_user.full_name, telegram_id=current_user,
                        language=message.from_user.language_code)
            await message.answer(
                f"Assalomu alaykum {html.link(link=f'http://t.me/{message.from_user.username}', value=f'{message.from_user.full_name}')}!",
            reply_markup=group_add(), disable_web_page_preview=True)
    except Exception as e:
        print(e)

@dp.message(CommandStart(), IsGroup())
async def start_bot(message:types.Message):
    current_user = message.from_user.id
    try:
        if db.select_user(id=current_user):

            await message.answer(
                f"Salom 👋  "
                f" {html.link(link=f'http://t.me/{message.from_user.username}', value=f'{message.from_user.full_name}')} ! \n\n"
                f"Bizning guruhga xush kelibsiz\n",
            reply_markup=group_add(), disable_web_page_preview=True)
        else:
            db.add_user(id=current_user, fullname=message.from_user.full_name, telegram_id=current_user,
                        language=message.from_user.language_code)
            await message.answer(
                f"Salom 👋  "
                f" {html.link(link=f'http://t.me/{message.from_user.username}', value=f'{message.from_user.full_name}')} ! \n\n"
                f"Bizning guruhga xush kelibsiz\n",
                reply_markup=group_add(), disable_web_page_preview=True)
    except Exception as e:
        print(e)


@dp.message(MyFilter(my_text=['@', 'https', 'http', 'www']),GroupMembers(), IsGroup())
async def check(message: types.Message):
    current_user = message.from_user.id
    try:
        if db.select_user(id=current_user):
            db.illegal_add(telegram_id=current_user)
            data = db.select_user(id=current_user)[-1]
        else:
            db.add_user(id=current_user, fullname=message.from_user.full_name, telegram_id=current_user,
                        language=message.from_user.language_code)
            data = db.select_user(id=current_user)[-1]
            db.illegal_add(telegram_id=current_user)

    except Exception as e:
        print(e)
    finally:
        if data >= 3:
            await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            db.update_illegal_zero(telegram_id=current_user)
        else:
            pass
        links = html.link(
            value=f'{message.from_user.first_name if message.from_user.first_name else message.from_user.last_name}',
            link=f'http://t.me/{message.from_user.username}'
        )
        await message.delete()
        await message.answer(
            f'❗️ {links}  '
            f'{html.bold(value="Iltimos reklama yubormang")}\n' 
            f'Sizda ogolantirishlar soni {data} ta {" ".join(["❌"] * data)}\n'  
            f' Ogoxlantirishlar soni 5 ta ga yetganda guruhdan spam olasiz 👟',
            reply_markup=group_add(), disable_web_page_preview=True
        )


@dp.edited_message(MyFilter(my_text=['@', 'https', 'http', 'www']), GroupMembers(), IsGroup())
async def check_edit(message: types.Message):
    current_user = message.from_user.id
    try:
        if db.select_user(id=current_user):
            db.illegal_add(telegram_id=current_user)
            data = db.select_user(id=current_user)[-1]
        else:
            db.add_user(id=current_user, fullname=message.from_user.full_name, telegram_id=current_user,
                        language=message.from_user.language_code)
            data = db.select_user(id=current_user)[-1]
            db.illegal_add(telegram_id=current_user)

    except Exception as e:
        print(e)
    finally:
        if data >= 3:
            await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            db.update_illegal_zero(telegram_id=current_user)
        else:
            pass
        links = html.link(
            value=f'{message.from_user.first_name if message.from_user.first_name else message.from_user.last_name}',
            link=f'http://t.me/{message.from_user.username}'
        )
        await message.delete()
        await message.answer(
            f'❗️ {links}  '
            f'{html.bold(value="Iltimos reklama yubormang")}\n'
            f'Sizda ogolantirishlar soni {data} ta {" ".join(["❌"] * data)}\n'
            f' Ogoxlantirishlar soni 5 ta ga yetganda guruhdan spam olasiz 👟',
            reply_markup=group_add(), disable_web_page_preview=True
        )
