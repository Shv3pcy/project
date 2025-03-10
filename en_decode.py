"""
Спасибо сообществу StackOverflow за то,
что подогнали фрагменты кода.
Модуль для project_bot.py

t.me/SysBmi_Bot

"""


def decode(bin_txt):
    decode_txt = "".join(
        chr(int(bin_txt[i : i + 8], 2)) for i in range(0, len(bin_txt), 8)
    )
    return decode_txt


def encode(text):
    bin_code = bin(int.from_bytes(text.encode("utf-8", "surrogatepass"), "big"))[2:]
    bin_code = bin_code.zfill(8 * ((len(bin_code) + 7) // 8))
    return bin_code


# x = decode('0110100001100101011011000110110001101111')
# y = encode('hello')
# z = f'input: {x}\noutput: {y}'
