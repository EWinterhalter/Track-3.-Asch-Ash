#Main
import Config
import Text
import Func
import Keyboards

import asyncio
from aiogram import Bot, types, Dispatcher, F, Router
from aiogram.types import ContentType, Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os

bot = Bot(token=Config.tokenp)
dp = Dispatcher()
router = Router()

class AdminActions(StatesGroup):
    add_admin = State()
    del_admin = State()
    add_chat = State()
    del_chat = State()
    pass_word = State()
    
@dp.message(Command('start'), F.content_type == ContentType.TEXT)
async def start(message: types.Message, state: FSMContext):
    if os.path.exists('ashash.db') == False:
        await message.answer(
            Text.password_text,
            reply_markup=Keyboards.undo
        )
        await state.set_state(AdminActions.pass_word)
    if os.path.exists('ashash.db') == True:
        if message.from_user.username in await Func.getAdm() and message.chat.id not in await Func.getCht():
            await message.answer(Text.start_text, reply_markup=Keyboards.all_btn)
        elif message.from_user.username in await Func.getAdm() or message.chat.id in await Func.getCht():
            await message.answer(Text.start_chat, reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(Text.private_chat, reply_markup=ReplyKeyboardRemove())

@dp.message(AdminActions.pass_word)
async def check_pass(message: Message, state: FSMContext):
    await Func.askpass(message)
    await state.clear()
    return await start(message, state)
    
@dp.message(Command('show_admins'))
async def show_adm(message: types.Message):
    if message.from_user.username in await Func.getAdm():
        admins = await Func.ShowAdmins()
        await message.reply(
            str(admins)
        )
        
@dp.message(Command('show_chats'))
async def show_cht(message: types.Message):
    if message.from_user.username in await Func.getAdm():
        chats = await Func.ShowChats()
        await message.reply(
            str(chats)
        )

@dp.message(Command("add_admin"), F.content_type == ContentType.TEXT)
async def cmd_add_admin(message: Message, state: FSMContext):
    if message.from_user.username in await Func.getAdm():
        await message.answer(
            Text.username_text,
            reply_markup=Keyboards.undo
        )
        await state.set_state(AdminActions.add_admin)

@dp.message(AdminActions.add_admin, F.content_type == ContentType.TEXT)
async def link_add_admin(message: Message, state: FSMContext):
    admin_name = message.text.replace('@','')
    if message.text == '/Undo':
        await message.answer(Text.undo_text)
        await state.clear()
        return await start(message, state)
    await message.answer(Text.adminadd_text, reply_markup=Keyboards.all_btn) if await Func.insertAdmins(admin_name) else await message.answer("Такой админ уже есть", reply_markup=Keyboards.all_btn)
    await state.clear()

@dp.message(Command("add_chat"), F.content_type == ContentType.TEXT)
async def cmd_add_cht(message: Message, state: FSMContext):
    if message.from_user.username in await Func.getAdm():
        await message.answer(
            Text.chatid_text,
            reply_markup=Keyboards.undo
        )
        await state.set_state(AdminActions.add_chat)

@dp.message(AdminActions.add_chat, F.content_type == ContentType.TEXT)
async def link_add_chat(message: Message, state: FSMContext):
    if message.text == '/Undo':
        await message.answer(Text.undo_text)
        await state.clear()
        return await start(message, state)
    await message.answer(Text.chatadd_text, reply_markup=Keyboards.all_btn) if await Func.insertChat(message.text) else await message.answer("Такой чат уже есть", reply_markup=Keyboards.all_btn)
    await state.clear()

@dp.message(Command("del_chat"), F.content_type == ContentType.TEXT)
async def cmd_del_chat(message: Message, state: FSMContext):
    if message.from_user.username in await Func.getAdm():
        await message.answer(
            Text.chatid_text,
            reply_markup=Keyboards.undo
        )
        await state.set_state(AdminActions.del_chat)

@dp.message(AdminActions.del_chat, F.content_type == ContentType.TEXT)
async def link_del_chat(message: Message, state: FSMContext):
    if message.text == '/Undo':
        await message.answer(Text.undo_text)
        await state.clear()
        return await start(message, state)
    await message.answer(Text.deletechat_text, reply_markup=Keyboards.all_btn) if await Func.deleteChats(message.text) else await message.answer("Такого чата нет", reply_markup=Keyboards.all_btn)
    await state.clear()

@dp.message(Command("del_admin"),F.content_type == ContentType.TEXT)
async def cmd_del_admin(message: Message, state: FSMContext):
    if message.from_user.username in await Func.getAdm():
        await message.answer(
            Text.username_text,
            reply_markup=Keyboards.undo
        )
        await state.set_state(AdminActions.del_admin)

@dp.message(AdminActions.del_admin, F.content_type == ContentType.TEXT)
async def link_del_admin(message: Message, state: FSMContext):
    admin_name = message.text.replace('@','')
    if message.text == '/Undo':
        await message.answer(Text.undo_text)
        await state.clear()
        return await start(message, state)
    await message.answer(Text.admindel_text, reply_markup=Keyboards.all_btn) if await Func.deleteAdmins(admin_name) else await message.answer("Такого админа нет", reply_markup=Keyboards.all_btn)
    await state.clear()

@dp.message(Command('help'))
async def help(message: types.Message):
    await message.reply(Text.help_text)

@dp.message(Command('status'), F.content_type == ContentType.TEXT)
async def status(message: types.Message):
    if message.chat.id in await Func.getCht():
        cht = await Func.getCht()
        if len(cht) != 0:
            command = message.text.split(' ')
            if len(command) == 1:
                output = Text.orderr_id
            else:
                result = await Func.payment_info(command[1])
                if result == Text.qr_code:
                    output = result
                else:
                    output = await Func.convert(result)
            await message.reply(
                output
                )
        else:
            await bot.send_message(message.chat.id, Text.private_chat)
    else: await bot.send_message(message.chat.id, Text.status_in)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
