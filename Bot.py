import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = "7324745052:AAEfVnkTGq5Ip9P5l7uIXkdydyMRDZz6IZw"
CHANNEL_ID = "@elektr_toki"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def check_subscription(user_id):
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    return member.status in ["member", "administrator", "creator"]

@dp.callback_query_handler(lambda call: call.data == "answer")
async def answer_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await call.message.answer("Siz kanalga a'zo bo'lgansiz! Javobingiz qabul qilindi.")
    else:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔗 Kanalga obuna bo'lish", url="https://t.me/elektr_toki")
        )
        await call.message.answer("Iltimos, kanalga obuna bo'ling!", reply_markup=keyboard)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Javob berish", callback_data="answer")
    )
    await message.answer("Viktorina savoliga javob berish uchun quyidagi tugmani bosing:", reply_markup=keyboard)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
