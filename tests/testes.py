import re

def is_valid_stock_name(stock_name):
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, stock_name))

# Exemplo de uso
stock_name = "aapl"
if is_valid_stock_name(stock_name):
    print(f"{stock_name} é um nome de stock válido.")
else:
    print(f"{stock_name} não é um nome de stock válido.")
