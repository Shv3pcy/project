"""Encoder/Decoder module for SysBmi_Bot

Contains functions for text encoding and decoding to binary format.

t.me/SysBmi_Bot
"""


def decode(bin_txt):
    """Decode binary text to UTF-8 string
    
    Args:
        bin_txt (str): Binary string to decode
        
    Returns:
        str: Decoded text
    """
    decode_txt = "".join(
        chr(int(bin_txt[i : i + 8], 2)) for i in range(0, len(bin_txt), 8)
    )
    return decode_txt


def encode(text):
    """Encode text to binary format
    
    Args:
        text (str): Text to encode
        
    Returns:
        str: Binary representation of the text
    """
    bin_code = bin(int.from_bytes(text.encode("utf-8", "surrogatepass"), "big"))[2:]
    bin_code = bin_code.zfill(8 * ((len(bin_code) + 7) // 8))
    return bin_code