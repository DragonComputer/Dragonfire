#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: takenote
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the classes related to Dragonfire's reminder for taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import datetime  # Basic date and time types
import subprocess  # Subprocess managements
import time  # Time access and conversions
from random import choice  # Generate pseudo-random numbers


class Reminder():
    """Class to contains reminder feature for taking note ability.
    """

    def __init__(self):
        """Initialization method of :class:`dragonfire.reminder.Reminder` class.
        """
        # self.userin = userin

    def check_time(self, now_timestamp, reminde_time_stamp):
        """Method to dragonfire's command structures of searching in youtube ability.

        Args:
            now_timestamp:                     current date.
            reminde_time_stamp:                 reminde date.
        """
        return now_timestamp == reminde_time_stamp

    def remind(self, note_taker, userin, user_prefix, user_answering_note):
        """Method to dragonfire's command structures of searching in youtube ability.
        Keyword Args:
                    note_taker (object):        note_taker class's object.
                    userin:                     :class:`dragonfire.utilities.TextToAction` instance.
                    user_prefix:                user's preferred titles.
                    user_answering_note:       User answering string array.
        """
        while True:
            now_timestamp = int(datetime.datetime.now().timestamp() / 60)
            result = note_taker.db_get(None, None, False, True)
            is_there_active = False
            for row in result:
                if self.check_time(str(now_timestamp), str(row['remind_time_stamp'])):
                    try:
                        subprocess.Popen(["notify-send", "Dragonfire", row['note']])
                    except BaseException:
                        pass
                    user_answering_note['status'] = True
                    user_answering_note['isRemind'] = True
                    user_answering_note['is_again'] = True
                    user_answering_note['note_keeper'] = row['note']

                    note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True, False)

                    userin.say(choice(["You have reminder", "Reminder", "Remind Time"]) + choice([":", ", " + user_prefix + ":"]) + "\n" + row['note'] + ",\n" + choice(["Wanna ", ""]) + choice(["Repeat?", "Suspend?", "See again?"]))
                # else:
                #     userin.say("nothing found to remind ")
                if not is_there_active:
                    if row['is_active']:
                        is_there_active = True
            user_answering_note['is_active'] = is_there_active
            if not is_there_active:   # if there is no active reminder, loop will be interrupted.
                break
            time.sleep(60)
