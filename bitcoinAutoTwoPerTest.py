
krw = 90
coin = 1000
trades_price = 12000
current_price = 9000
target_price = 10000

def buy_market_order(krw):
    """
    Buy market order
    :param krw: int
    :return:
    """
    try:
        if krw > 5000:
            coin = current_price / krw
            print("coin: ", str(coin))
    except Exception as e:
        print(e)

def sell_market_order(coin):
    """
    Sell market order
    :param coin: float
    :return:
    """
    krw = int(current_price * coin)
    print(krw)

if target_price < current_price:
    if krw > 5000:
        buy_result = buy_market_order(krw * 0.9995)
        print("매수")
    elif current_price > trades_price + (trades_price * 0.02) and coin > 0.00008:
        sell_result = sell_market_order(coin * 0.9995)
        print("이익 매도")
elif current_price < trades_price - (trades_price * 0.03) and coin > 0.00008:
    sell_result = sell_market_order(coin * 0.9995)
    print("손절")