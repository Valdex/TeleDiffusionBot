from bot.common import dp
from bot.db import db, DBTables
from aiogram import types
from aiogram.types import Message
from .factories.image_info import full_prompt, prompt_only, regenerate, import_prompt, back
from bot.keyboards.image_info import get_img_info_keyboard, get_img_back_keyboard
from bot.handlers.txt2img.txt2img import generate_command
from bot.utils.cooldown import throttle
from bot.utils.private_keyboard import other_user
from bot.modules.api.objects.prompt_request import Generated
from bot.utils.errorable_command import wrap_exception


@wrap_exception()
async def on_back(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    await call.message.edit_text(
        "Image was generated using this bot",
        parse_mode='html',
        reply_markup=get_img_info_keyboard(p_id)
    )


@wrap_exception()
@throttle(5)
async def on_prompt_only(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    prompt: Generated = db[DBTables.generated].get(p_id)

    await call.message.edit_text(
        f"🖤 Prompt: {prompt.prompt.prompt} \n"
        f"{f'🐊 Negative: {prompt.prompt.negative_prompt}' if prompt.prompt.negative_prompt else ''}",
        parse_mode='html',
        reply_markup=get_img_back_keyboard(p_id)
    )


@wrap_exception()
@throttle(5)
async def on_full_info(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    prompt: Generated = db[DBTables.generated].get(p_id)

    await call.message.edit_text(
        f"🖤 Prompt: {prompt.prompt.prompt} \n"
        f"🐊 Negative: {prompt.prompt.negative_prompt} \n"
        f"💫 Model: {prompt.model} \n"
        f"🪜 Steps: {prompt.prompt.steps} \n"
        f"🧑‍🎨 CFG Scale: {prompt.prompt.cfg_scale} \n"
        f"🖥️ Size: {prompt.prompt.width}x{prompt.prompt.height} \n"
        f"😀 Restore faces: {'on' if prompt.prompt.restore_faces else 'off'} \n"
        f"⚒️ Sampler: {prompt.prompt.sampler} \n"
        f"🌱 Seed: {prompt.seed}",
        parse_mode='html',
        reply_markup=get_img_back_keyboard(p_id)
    )


@wrap_exception()
@throttle(5)
async def on_regenerate(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    prompt: Generated = db[DBTables.generated].get(p_id)

    regenerate_message = Message(
        message_id=call.message.message_id,
        from_user=call.from_user,
        chat=call.message.chat,
        date=call.message.date,
        text=call.message.text,
        entities=call.message.entities,
        caption_entities=call.message.caption_entities,
        reply_markup=call.message.reply_markup,
        args=prompt.prompt.prompt
    )

    await generate_command(regenerate_message)

@wrap_exception()
@throttle(5)
async def on_import(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    generated: Generated = db[DBTables.generated].get(p_id)
    prompt = generated.prompt
    prompt.creator = call.from_user.id
    db[DBTables.prompts][call.from_user.id] = prompt
    await db[DBTables.config].write()

    await call.message.edit_text(
        f"️🥐 Prompt imported",
        reply_markup=get_img_back_keyboard(p_id)
    )


def register():
    dp.register_callback_query_handler(on_prompt_only, prompt_only.filter())
    dp.register_callback_query_handler(on_back, back.filter())
    dp.register_callback_query_handler(on_full_info, full_prompt.filter())
    dp.register_callback_query_handler(on_regenerate, regenerate.filter())
    dp.register_callback_query_handler(on_import, import_prompt.filter())
