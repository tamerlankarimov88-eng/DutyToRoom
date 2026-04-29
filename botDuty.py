import datetime
import aiocron
import pytz
from aiogram import Bot, Dispatcher, types, executor

# Ваш токен уже здесь
API_TOKEN = '8763045727:AAE8-quJT8-81q4197wtCfloJFZiJW2zAoc'
# Укажите ID группы (например, -100123456789)
GROUP_ID = 'ID_ВАШЕЙ_ГРУППЫ' 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
moscow_tz = pytz.timezone('Europe/Moscow')

# График по дням недели
DUTY_SCHEDULE = {
    0: "Раянов Радмир и Нецвитай Влад",     # Понедельник
    1: "Пронин Влад и Пугачёв Влад",       # Вторник
    2: "Султанов Вадим и Каримов Тамерлан", # Среда
    3: "Раянов Радмир и Нецвитай Влад",     # Четверг
    4: "Пронин Влад и Пугачёв Влад",       # Пятница
    5: "🧹 ПХД — Убираются все!",            # Суббота
    6: "Султанов Вадим и Каримов Тамерлан"  # Воскресенье
}

WEEKDAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

def get_weekly_text():
    """Динамически формирует график на 7 дней вперед"""
    now = datetime.datetime.now(moscow_tz)
    text = "📅 **График дежурств на неделю:**\n\n"
    
    for i in range(7):
        day = now + datetime.timedelta(days=i)
        w_idx = day.weekday()
        date_str = day.strftime("%d.%m")
        duty = DUTY_SCHEDULE[w_idx]
        
        if i == 0:
            text += f"➡️ **{date_str} ({WEEKDAYS_RU[w_idx]}): {duty}** (Сегодня)\n"
        else:
            text += f"▫️ {date_str} ({WEEKDAYS_RU[w_idx]}): {duty}\n"
    return text

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Бот дежурств запущен!\n/today — дежурные на сегодня\n/week — график на 7 дней")

@dp.message_handler(commands=['today'])
async def cmd_today(message: types.Message):
    now = datetime.datetime.now(moscow_tz)
    info = DUTY_SCHEDULE[now.weekday()]
    await message.answer(f"📅 **Сегодня дежурят:**\n{info}", parse_mode="Markdown")

@dp.message_handler(commands=['week'])
async def cmd_week(message: types.Message):
    await message.answer(get_weekly_text(), parse_mode="Markdown")

# Авто-уведомление каждый день в 20:00 по МСК
@aiocron.crontab('0 20 * * *', tz=moscow_tz)
async def scheduled_msg():
    now = datetime.datetime.now(moscow_tz)
    info = DUTY_SCHEDULE[now.weekday()]
    text = f"🔔 **Напоминание (20:00):**\nСегодня дежурят: {info}"
    try:
        await bot.send_message(GROUP_ID, text, parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

if __name__ == '__main__':
    print("Бот успешно запущен и следит за графиком...")
    executor.start_polling(dp, skip_updates=True)
