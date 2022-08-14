import pyupbit
import numpy as np



def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-BTC", interval="60minute", count= 7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['fee_Buy'] = df['target'] * 0.0025
    df['fee_Cell'] = df['close'] * 0.0025
    df['ror'] = np.where(df['high'] > df['target'] + df['fee_Buy'],
                     (df['close'] - df['fee_Cell']) / df['target'],
                     1)

    ror = df['ror'].cumprod()[-2]

    return ror

listRorK = {}

for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))
    listRorK[float('%.1f'%k)] = ror

# print("--------------------------------")
print("수익률 이라죠 %.1f %f" % (max(listRorK, key=listRorK.get), max(listRorK.values())))