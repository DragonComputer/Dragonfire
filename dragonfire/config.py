#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: config
    :platform: Unix
    :synopsis: the module that contains the configuration for the API of Dragonfire.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""


class Config():
    """Class that stores the Twitter API and MySQL database connection credentials in class variables.
    """

    # Twitter Credentials
    TWITTER_CONSUMER_KEY = 'CONSUMER_KEY'
    TWITTER_CONSUMER_SECRET = 'CONSUMER_SECRET'
    TWITTER_ACCESS_KEY = 'ACCESS_KEY'
    TWITTER_ACCESS_SECRET = 'ACCESS_SECRET'

    # MySQL Credentials
    MYSQL_HOST = 'MYSQL_HOST'
    MYSQL_DB = 'MYSQL_DB'
    MYSQL_USER = 'MYSQL_USER'
    MYSQL_PASS = 'MYSQL_PASS'
