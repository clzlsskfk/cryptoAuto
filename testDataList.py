import pyupbit
import numpy as np
import time

df = pyupbit.get_ohlcv_from(ticker="USDT-ETH", interval="minute5", fromDatetime="20220601", to="20220701")

df.to_excel("backData.xlsx")