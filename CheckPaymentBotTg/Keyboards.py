#Keyboards

from aiogram.types import ReplyKeyboardMarkup,  KeyboardButton
kb = [
    [KeyboardButton(text='/add_admin')],
    [KeyboardButton(text='/del_admin')],
    [KeyboardButton(text='/show_admins')],
    [KeyboardButton(text='/add_chat')],
    [KeyboardButton(text='/del_chat')],
    [KeyboardButton(text='/show_chats')]
]
all_btn = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb2 = [
    [KeyboardButton(text='/Undo')]
]
undo = ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)
