import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from binance.client import Client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Config import API_KEY, SECRET_KEY, TOKEN
from DateFutures import DateFutures
from DateSpot import DateSpot
from DateUsers import DateUsers
from PriceCoin import knowCoin
from PriceDisplay import Display
from WalletAccount import walet
from AllOrders import Orsers
from WalletAccountFutureses import WalletFutures

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

@dp.message_handler(commands=['start'])#start
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.full_name}\nЯ бот который торгует на Binance\nЧто бы начать роботу нажми на кнопку "Начать!"', reply_markup=markup0)
    date_users = DateUsers(message.from_user.id, message.from_user.username, message.from_user.full_name)
    date_users.recorde_in_date()

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
                knowPrice = knowCoin(data['name'])
                knowPrice.know()
                await bot.send_message(message.from_user.id, knowPrice.price + ' $', reply_markup=markup2)
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
                record = Display(data['name'])
                record.display()
                await bot.send_document(message.from_user.id, record.price_5m_r)
                await bot.send_document(message.from_user.id, record.price_15m_r)
                await state.finish()
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
        if balance_get < 10:
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
                                                            main_spot.get_info()
                                                            await bot.send_message(message.from_user.id, 'Бот закончит работу когда ' + data['full_name_coin'] + ' вырастет на ' + str(data['profit_spot']) + ' ¢')
                                                        elif data['avg_time'] == '15 мин':
                                                            await bot.send_message(message.from_user.id, 'Бот начинает работу!\n\nБудет работать с:\nМонеткой - ' + data['full_name_coin'] + '\nКол-во монет - ' + str(data['colvo_coin']) + '\nПрофит - ' + str(data['profit_spot']) + ' $\nСреднее время - ' + data['avg_time'])
                                                            main_spot.get_info()
                                                            await bot.send_message(message.from_user.id, 'Бот закончит работу когда ' + data['full_name_coin'] + ' вырастет на ' + str(data['profit_spot']) + ' ¢')
                                                        elif data['avg_time'] == '60 мин':
                                                            await bot.send_message(message.from_user.id, 'Бот начинает работу!\n\nБудет работать с:\nМонеткой - ' + data['full_name_coin'] + '\nКол-во монет - ' + str(data['colvo_coin']) + '\nПрофит - ' + str(data['profit_spot']) + ' $\nСреднее время - ' + data['avg_time'])
                                                            main_spot.get_info()
                                                            await bot.send_message(message.from_user.id, 'Бот закончит работу когда ' + data['full_name_coin'] + ' вырастет на ' + str(data['profit_spot']) + ' ¢')
                                                        elif data['avg_time'] == '240 мин':
                                                            await bot.send_message(message.from_user.id, 'Бот начинает работу!\n\nБудет работать с:\nМонеткой - ' + data['full_name_coin'] + '\nКол-во монет - ' + str(data['colvo_coin']) + '\nПрофит - ' + str(data['profit_spot']) + ' $\nСреднее время - ' + data['avg_time'])
                                                            main_spot.get_info()
                                                            await bot.send_message(message.from_user.id, 'Бот закончит работу когда ' + data['full_name_coin'] + ' вырастет на ' + str(data['profit_spot']) + ' ¢')
                                                        else:
                                                            await FSMtrade_coin.avg_time.set()
                                                            await bot.send_message(message.from_user.id, '❗️ Ошибка ❗️\n\nПовторите попытку')
    elif message.text == 'Счет кошелька':
        balance = walet()
        balance.main()
        await bot.send_message(message.from_user.id, 'Баланс кошелька USDT: ' + str(float(balance.usdt_balance)) + '\nМонеток ADA: ' + str(float(balance.ada_balance)) + ' шт. ' + 'в $ 1 шт. = ' + str(float(balance.price)) + '\nМонеток BNB: ' + str(float(balance.bnb_balance)) + ' шт. ' + 'в $ 1 шт. = ' + str(float(balance.b_price)) + '\nМонеток XRP: ' + str(float(balance.xrp_balance)) + ' шт. ' 'в $ 1 шт. = ' + str(float(balance.x_price)))
    elif message.text == 'Все ордера которые были на этом аккаунте':
        await FSMFuturesTrade.name_coin.set()
        await bot.send_message(message.from_user.id, 'Введите название монетки для получение данных:\n\n(ЕСЛИ НИЧЕГО НЕ ВЫВОДИТЬСЯ ЗНАЧИТ С ДАННОЙ МОНЕТОЙ НИЧЕГО НЕ ПРОИСХОДИЛО У ВАС НА АККАУНТЕ)')

        @dp.message_handler(state=FSMFuturesTrade.name_coin)
        async def name_coin_futures(message: types.Message, state: FSMContext):
             async with state.proxy() as data:
                 data['name_coin'] = message.text
             orders = Orsers(data['name_coin'])
             orders.main()
             await bot.send_message(message.from_user.id, 'Название монетки: ' + orders.order_symbol + '\nЦена за которую купили/продали монетку: ' + orders.order_price + '\nКол-во монеток которых купили/продали: ' + orders.order_origQty + '\nСумма монеток которых мы купили/продали: ' + orders.order_cummulativeQuoteQty + '\nЧто мы с этой монеткой сделали: ' + orders.order_side)
             await state.finish()
    elif message.text == 'Узнать баланс':
        walletFutures = WalletFutures()
        walletFutures.main()
        await bot.send_message(message.from_user.id, 'Ваш баланс: ' + walletFutures.balance_futures_get + ' $', reply_markup=markup6)
    elif message.text == 'Начать торговлю':
        open_orders_futures = client.futures_get_open_orders()
        open_orders_futures_len = len(open_orders_futures)
        if open_orders_futures_len == 0:
            await FSMFuturesTrade.name_coin_futures.set()
            await bot.send_message(message.from_user.id, 'Введите название монеетки:\n\nНапример: BTCUSDT')

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
                    await bot.send_message(message.from_user.id, 'Введите кредитное плечо:\n\nНапример:20')

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
                                            await bot.send_message(message.from_user.id, 'Бот начинает работу!\n\nБот будет работать с:\nМонеткой - ' + data['name_coin_futures'] + '\nС кредитным плечом - ' + str(data['leverage']) + '\nС суммой: ' + str(data['sum_usdt']) + '\nПрофит в %: ' + str(data['profit']))
                                            main.get_info()
        elif open_orders_futures_len > 0:
            await bot.send_message(message.from_user.id, '❗️ Бот уже работает ❗️\n\nОжидайте', reply_markup=markup5)
    else:
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markup5)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
else:
    print('бот не работает!')