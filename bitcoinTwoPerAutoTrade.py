# coding=utf-8
import time
import pyupbit
import datetime
import requests
import schedule

myToken = "xoxb-3935319848149-3940742978484-J9c0BduoMpbZNN3dFymdR15O"
slack_channel = "#coin"

access = "9eoEhq1tzNI2MnGo5B1xG6iVWiSA4bqxgLbnGi5Z"
secret = "WQEaUd2ux1wxRx7QRzaag4iIBv4hWFuQzbNRAsRK"


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text})
    print(response)


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute15", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


def get_trades_price(ticker):
    return upbit.get_avg_buy_price(ticker)


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 시작 메세지 슬랙 전송
post_message(myToken, slack_channel, "자동 2% 이익실현 autotrade start")
schedule.every().hour.do(lambda: post_message(myToken, slack_channel, "프로그램 실행 중"))

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")  # 09:00
        end_time = start_time + datetime.timedelta(days=1)  # 09:00 + 1일

        # 09:00 < 현재 < 08:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)
            current_price = get_current_price("KRW-BTC")
            trades_price = get_trades_price("BTC")
            if target_price < current_price:
                krw = get_balance("KRW")
                btc = get_balance("BTC")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-BTC", krw * 0.9995)
                    post_message(myToken, slack_channel, slack_channel, "BTC buy : " + str(buy_result))
                    print("매도")
                elif current_price > trades_price + (trades_price * 0.02) and btc > 0.00008:
                    sell_result = upbit.sell_market_order("KRW-BTC", btc * 0.9995)
                    post_message(myToken, slack_channel, slack_channel, "BTC cell(수익) : " + str(sell_result))
                    print("이익 매수")
                elif current_price < trades_price - (trades_price * 0.03) and btc > 0.00008:
                    sell_result = upbit.sell_market_order("KRW-BTC", btc * 0.9995)
                    post_message(myToken, slack_channel, slack_channel, "BTC cell(손절) : " + str(sell_result))
                    print("손절")
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken, slack_channel, slack_channel, e)
        time.sleep(1)