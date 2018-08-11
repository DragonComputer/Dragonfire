# -*- coding: utf-8 -*-

"""
.. module:: test_arithmetic
    :platform: Unix
    :synopsis: tests for the arithmetic submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from dragonfire.arithmetic import arithmetic_parse, text2int

import pytest


def test_text2int():
    assert text2int("seven billion one hundred million thirty one thousand three hundred thirty seven") == 7100031337


@pytest.mark.parametrize("command, response", [
    ("How much is 12 + 14?", "12 + 14 = 26"),
    ("How much is twelve thousand three hundred four plus two hundred fifty six?", "12304 + 256 = 12560"),
    ("What is five hundred eighty nine times six?", "589 * 6 = 3534"),
    ("What is five hundred eighty nine divided by 89?", "589 / 89 = 6.617977528089888"),
    ("What is seven billion five million and four thousand three hundred and four plus five million and four thousand three hundred and four?", "7005004304 + 5004304 = 7010008608"),
    ("How much is 16 - 23?", "16 - 23 = -7"),
    ("How much is 144 * 12?", "144 * 12 = 1728"),
    ("How much is 23 / 0?", "Sorry, but that does not make sense as the divisor cannot be zero."),
    ("How much is 12 + ( 14 * 3 )?", "12 + ( 14 * 3 ) = 54"),
    ("How much is 12 + ( 14 *  )?", False)
])
def test_arithmetic_parse(command, response):
    assert arithmetic_parse(command) == response
