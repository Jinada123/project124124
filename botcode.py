from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import logging, asyncio
import base64, requests
from openai import OpenAI

from config import key, token

dp = Dispatcher()


client = OpenAI(api_key=key)


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer("Здравствуйтpipе! Добро пожаловать в наш кредитный сервис. \n"
                         "Мы поможем вам рассчитать возможность получения кредита и оптимальный выбор банка на основе ваших финансовых данных. \n" 
                         "Для того чтобы мы могли рассчитать для вас условия кредита, пожалуйста, заполните анкету следующим образом: \n\n"
                         "Я хочу получить кредит в (ваша страна) основываясь на валюте (ваша валюта): \n"
                         "1) Сумма кредита, которую я хочу получить:  \n"
                         "2) Процентная ставка или фиксированная/плавающая ставка должна быть:  \n"
                         "3) Срок кредита:  \n"
                         "4) Тип платежей (выбирая между аннуитетным и дифференцированным):  \n"
                         "5) Мой ежемесячный доход: \n"
                         "6) У меня положительная кредитная история: (да/нет). \n"
                         "7) У меня есть залог или поручители? (да/нет). \n"
                         "На основании введённых данных, рассчитай возможные условия моего кредита и оцени выдадут ли мне его?")
    


@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer("1. Halyk Bank: \n"
                          "Запрос суммы кредита: Возможен через отделения банка, мобильное приложение или онлайн-банкинг. \n"
                          "Запрос процентной ставки: Процентная ставка варьируется в зависимости от программы кредитования и начинается от 17-20%. \n"
                          "Запрос срока кредита: Предоставляются кредиты на срок до 7 лет. \n"
                          "Выбор типа платежей: Возможен выбор аннуитетных или дифференцированных платежей. \n"
                          "Запрос ежемесячного дохода: Требуется подтверждение дохода при заявке на кредит. \n"
                          "Проверка кредитной истории: Банк проверяет кредитную историю заемщика через кредитные бюро. \n"
                          "Залог или поручители: Возможно требование залога или поручителей в зависимости от суммы кредита. \n\n"
                          "2. Kaspi Bank: \n"
                          "Запрос суммы кредита: Доступен онлайн через приложение Kaspi.kz. \n"
                          "Запрос процентной ставки: В среднем процентная ставка от 20-25%. \n"
                          "Запрос срока кредита: Срок кредита может составлять до 5 лет. \n"
                          "Выбор типа платежей: Только аннуитетные платежи. \n"
                          "Запрос ежемесячного дохода: Необходим, но подтверждение часто не требуется для небольших сумм. \n"
                          "Проверка кредитной истории: Проводится через внутреннюю систему и кредитные бюро. \n"
                          "Залог или поручители: Чаще всего не требуются для небольших сумм. \n\n"
                          "3. Qazkom (Казкоммерцбанк): \n"
                          "После слияния с Halyk Bank основные параметры кредитования схожи с Halyk Bank. \n\n"
                          "4. Нурбанк: \n"
                          "Запрос суммы кредита: Предоставляется через отделения или онлайн-банкинг. \n"
                          "Запрос процентной ставки: Ставка зависит от продукта, начиная от 18%. \n"
                          "Запрос срока кредита: Возможен до 5-7 лет. \n"
                          "Выбор типа платежей: Предлагаются аннуитетные или дифференцированные платежи. \n"
                          "Запрос ежемесячного дохода: Требуется справка о доходах или иные документы. \n"
                          "Проверка кредитной истории: Проверка через бюро кредитных историй. \n"
                          "Залог или поручители: Может требоваться залог для крупных сумм. \n\n"
                          "5. Jusan Bank: \n"
                          "Запрос суммы кредита: Можно оформить онлайн или в отделении банка. \n"
                          "Запрос процентной ставки: Процентные ставки начинаются с 15-18%. \n"
                          "Запрос срока кредита: Максимальный срок — до 5-7 лет. \n"
                          "Выбор типа платежей: Аннуитетные платежи.\n"
                          "Запрос ежемесячного дохода: Требуется подтверждение доходов. \n"
                          "Проверка кредитной истории: Проводится обязательная проверка кредитной истории. \n"
                          "Залог или поручители: Для крупных сумм требуется залог, для небольших — поручители необязательны. \n\n"
                          "6. Eurasian Bank: \n"
                          "Запрос суммы кредита: Доступен через мобильное приложение или в отделении. \n"
                          "Запрос процентной ставки: Ставка варьируется от 19-23%. \n"
                          "Запрос срока кредита: Возможны кредиты на срок до 7 лет. \n"
                          "Выбор типа платежей: Предлагаются аннуитетные платежи. \n"
                          "Запрос ежемесячного дохода: Требуется подтверждение доходов. \n"
                          "Проверка кредитной истории: Проводится обязательная проверка кредитной истории. \n"
                          "Залог или поручители: Могут потребоваться в зависимости от суммы кредита. \n")



def ask_gpt35turbo(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{text}"},
        ]
    )
    answer = response.choices[0].message.content
    print(answer)
    return answer

@dp.message()
async def telegram(message: Message) -> None:
    answer = ask_gpt35turbo(message.text)
    try:
        await message.answer(answer)
    except TypeError:
            await message.answer("Nice try!")

async def main() -> None:
    bot = Bot(token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
