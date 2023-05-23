from aiogram import types
from bot.callbacks.factories.image_info import (prompt_only, full_prompt, regenerate, import_prompt, back)


def get_img_info_keyboard(p_id: str) -> types.InlineKeyboardMarkup:
    buttons = [types.InlineKeyboardButton(text="📋 Show prompts", callback_data=prompt_only.new(p_id=p_id)),
               types.InlineKeyboardButton(text="🧿 Show full info", callback_data=full_prompt.new(p_id=p_id)),
               types.InlineKeyboardButton(text="🪄 Import prompt", callback_data=import_prompt.new(p_id=p_id)),
               types.InlineKeyboardButton(text="🔁︰ ReGenerate Image", callback_data=regenerate.new(p_id=p_id))]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_img_back_keyboard(p_id: str) -> types.InlineKeyboardMarkup:
    buttons = [types.InlineKeyboardButton(text="👈 Back", callback_data=back.new(p_id=p_id))]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
