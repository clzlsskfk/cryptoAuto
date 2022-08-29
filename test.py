import pyupbit

import requests

access = "9eoEhq1tzNI2MnGo5B1xG6iVWiSA4bqxgLbnGi5Z"          # 본인 값으로 변경
secret = "WQEaUd2ux1wxRx7QRzaag4iIBv4hWFuQzbNRAsRK"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

myToken = "xoxb-3935319848149-3940742978484-96lBHaXusDfhqKC2cJ1h0bRF"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text})
    print(response)


message = post_message(myToken, "#coin", "할로")

# print(upbit.get_balance("KRW-BTC"))     # KRW-XRP 조회
# print(upbit.get_balance("KRW"))         # 보유 현금 조회
#
# def get_target_price(ticker, k):
#     """변동성 돌파 전략으로 매수 목표가 조회"""
#     df = pyupbit.get_ohlcv(ticker, interval="minute15", count=2)
#     df.to_excel("정보.xlsx")
#     target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
#     return target_price
#
#
# target_price = get_target_price("KRW-BTC", 0.3)
# price = upbit.get_avg_buy_price("BTC")
#
# print(price)
