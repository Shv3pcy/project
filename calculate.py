"""
Модуль для project_bot.py

t.me/SysBmi_Bot
"""


def bmi_calc(body_weight, body_height):
    body_height = float(body_height)
    result = body_weight / (body_height**2)
    result = round(result, 2)
    return result


# x = input()
# y = input()
# z = bmi_calc(x, y)


def sys2_10(number):
    number = str(number)
    result = int(number, 2)
    return result


def sys10_2(number):
    number = int(number)
    result = bin(number)
    return result


# x  = sys2_10('1001')
# y = sys10_2('9')
# z = f'{x}\n{y}'
