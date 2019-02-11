#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: takenote
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the classes related to Dragonfire's note taking ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import datetime  # Basic date and time types
from random import choice  # Generate pseudo-random numbers
try:
    import thread  # Low-level threading API (Python 2.7)
except ImportError:
    import _thread as thread  # Low-level threading API (Python 3.x)

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from os.path import expanduser  # Imported to get the home directory
from dragonfire.database import NotePad  # Submodule of Dragonfire module that contains the database schema
from sqlalchemy.orm.exc import NoResultFound  # the Python SQL toolkit and Object Relational Mapper

from dragonfire.reminder import Reminder

reminder = Reminder()


class NoteTaker():
    """Class to provide the taking note ability.
    """

    def __init__(self):
        """Initialization method of :class:`dragonfire.takenote.NoteTaker` class.
        """

        home = expanduser("~")  # Get the home directory of the user
        self.db = TinyDB(home + '/.dragonfire_db.json')  # This is where we store the database; /home/USERNAME/.dragonfire_db.json
        self.is_server = False
        self.db_session = None

    def check_setnote(self, com, doc, h, user_answering, userin, user_prefix):
        """Method to Dragonfire's check set commands for note taking ability.

        Args:
            com (str):          User's command.
            doc:                doc of com from __init__.py
            h:                  doc helper from __init__.py
            user_answering:     User answering state dictionary.
            userin:             :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:        user's preferred titles.
        """

        if h.check_verb_lemma("create") and h.check_lemma("to") and h.check_verb_lemma("do") and h.check_noun_lemma("list"):
            takenote_query = ""
            for token in doc:
                if not (token.lemma_ == "create" or token.lemma_ == "to" or token.lemma_ == "do" or token.lemma_ == "list" or token.is_stop):
                    takenote_query += ' ' + token.text
            takenote_query = takenote_query.strip()
            user_answering['status'] = True
            user_answering['for'] = 'note_taking'
            user_answering['reason'] = 'todo_list'
            if not takenote_query:  # when command come without note.
                return userin.say(choice([
                    "Okay, " + user_prefix + ". What is the name?",
                    "I'm listening for give a name to list, " + user_prefix + ".",
                    "Alright, " + user_prefix + ". Please, say a list name.",
                    "Ready. What is the name of list?",
                    "Say a name for list."
                ]))
            else:  # when command came with note.
                user_answering['todo_list']['name'] = ""
                user_answering['todo_list']['count'] = 1
                user_answering['takenote_query'] = takenote_query

                return userin.say(choice([
                    "1. item receipt. Give a name to the list, " + user_prefix + "."

                ]))
        elif h.check_verb_lemma("remind") and h.check_text("me"):
            takenote_query = ""
            for token in doc:
                if not (token.lemma_ == "remind" or token.lemma_ == "me" or token.is_stop):
                    takenote_query += ' ' + token.text
            takenote_query = takenote_query.strip()
            user_answering['status'] = True
            user_answering['for'] = 'note_taking'
            user_answering['reason'] = 'remind'
            if not takenote_query:  # when command came without note.
                return userin.say(choice([
                    "Understood. what is note?",
                    "Yes! I'm listening the note.",
                    "Alright, " + user_prefix + ". What will I remind?",
                    "Ready to record, " + user_prefix + ". what is the note?",
                    "Okay, " + user_prefix + ". Please enter the note."
                ]))
            else:  # when command came with note.
                user_answering['takenote_query'] = takenote_query
                return userin.say(choice([
                    "It's Okay, " + user_prefix + ". When will I remind?",
                    "Alright. When do you want to remember?",
                    "Alright, " + user_prefix + ". What is the remind time?",
                    "Note taken. Give the remind time.",
                    "I get it, " + user_prefix + ". Please enter the remind time."
                ]))
        elif h.check_verb_lemma("take") and h.check_noun_lemma("note"):
            user_answering['status'] = True
            user_answering['for'] = 'note_taking'
            user_answering['reason'] = 'basic'
            return userin.say(choice([
                "Yes, " + user_prefix + ".",
                "Yes. I'm listening",
                "Alright, " + user_prefix + ".",
                "Ready to record, " + user_prefix + ".",
                "Keep going, " + user_prefix + "."
            ]))
        elif h.check_verb_lemma("note") and h.check_lemma("that"):
            takenote_query = ""
            for token in doc:
                if not (token.lemma_ == "note" or token.lemma_ == "that" or token.is_stop):
                    takenote_query += ' ' + token.text
            takenote_query = takenote_query.strip()
            if not takenote_query:  # when the input does not contain a note
                user_answering['status'] = True
                user_answering['for'] = 'note_taking'
                user_answering['reason'] = 'basic'
                return userin.say(choice([
                    "Yes, " + user_prefix + ".",
                    "Yes. I'm listening",
                    "Alright, " + user_prefix + ".",
                    "Ready to record, " + user_prefix + ".",
                    "Keep going, " + user_prefix + "."
                ]))
            else:
                self.db_upsert(takenote_query)
                user_answering['status'] = False
                return userin.say(choice(["The note taken", "The note was recorded", "I get it"]) + choice([".", ", " + user_prefix + "."]))

        if user_answering['status']:
            if com.startswith("whatever") or com.startswith("give up") or com.startswith("not now") or com.startswith("forget it") or com.startswith("WHATEVER") or com.startswith("GIVE UP") or com.startswith("NOT NOW") or com.startswith("FORGET IT"):  # for writing interrupt while taking notes and creating reminders.
                user_answering['status'] = False
                user_answering.pop('todo_list', None)
                user_answering.pop('takenote_query', None)
                return userin.say(choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([".", ", " + user_prefix + "."]))

            if user_answering['reason'] == 'todo_list':
                if not user_answering['todo_list']['name']:
                    user_answering['todo_list']['name'] = com
                    if not user_answering['takenote_query']:  # keeper compare for the elastic usage.
                        return userin.say("I get it. Enter the 1. item...")
                    else:
                        self.db_upsert(user_answering['takenote_query'], None, None, user_answering['todo_list']['name'], user_answering['todo_list']['count'], True)
                        return userin.say("I get it. Enter the " + str(user_answering['todo_list']['count'] + 1) + ". item...")
                else:
                    if com.startswith("enough") or com.startswith("it is okay") or com.startswith("it is ok") or com.startswith("it's okay") or com.startswith("it's ok") or com.startswith("end") or com.startswith("ENOUGH") or com.startswith("IT IS OKAY") or com.startswith("IT IS OK") or com.startswith("IT'S OKAY") or com.startswith("IT'S OK") or com.startswith("END"):
                        temporary_keeper = user_answering['todo_list']['name']
                        user_answering['status'] = False
                        user_answering.pop('todo_list', None)
                        user_answering.pop('takenote_query', None)

                        return userin.say(choice([
                            "List was recorded", temporary_keeper + " ToDo List generated",
                            "Get it. List ready"
                            ]) + choice([".", ", " + user_prefix + "."]))
                    user_answering['todo_list']['count'] += 1
                    self.db_upsert(com, None, None, user_answering['todo_list']['name'], user_answering['todo_list']['count'], True)

                    return userin.say(choice([
                        "It is Okay. Give " + str(user_answering['todo_list']['count'] + 1) + ". item",
                        "Get it. Give other item", "Okay. Enter other one", "Okay, you can say other",
                        "Get it. Listening for other"
                        ]) + choice([".", ", " + user_prefix + "."]))

            if user_answering['reason'] == 'remind':
                if user_answering['remind_again']:  # for using same reminder on different time.
                    user_answering['remind_again'] = False
                    if com.startswith("yes") and com.endswith("yes") or com.startswith("yep") and com.endswith("yep") or com.startswith("okay") and com.endswith("okay") or h.check_deps_contains("do it"):
                        return userin.say(choice([
                            "It's okay",
                            "Get it", "reminder will repeat", " It has been set again"
                            ]) + choice([", " + user_prefix + ". ", ". "]) + choice([
                                "What is the remind time?",
                                "When do you want to remind?",
                                "Give remind time.",
                                "Say the time"
                                ]))
                    else:
                        user_answering['status'] = False
                        user_answering.pop('takenote_query', None)
                        return userin.say(choice([
                            "As you wish",
                            "I understand",
                            "Alright",
                            "Ready whenever you want",
                            "Get it"
                            ]) + choice([". ", ", " + user_prefix + ". "]))

                if not user_answering['takenote_query']:
                    user_answering['takenote_query'] = com
                    return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice([", " + user_prefix + ". ", ". "]) + choice([
                        "What is the remind time?",
                        "When do you want to remind?",
                        "Give the remind time.",
                        "Say the time"
                        ]))
                else:  # flexible usage is going to be set.
                    if com.startswith("after") or com.endswith("later") or com.startswith("in") or com.startswith(""):
                        if h.check_noun_lemma("minute") or h.check_noun_lemma("minutes"):
                            takenote_query = ""
                            for token in doc:
                                if not (token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "minute" or token.lemma_ == "minutes" or token.is_stop):
                                    takenote_query += ' ' + token.text
                                    mnt = float(takenote_query)
                                    if isinstance(mnt, float):
                                        # timestamp is a kind of second.
                                        time = datetime.datetime.now().timestamp() + mnt * 60
                                        time = int(time / 60)
                                        self.db_upsert(user_answering['takenote_query'], None, time, None, None, False, True, True)
                                        # return userin.say(str(time.strftime("%H:%M")))
                                    else:
                                        return userin.say("Repeat!")
                        elif h.check_noun_lemma("hour") or h.check_noun_lemma("hours"):
                            takenote_query = ""
                            for token in doc:
                                if not (token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "hour" or token.lemma_ == "hours" or token.is_stop):
                                    takenote_query += ' ' + token.text
                                    hr = int(takenote_query)
                                    if isinstance(hr, float):
                                        # timestamp is a kind of second.
                                        time = datetime.datetime.now().timestamp() + hr * 60 * 60
                                        time = int(time / 60)
                                        self.db_upsert(user_answering['takenote_query'], None, time, None, None, False, True, True)
                                        # return userin.say(str(time))
                                    else:
                                        return userin.say("Repeat!")
                        elif h.check_noun_lemma("day") or h.check_noun_lemma("days"):
                            takenote_query = ""
                            for token in doc:
                                if not (token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "day" or token.lemma_ == "days" or token.is_stop):
                                    takenote_query += ' ' + token.text
                                    dy = int(takenote_query)
                                    if isinstance(dy, float):
                                        # timestamp is a kind of second.
                                        time = datetime.datetime.now().timestamp() + dy * 24 * 60 * 60
                                        time = int(time / 60)
                                        self.db_upsert(user_answering['takenote_query'], None, time, None, None, False, True, True)
                                        # return userin.say(str(time))
                                    else:
                                        return userin.say("Repeat!")
                        user_answering['status'] = False
                        user_answering.pop('takenote_query', None)
                        if not user_answering['is_reminder_active']:  # if reminder checker loop not run, start the loop.
                            thread.start_new_thread(reminder.remind, (self, userin, user_prefix, user_answering))
                        return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice([", " + user_prefix + ". ", ". "]) + choice([
                            "Reminder Added.",
                            "I'm waiting to remind.",
                            "I will remind.",
                            "Reminder has been set."
                            ]))
            else:                                      # taking note second compare here.
                user_answering['status'] = False
                self.db_upsert(com)
                return userin.say(choice([
                    "The note Taken",
                    "Alright",
                    "I noted",
                    "Ready whenever you want to get it",
                    "Get it"
                    ]) + choice([".", ", " + user_prefix + ". "]))

        if h.check_lemma("delete") or h.check_verb_lemma("remove"):
            if h.check_lemma("all"):
                if h.check_lemma("over") and h.check_noun_lemma("database"):
                    self.db_delete(None, None, True)
                    return userin.say("notes database cleared")

                if h.check_lemma("note") or h.check_lemma("notes"):
                    self.db_delete()
                    return userin.say("All notes Deleted")

                if (h.check_verb_lemma("do") and h.check_noun_lemma("lists")) or (h.check_verb_lemma("do") and h.check_noun_lemma("list")):
                    self.db_delete(None, None, False, None, None, True)
                    return userin.say("All to do lists deleted")

                if h.check_lemma("reminder") or h.check_lemma("reminders"):
                    self.db_delete(None, None, False, None, None, False, True)
                    return userin.say("All reminders deleted")
        return None


    def check_getnote(self, com, doc, h, user_answering, userin, user_prefix):
        """Method to Dragonfire's check get commands for note taking ability.

        Args:
            com (str):          User's command.
            doc:                doc of com from __init__.py
            h:                  doc helper from __init__.py
            user_answering:     User answering state dictionary.
            userin:             :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:        user's preferred titles.
        """

        if h.check_verb_lemma("say") or h.check_verb_lemma("get") or h.check_verb_lemma("give"):

            if h.check_noun_lemma("note") or h.check_noun_lemma("notes"):
                return userin.say(self.db_get(None, None))

            if h.check_verb_lemma("do") or (h.check_verb_lemma("do") and h.check_noun_lemma("list")):
                takenote_query = ""
                for token in doc:
                    if not (token.lemma_ == "say" or token.lemma_ == "get" or token.lemma_ == "give" or token.lemma_ == "do" or token.lemma_ == "list" or token.lemma_ == "dragonfire" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                if not takenote_query:  # when command come without note.
                    result = self.db_get(None, None, True)
                    if not result:
                        return userin.say("There is no list")
                    return userin.say(choice([
                        "which list",
                        "Alright, say the list name",
                        "Okay, What is the name of list",
                        "List name"
                    ]) + choice(["?", ", " + user_prefix + "?"]))
                else:  # when command came with note.
                    result = self.db_get(None, com, True)
                    if not result:
                        return userin.say(choice([
                            "This name is not exist",
                            "I couldn't find it, say again",
                            "Not found, Repeat",
                            "Not exist, speak again"
                        ]) + choice(["?", ", " + user_prefix + "?"]))
                    else:
                        return userin.say(result)

        if com.startswith("whatever") or com.startswith("give up") or com.startswith("not now") or com.startswith("forget it") or com.startswith("WHATEVER") or com.startswith("GIVE UP") or com.startswith("NOT NOW") or com.startswith("FORGET IT"):  # for writing interrupr while taking notes and creating reminders.
            return userin.say(
                choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice(
                    [". ", ", " + user_prefix + ". "]))

        if (h.check_lemma("give") or h.check_lemma("say") or h.check_lemma("get")) or h.check_verb_lemma("remind"):
            if h.check_noun_lemma("names") or h.check_noun_lemma("them") or not h.check_noun_lemma(""):
                result = self.db_get(None, None, True)
                return userin.say("list of the lists:\n" + result)

        result = self.db_get(None, com, True)
        if not result:
            return userin.say(choice([
                "This name is not exist",
                "I couldn't find it, say again",
                "Not found, Repeat",
                "Not exist, speak again"
            ]) + choice(["?", ", " + user_prefix + "?"]))
        else:
            return userin.say(result)
        return None


    def db_get(self, note, list_name, is_todolist=False, is_reminder=False, is_public=True, user_id=None):
        """Function to get a note record from the database.  NOT COMPLETED.

        Args:
            note (str):  note that pulled from the user's input/command.

        Keyword Args:
            is_reminder (int):  Is it a note for remind? (default: False)
            is_todolist (int):  Ia it a to do list? (default: False)
            is_public (int):    Is it a public record? (non-user specific)
            user_id (int):      User's ID.

        Returns:
            str:  Response.
        """

        if self.is_server:
            try:
                notepad = self.db_session.query(NotePad).filter(NotePad.note == note, NotePad.is_reminder == is_reminder, NotePad.user_id == user_id, NotePad.is_public == is_public).order_by(NotePad.counter.desc()).first()
                answer = notepad.note
                return self.mirror(answer)
            except NoResultFound:
                return None
        else:
            if is_reminder:
                result = self.db.search((Query().is_reminder == is_reminder))
                return result

            if is_todolist:

                if not list_name:               # if user don't remember the list name.
                    result = self.db.search((Query().is_todolist == is_todolist))
                    if not result:
                        return None
                    name_keeper = []
                    for row in result:
                        if row['list_name'] in name_keeper:
                            pass
                        else:
                            name_keeper.append(row['list_name'])
                    response = ""
                    for row in name_keeper:
                        response += row + ",\n"
                    return response

                result = self.db.search((Query().is_todolist == is_todolist) & (Query().list_name == list_name))
                if not result:
                    return None  # for the recursive compare
                answer = ""
                for row in result:
                    answer += "item " + str(row['list_sequence']) + ": " + row['note'] + ". \n"
                return answer

            result = self.db.search((Query().is_todolist == is_todolist) & (Query().is_reminder == is_reminder))
            if not result:
                return "There is no note"

            counter = 0
            answer = ""
            for row in result:
                counter += 1
                answer += "note " + str(counter) + ": " + row['note'] + ". \n"
            return answer

    def db_upsert(self, note, category=None, remind_time_stamp=None, list_name=None, list_sequence=None, is_todolist=False, is_reminder=False, is_active=False, is_public=True, user_id=None):
        """Function to insert(or update) a note record to the database.

        Args:
            note (str):      note that extracted from the user's input/command.
            com (str):          User's command.

        Keyword Args:
            is_reminder (int):  Is it a note for remind? (default: False)
            is_public (int):    Is it a public note? (non-user specific)
            user_id (int):      User's ID.

        Returns:
            str:  Response.
        """

        if self.is_server:
            notepad = self.db_session.query(NotePad).filter(NotePad.note == note, NotePad.is_todolist == is_todolist,
                                                            NotePad.list_name == list_name,
                                                            NotePad.list_sequence == list_sequence,
                                                            NotePad.is_reminder == is_reminder,
                                                            NotePad.user_id == user_id, NotePad.is_public == is_public,
                                                            NotePad.category == category,
                                                            NotePad.remind_time_stamp == remind_time_stamp,
                                                            NotePad.is_active == is_active).one_or_none()
            if not notepad:
                new_notepad = NotePad(note=note, is_todolist=is_todolist, list_name=list_name,
                                      list_sequence=list_sequence, is_reminder=is_reminder,
                                      user_id=user_id, is_public=is_public, category=category, remind_time_stamp=remind_time_stamp, is_active=is_active)
                self.db_session.add(new_notepad)
                self.db_session.commit()
            else:
                notepad.counter += 1
                self.db_session.commit()
        else:
            if (not is_reminder and not is_todolist) or (is_todolist and not is_reminder):
                if not self.db.search((Query().note == note)):  # if there is no exacty record on the database then
                    self.db.insert({
                        'note': note,
                        'category': category,
                        'is_reminder': is_reminder,
                        'list_name': list_name,
                        'is_todolist': is_todolist,
                        'remind_time_stamp': remind_time_stamp,
                        'list_sequence': list_sequence
                    })  # insert the given data
            elif is_reminder and not is_todolist:
                if not self.db.search((Query().note == note)):  # if there is no exact record on the database then
                    pass
                else:
                    while self.db.search((Query().note == note)):
                        self.db.remove((Query().note == note))
                self.db.insert({
                    'note': note,
                    'category': category,
                    'is_reminder': is_reminder,
                    'list_name': list_name,
                    'is_todolist': is_todolist,
                    'remind_time_stamp': remind_time_stamp,
                    'list_sequence': list_sequence,
                    'is_active': is_active
                })  # insert the given data
            else:
                pass     # the note is to do list and reminder both at the same time. This compare will using on future.
            return ""

    def db_delete(self, note=None, category=None, are_all=False, list_name=None, list_sequence=None, is_todolist=False, is_reminder=False, is_active=False, is_public=True, user_id=None):
        """Function to delete a note record from the database.  NOT COMPLETED.

        Args:
            note (str):  note that extracted from the user's input/command.

        Keyword Args:
            is_reminder (int):  Is it a note for remind? (default: False)
            is_public (int):    Is it a public record? (non-user specific)
            user_id (int):      User's ID.

        Returns:
            str: Response.
        """

        if self.is_server:
            if not is_public and user_id:
                notepad = self.db_session.query(NotePad).filter(NotePad.note == note, NotePad.user_id == user_id).one_or_none()
                if not notepad:
                    return "I don't remember anything about " + self.mirror(note)
                else:
                    notepad.delete()
                    self.db_session.commit()
                    return "OK, I forgot everything I know about " + self.mirror(note)
            else:
                return "I cannot forget a general note about " + self.mirror(note)
        else:
            if are_all:
                self.db.remove((Query().is_todolist == is_todolist) | (Query().is_reminder == is_reminder))  #İf added the "to do list for remind" to the future, this line will be reworked.
                return ""
            if self.db.remove((Query().is_todolist == is_todolist) & (Query().is_reminder == is_reminder)):
                return ""
            else:
                return "There is no note."
