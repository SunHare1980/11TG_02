from config import TOKEN, APIKEY, JAKEY
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/Weather")

@dp.message(Command('Weather'))
async def help(message: Message):
    weather = get_weather('Kursk')
    await message.answer("Погода в городе Курск "+ str(weather['main']['temp'])+"°C\n"+str(weather['weather'][0]['description']))

@dp.message(CommandStart())
async def start(message: Message):
    # tts = gTTS(text='Привет!', lang='ru')
    # tts.save("Privet.ogg")
    await message.answer("Приветики, я бот!")
    audio = FSInputFile("Privet.ogg")
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
async def main():
    await dp.start_polling(bot)

def get_weather(city):
   api_key = APIKEY
   #адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
   url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru&units=metric"
   #для получения результата нам понадобится модуль requests
   response = requests.get(url)
   #прописываем формат возврата результата
   return response.json()
@dp.message(F.photo)
async def react_photo(message: Message):
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')

@dp.message()
async def start(message: Message):
    await message.answer(translate_text(message.text, JAKEY))


import requests


def translate_text(text, api_key):
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api_key}"
    }

    body = {
        "targetLanguageCode": "en",
        "texts": [text],
        "folderId": "b1ggie2lfmuj3ilan7uj"  # замените на ваш идентификатор каталога
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        translated_texts = response.json().get("translations", [])
        if translated_texts:
            return translated_texts[0].get("text", "")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return None


if __name__ == "__main__":
    asyncio.run(main())


    # { % if weather %}
    # < h3 > Погода
    # в
    # {{weather['name']}} < / h3 >
    # < p > Температура: {{weather['main']['temp']}}°C < / p >
    # < p > Погода: {{weather['weather'][0]['description']}} < / p >
