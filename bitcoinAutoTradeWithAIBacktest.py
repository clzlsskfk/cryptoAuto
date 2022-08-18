import time
import pyupbit
import datetime
import schedule
from fbprophet import Prophet

access = "9eoEhq1tzNI2MnGo5B1xG6iVWiSA4bqxgLbnGi5Z"
secret = "WQEaUd2ux1wxRx7QRzaag4iIBv4hWFuQzbNRAsRK"


data = {"krw": 100000.0, "btc": 0.0}

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def buy_market_order(ticker, price):
    if "KRW-BTC" == ticker:
        balance["krw"] -= price
        balance["btc"] += price/current_price
        print("buy = %f, %f" % (balance["krw"], balance["btc"]))

def sell_market_order(ticker, price):
    if "KRW-BTC" == ticker:
        balance["btc"] -= price
        balance["krw"] += price/current_price
        print("sell = %f, %f" % (balance["btc"], balance["krw"]))

# def get_balance(ticker):
#     """잔고 조회"""
#     #{'currency': 'KRW', 'balance': '0.10350773', 'locked': '0', 'avg_buy_price': '0', 'avg_buy_price_modified': True, 'unit_currency': 'KRW'}
#     balances = upbit.get_balances()
#     for b in balances:
#         if b['currency'] == ticker:
#             if b['balance'] is not None:
#                 print("get_balance 에서 b의 값 = ")
#                 print(b)
#                 return float(b['balance'])
#             else:
#                 return 0
#     return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

predicted_close_price = 0
def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    df = pyupbit.get_ohlcv(ticker, interval="minute5")
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds', 'y']]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=24, freq='M')
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]
    predicted_close_price = closeValue
    df.to_excel("AIData.xlsx")
    print("AIData 엑셀 생성 완료")
predict_price("KRW-BTC")
schedule.every().hour.do(lambda: predict_price("KRW-BTC"))

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        schedule.run_pending()

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.1)
            current_price = get_current_price("KRW-BTC")
            balance = data
            if target_price < current_price and current_price < predicted_close_price:
                if balance["krw"] > 5000:
                    print("buy_start")
                    buy_market_order(ticker="KRW-BTC", price=balance["krw"]*0.9995)
        else:
            if balance["btc"] > 0.00008:
                print("sell_start")
                sell_market_order("KRW-BTC", balance["btc"]*0.9995)
                print(sell_market_order("KRW-BTC", balance["btc"]*0.9995))
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)