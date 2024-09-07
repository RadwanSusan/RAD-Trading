# src\RAD_trading\utils\math_utils.py
def round_to_pip(price, pip_size):
    return round(price / pip_size) * pip_size
