import decimal

if float(decimal.Decimal('.1') + decimal.Decimal('.2')) == 0.3:
    print("true")
else:
    print("false")
    print(0.1 + 0.2)

print(float(decimal.Decimal('.1') + decimal.Decimal('.2')))