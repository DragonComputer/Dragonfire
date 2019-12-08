#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
.. module:: utilities
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that holds the custom exceptions.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

class WikipediaNoResultsFoundError(Exception):
    def __init__(self, message = "", errors = None):
        super().__init__(message)
        self.errors = errors