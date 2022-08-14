import pyupbit
import numpy as np
import bestk

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량을 나타내고, count는 몇일간의 테스트인지 작성
df = pyupbit.get_ohlcv("KRW-ETH", interval="60minute", count=100)

# 일주일간 최고 수익률의 k값 계산
print("Best k = %.1f" % max(bestk.listRorK, key=bestk.listRorK.get))
k = max(bestk.listRorK, key=bestk.listRorK.get)
df['k'] = k

# 15일 이동 평균선 조회
dfMa = pyupbit.get_ohlcv("KRW-ETH", interval="day", count=15)
df['ma15'] = dfMa['close'].rolling(window=15).mean().iloc[-1]

# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * k

# target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

df['fee_Buy'] = df['target'] * 0.0025
df['fee_Cell'] = df['close'] * 0.0025
# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where((df['high'] > df['target'] + df['fee_Buy']) & (df['ma15'] < df['high']),
                     (df['close'] - df['fee_Cell']) / df['target'],
                     1)

# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Drow Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD 계산
print("MDD(%): ", df['dd'].max())

# 엑셀로 출력
df.to_excel("dd.xlsx")