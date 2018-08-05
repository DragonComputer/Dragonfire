#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: arithmetic
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that provides basic methods to evaluate the algebraic expressions.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""


def text2int(textnum, numwords={}):
    """Function that converts number descriptions written in English to integer.

    Args:
        textnum (str):  Number despcription written in English.

    Keyword Args:
        numwords (dict): Dictionary that maps words to numbers.

    Returns:
        int: Integer version of given number description in string format.
    """

    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def arithmetic_parse(com):
    """Method to evaluate the algebraic expressions written in English.

    Args:
        com (str):  User's command.

    Returns:
        str: Result of the given algebraic expression.
    """

    if not any(e in com.upper() for e in ['+', '-', '/', '*', '^', '=', 'x', 'y', 'z', 'PLUS', 'MINUS', 'DIVIDED BY', 'MULTIPLIED BY', 'TIMES', 'TO THE POWER OF', 'EQUAL']):
        return False
    com = com.lower()
    numwords = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",

        "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",

        "hundred", "thousand", "million", "billion", "trillion",

        "and"
    ]

    operators = {
        'plus': '+',
        'minus': '-',
        'divided_by': '/',
        'multiplied_by': '*',
        'times': '*',
        'to_the_power_of': '^',
        'equal': '='
    }

    com = com.replace("?", "")
    com = com.replace("divided by", "divided_by")
    com = com.replace("multiplied by", "multiplied_by")
    com = com.replace("to the power of", "to_the_power_of")
    words = com.split()
    stash = []
    expression = []
    for i in range(len(words)):
        word = words.pop(0)
        if stash and (word not in numwords):
            expression.append(str(text2int(' '.join(stash))))
            stash = []
        if word in numwords:
            stash.append(word)
        elif word in operators:
            expression.append(operators[word])
        elif word in ['+', '-', '/', '*', '^', '(', ')'] or word.isdigit():
            expression.append(word)
        elif word == '=' or 'equal' in word:
            break
    if stash:
        expression.append(str(text2int(' '.join(stash))))
        stash = []

    try:
        return ' '.join(expression) + ' = ' + str(eval(''.join(expression)))
    except ZeroDivisionError:
        return "Sorry, but that does not make sense as the divisor cannot be zero."
    except:
        return False
