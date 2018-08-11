# -*- coding: utf-8 -*-

"""
.. module:: test_stray
    :platform: Unix
    :synopsis: tests for the stray submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from multiprocessing import Process, Event
import time

from dragonfire.stray import SystemTrayExitListenerSet, SystemTrayInit

import pytest


def test_stray():
    e = Event()
    SystemTrayExitListenerSet(e)
    stray_proc = Process(target=SystemTrayInit)
    stray_proc.start()
    time.sleep(3)
    stray_proc.terminate()
    assert True
