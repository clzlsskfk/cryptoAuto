import pyupbit

access = "9eoEhq1tzNI2MnGo5B1xG6iVWiSA4bqxgLbnGi5Z"          # 본인 값으로 변경
secret = "WQEaUd2ux1wxRx7QRzaag4iIBv4hWFuQzbNRAsRK"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회