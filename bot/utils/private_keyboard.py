from aiogram import types


async def other_user(call: types.CallbackQuery) -> bool:
    if not hasattr(call.message.reply_to_message, 'from_id'):
        await call.answer('Error, original call was removed', show_alert=True)
        return True
    elif call.message.reply_to_message.from_id != call.from_user.id:
        await call.answer('It is not your menu!', show_alert=True)
        return True

    return False
