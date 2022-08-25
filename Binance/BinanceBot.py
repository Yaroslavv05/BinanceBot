import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from binance.client import Client
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Config import API_KEY, SECRET_KEY, TOKEN
from DateFutures import DateFutures
from DateSpot import DateSpot

storage = MemoryStorage()
client = Client(API_KEY, SECRET_KEY)
TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
markup0 = ReplyKeyboardMarkup(resize_keyboard=True)
markup0.add('Начать!')
markup4 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup4.add('5 мин', '15 мин', '60 мин', '240 мин')
markup5 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup5.add('💵 Покупать/продавать монетку', '🤑 Торговать на фьючерсах', 'ℹ️ Информационная страница')
markup6 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup6.add("Начать торговлю", 'Узнать баланс', 'Отмена!')
markup2 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup2.add('Цена монетки', 'Узнать за какую цену мы купили/продажу монетку', 'Все ордера которые были на этом аккаунте', 'Вывод цен монетки за 5/15 мин', 'Отмена!')
markup1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup1.add('Начать торговать', 'Счет кошелька', 'Отмена!')
f = open('../Цена за покупку.txt', 'r')
n = open('../Цена за продажу.txt', 'r')
price_5m = open('../Цены за 5 мин.txt', 'w')
price_15m = open('../Цены за 15 мин.txt', 'w')
price_5m_r = open('../Цены за 5 мин.txt', 'rb')
price_15m_r = open('../Цены за 15 мин.txt', 'rb')

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.full_name}\nЯ бот который торгует на Binance\nЧто бы начать роботу нажми на кнопку "Начать!"', reply_markup=markup0)

class FSMcoin_price(StatesGroup):
    name = State()
class FSMcoin_price_avg(StatesGroup):
    name = State()
class FSMtrade_coin(StatesGroup):
    full_name_coin = State()
    name_coin = State()
    pair = State()
    colvo_coin = State()
    profit_spot = State()
    avg_time = State()
class FSMFuturesTrade(StatesGroup):
    name_coin_futures = State()
    leverage = State()
    sum_usdt = State()
    profit = State()
    name_coin = State()
@dp.message_handler(content_types=['text'], state=None)
async def bot_func(message: types.Message):
    print(f"id: {message.from_user.id} | Name: {message.from_user.full_name} | Msg: {message.text} | Time: {message.date}")
    if message.text == 'Начать!':
        await bot.send_message(message.from_user.id, 'Главное меню:', reply_markup=markup5)
    elif message.text == '💵 Покупать/продавать монетку':
        await bot.send_message(message.from_user.id, 'Выбирайте:', reply_markup=markup1)
    elif message.text == '🤑 Торговать на фьючерсах':
        await bot.send_message(message.from_user.id, 'Выбирайте:', reply_markup=markup6)
    elif message.text == 'ℹ️ Информационная страница':
        await bot.send_message(message.from_user.id, 'Выбирайте:', reply_markup=markup2)
    elif message.text == 'Отмена!':
        await bot.send_message(message.from_user.id, 'Главное меню:', reply_markup=markup5)
    elif message.text == 'Цена монетки':
        await FSMcoin_price.name.set()
        await bot.send_message(message.from_user.id, 'Введи название монетки:\n\nНапример: BTCUSDT')

        @dp.message_handler(state=FSMcoin_price.name)
        async def coin_price_vuvod(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['name'] = message.text
            if len(data['name']) == 7 or len(data['name']) == 8:
                price_all = client.get_symbol_ticker(symbol=data['name'])
                price = str(float(price_all.get('price')))
                await bot.send_message(message.from_user.id, price + ' $', reply_markup=markup2)
                await state.finish()
            elif len(data['name']) <= 6 or len(data['name']) >= 9:
                await FSMcoin_price.name.set()
                await bot.send_message(message.from_user.id, 'Название монетки должно содержать 7/8 символов!\n\nВведите повторно')

                @dp.message_handler(state=FSMcoin_price.name)
                async def coin_price_vuvod(message: types.Message, state: FSMContext):
                    async with state.proxy() as data:
                        data['name'] = message.text
    elif message.text == 'Вывод цен монетки за 5/15 мин':
        await FSMcoin_price_avg.name.set()
        await bot.send_message(message.from_user.id, 'Введи название монетки:')

        @dp.message_handler(state=FSMcoin_price_avg.name)
        async def coin_avg_vuvod(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['name'] = message.text
            if len(data['name']) == 7 or len(data['name']) == 8:
                klines_5m = client.get_historical_klines(data['name'], Client.KLINE_INTERVAL_5MINUTE, '1 day UTC')
                for i in range(len(klines_5m)):
                    a_5 = klines_5m[i]
                    price_5m.write(str(float(a_5[3])) + ' $' + '\n')
                klines_15m = client.get_historical_klines(data['name'], Client.KLINE_INTERVAL_15MINUTE, '1 day UTC')
                for i in range(len(klines_15m)):
                    a_15 = klines_15m[i]
                    price_15m.write(str(float(a_15[3])) + ' $' + '\n')
                price_5m.close()
                price_15m.close()
                await bot.send_document(message.from_user.id, price_5m_r)
                await bot.send_document(message.from_user.id, price_15m_r)
            elif len(data['name']) <= 6 or len(data['name']) >= 8:
                await FSMcoin_price_avg.name.set()
                await bot.send_message(message.from_user.id, 'Название монетки должно содержать 7/8 символов!\n\nВведите повторно')

                @dp.message_handler(state=FSMcoin_price_avg.name)
                async def coin_avg_vuvod(message: types.Message, state: FSMContext):
                    async with state.proxy() as data:
                        data['name'] = message.text
    elif message.text == 'Начать торговать':
        balance = client.get_asset_balance(asset='USDT')
        balance_get = float(balance.get('free'))
        if balance_get > 10:
            await bot.send_message(message.from_user.id, '❗️ Средств недостаточно ❗️')
        elif balance_get >= 10:
            await FSMtrade_coin.full_name_coin.set()
            await bot.send_message(message.from_user.id, 'Введите название монетки:\n\nНапример: BTCUSDT')

            @dp.message_handler(state=FSMtrade_coin.full_name_coin)
            async def coin_avg_vuvod(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['full_name_coin'] = message.text
                await FSMtrade_coin.next()
                if len(data['full_name_coin']) <= 6 or len(data['full_name_coin']) >= 9:
                    await FSMtrade_coin.full_name_coin.set()
                    await bot.send_message(message.from_user.id, 'Название монетки должно содержать 7/8 символов!\n\nВведите повторно')
                elif len(data['full_name_coin']) == 7 or len(data['full_name_coin']) == 8:
                    await FSMtrade_coin.name_coin.set()
                    await bot.send_message(message.from_user.id, 'Введите название монетки например:\n\nНапример:BTC')

                    @dp.message_handler(state=FSMtrade_coin.name_coin)
                    async def coin_avg_vuvod(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            data['name_coin'] = message.text
                        await FSMtrade_coin.next()
                        if len(data['name_coin']) <= 2 or len(data['name_coin']) >= 5:
                            await FSMtrade_coin.name_coin.set()
                            await bot.send_message(message.from_user.id, 'Название монетки должно содержать 3/4 символов!\n\nВведите повторно')
                        elif len(data['name_coin']) == 3 or len(data['name_coin']) == 4:
                            await FSMtrade_coin.pair.set()
                            await bot.send_message(message.from_user.id, "Введите отношение монетки:\n\nНапример:USDT")

                            @dp.message_handler(state=FSMtrade_coin.pair)
                            async def coin_avg_vuvod(message: types.Message, state: FSMContext):
                                async with state.proxy() as data:
                                    data['pair'] = message.text
                                await FSMtrade_coin.next()
                                if len(data['pair']) <= 2 or len(data['pair']) >= 5:
                                    await FSMtrade_coin.pair.set()
                                    await bot.send_message(message.from_user.id, 'Название пары должно содержать 3/4 символов!\n\nВведите повторно')
                                elif len(data['pair']) == 3 or len(data['pair']) == 4:
                                    await FSMtrade_coin.colvo_coin.set()
                                    await bot.send_message(message.from_user.id, 'Введите какое кол-во монет хотите поставить:\n\nНапример: 1')

                                    @dp.message_handler(state=FSMtrade_coin.colvo_coin)
                                    async def coin_avg_vuvod(message: types.Message, state: FSMContext):
                                        async with state.proxy() as data:
                                            data['colvo_coin'] = float(message.text)
                                        await FSMtrade_coin.next()
                                        if data['colvo_coin'] <= 0.00042:
                                            await FSMtrade_coin.colvo_coin.set()
                                            await bot.send_message(message.from_user.id, 'Минимальное кол-во монет - 0,00043 BTC ≈ 10$\n\nВведите повторно')
                                        elif data['colvo_coin'] >= 0.00043:
                                            await FSMtrade_coin.profit_spot.set()
                                            await bot.send_message(message.from_user.id, 'Введите какую прибыль вы хотите в центах:\n\nНапример: 0.03')

                                            @dp.message_handler(state=FSMtrade_coin.profit_spot)
                                            async def coin_avg_vuvod(message: types.Message, state: FSMContext):
                                                async with state.proxy() as data:
                                                    data['profit_spot'] = float(message.text)
                                                await FSMtrade_coin.next()
                                                if data['profit_spot'] < 0.01:
                                                    await FSMtrade_coin.profit_spot.set()
                                                    await bot.send_message(message.from_user.id, 'Минимальный профит который вы можете ввести - 0.01\n\nВведите повторно')
                                                elif data['profit_spot'] >= 0.01:
                                                    await FSMtrade_coin.avg_time.set()
                                                    await bot.send_message(message.from_user.id,'Ввыберите среднее время за которое бот будет покупать монетки:', reply_markup=markup4)

                                                    @dp.message_handler(state=FSMtrade_coin.avg_time)
                                                    async def coin_avg_vuvod(message: types.Message, state: FSMContext):
                                                        async with state.proxy() as data:
                                                            data['avg_time'] = message.text
                                                            main_spot = DateSpot(message.from_user.id, data['full_name_coin'], data['name_coin'], data['pair'], data['colvo_coin'], data['profit_spot'], data['avg_time'])
                                                            main_spot.input_date()
                                                        if data['avg_time'] == '5 мин':
                                                            await bot.send_message(message.from_user.id, 'Бот начинает работу!\n\nБудет работать с:\nМонеткой - ' + data['full_name_coin'] + '\nКол-во монет - ' + str(data['colvo_coin']) + '\nПрофит - ' + str(data['profit_spot']) + ' $\nСреднее время - ' + data['avg_time'])
                                                        else:
                                                            await FSMtrade_coin.avg_time.set()
                                                            await bot.send_message(message.from_user.id, '❗️ Ошибка ❗️\n\nПовторите попытку')
    elif message.text == 'Счет кошелька':
        assets_ada = client.get_asset_balance(asset='ADA')
        ada_balance = assets_ada.get('free')
        assets_bnb = client.get_asset_balance(asset='BNB')
        bnb_balance = assets_bnb.get('free')
        assets_xrp = client.get_asset_balance(asset='XRP')
        xrp_balance = assets_xrp.get('free')
        assets_usdt = client.get_asset_balance(asset='USDT')
        usdt_balance = assets_usdt.get('free')
        ada_price = client.get_symbol_ticker(symbol='ADAUSDT')
        symvol = ada_price.get('symbol')
        price = ada_price.get('price')
        bnb_price = client.get_symbol_ticker(symbol='BNBUSDT')
        b_price = bnb_price.get('price')
        xrp_price = client.get_symbol_ticker(symbol='XRPUSDT')
        x_price = xrp_price.get('price')
        await bot.send_message(message.from_user.id, 'Баланс кошелька USDT: ' + str(float(usdt_balance)) + '\nМонеток ADA: ' + str(float(ada_balance)) + ' шт. ' + 'в $ 1 шт. = ' + str(float(price)) + '\nМонеток BNB: ' + str(float(bnb_balance)) + ' шт. ' + 'в $ 1 шт. = ' + str(float(b_price)) + '\nМонеток XRP: ' + str(float(xrp_balance)) + ' шт. ' 'в $ 1 шт. = ' + str(float(x_price)))
    elif message.text == 'Узнать за какую цену мы купили/продажу монетку':
        for line in f:
            await bot.send_message(message.from_user.id, 'Цена за покупку составляет:  ' + line + '  $')
        for line3 in n:
            await bot.send_message(message.from_user.id, 'Цена за продажу составляет:  ' + line3 + '  $')
        f.close()
        n.close()
    elif message.text == 'Все ордера которые были на этом аккаунте':
        await FSMFuturesTrade.name_coin.set()
        await bot.send_message(message.from_user.id, 'Введите название монетки для получение данных:\n\n(ЕСЛИ НИЧЕГО НЕ ВЫВОДИТЬСЯ ЗНАЧИТ С ДАННОЙ МОНЕТОЙ НИЧЕГО НЕ ПРОИСХОДИЛО У ВАС НА АККАУНТЕ)')

        @dp.message_handler(state=FSMFuturesTrade.name_coin)
        async def name_coin_futures(message: types.Message, state: FSMContext):
             async with state.proxy() as data:
                 data['name_coin'] = message.text
             order = client.get_all_orders(symbol=data['name_coin'])
             element_count = len([item for item in order])
             for i in range(element_count):
                 order_symbol = order[i].get('symbol')
                 order_price = order[i].get('price')
                 order_origQty = order[i].get('origQty')
                 order_cummulativeQuoteQty = order[i].get('cummulativeQuoteQty')
                 order_side = order[i].get('side')
                 await bot.send_message(message.from_user.id, 'Название монетки: ' + order_symbol + '\nЦена за которую купили/продали монетку: ' + order_price + '\nКол-во монеток которых купили/продали: ' + order_origQty + '\nСумма монеток которых мы купили/продали: ' + order_cummulativeQuoteQty + '\nЧто мы с этой монеткой сделали: ' + order_side)
             await state.finish()
    elif message.text == 'Узнать баланс':
        balance_futures = client.futures_account_balance()
        balance_futures_get = float(balance_futures[6].get('balance'))
        balance_futures_get_round = str(round(balance_futures_get, 2))
        await bot.send_message(message.from_user.id, 'Ваш баланс: ' + balance_futures_get_round + ' $', reply_markup=markup6)
    elif message.text == 'Начать торговлю':
        open_orders_futures = client.futures_get_open_orders()
        open_orders_futures_len = len(open_orders_futures)
        if open_orders_futures_len == 0:
            await FSMFuturesTrade.name_coin_futures.set()
            await bot.send_message(message.from_user.id, 'Введите название монеетки:')

            @dp.message_handler(state=FSMFuturesTrade.name_coin_futures)
            async def name_coin_futures(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['name_coin_futures'] = message.text
                await FSMFuturesTrade.next()
                if len(data['name_coin_futures']) <= 6 or len(data['name_coin_futures']) >= 9:
                    await FSMFuturesTrade.name_coin_futures.set()
                    await bot.send_message(message.from_user.id,
                                           'Название монетки должно содержать 7/8 символов!\n\nВведите повторно')
                elif len(data['name_coin_futures']) == 7 or len(data['name_coin_futures']) == 8:
                    await FSMFuturesTrade.leverage.set()
                    await bot.send_message(message.from_user.id, 'Введите кредитное плечо:')

                    @dp.message_handler(state=FSMFuturesTrade.leverage)
                    async def name_coin_futures(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            data['leverage'] = int(message.text)
                        await FSMFuturesTrade.next()
                        if data['leverage'] <= 0 or data['leverage'] >= 126:
                            await FSMFuturesTrade.leverage.set()
                            await bot.send_message(message.from_user.id,
                                                   'Кредитное плечо может быть от 1 до 125!\n\nВведите повторно')
                        else:
                            await FSMFuturesTrade.sum_usdt.set()
                            balance_futures_trade = client.futures_account_balance()
                            balance_futures_trade_get = round(float(balance_futures_trade[6].get('balance')), 2)
                            await bot.send_message(message.from_user.id,
                                                   'Введите какую сумму хотите поставить:\n\nВаш баланс: ' + str(
                                                       balance_futures_trade_get) + ' $')

                            @dp.message_handler(state=FSMFuturesTrade.sum_usdt)
                            async def name_coin_futures(message: types.Message, state: FSMContext):
                                async with state.proxy() as data:
                                    data['sum_usdt'] = float(message.text)
                                if data['sum_usdt'] <= 0 or data['sum_usdt'] > balance_futures_trade_get:
                                    await FSMFuturesTrade.sum_usdt.set()
                                    await bot.send_message(message.from_user.id, 'Сумма не может привышать вашего баланса или  быть меньше 0!\n\nВведите повторно')
                                else:
                                    await FSMFuturesTrade.profit.set()
                                    await bot.send_message(message.from_user.id, 'Введите какой вы хотите процент прибыли:\n\nНапример: 1')

                                    @dp.message_handler(state=FSMFuturesTrade.profit)
                                    async def name_coin_futures(message: types.Message, state: FSMContext):
                                        async with state.proxy() as data:
                                            data['profit'] = float(message.text)
                                            main = DateFutures(message.from_user.id, data['name_coin_futures'], data['leverage'], data['sum_usdt'], data['profit'])
                                            main.input_date()
                                        if data['profit'] <= 0:
                                            await FSMFuturesTrade.profit.set()
                                            await bot.send_message(message.from_user.id, 'Процент прибыли не может быть меньше или равняться 0\n\nВведите повторно')
                                        elif data['profit'] > 0:
                                            main.get_info()
        elif open_orders_futures_len > 0:
            await bot.send_message(message.from_user.id, '❗️ Бот уже работает ❗️\n\nОжидайте', reply_markup=markup5)
    else:
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markup5)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
else:
    print('бот не работает!')