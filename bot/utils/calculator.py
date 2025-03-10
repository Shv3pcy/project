"""Calculator module for SysBmi_Bot

Contains functions for BMI calculation and number system conversions.

t.me/SysBmi_Bot
"""


def bmi_calc(body_weight, body_height):
    """Calculate Body Mass Index (BMI)
    
    Args:
        body_weight (int): Weight in kilograms
        body_height (float): Height in meters
        
    Returns:
        float: Calculated BMI value rounded to 2 decimal places
    """
    body_height = float(body_height)
    result = body_weight / (body_height**2)
    result = round(result, 2)
    return result


def sys2_10(number):
    """Convert binary number to decimal
    
    Args:
        number (str): Binary number as string
        
    Returns:
        int: Decimal representation of the binary number
    """
    number = str(number)
    result = int(number, 2)
    return result


def sys10_2(number):
    """Convert decimal number to binary
    
    Args:
        number (int): Decimal number
        
    Returns:
        str: Binary representation of the decimal number
    """
    number = int(number)
    result = bin(number)
    return result