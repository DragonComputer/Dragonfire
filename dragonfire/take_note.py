#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: take_note
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the class related to Dragonfire's taking notes ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from os.path import expanduser  # Imported to get the home directory
from dragonfire.config import Config  # Credentials for the database connection
from dragonfire.database import NotePad  # Submodule of Dragonfire module that contains the database schema
from sqlalchemy.orm.exc import NoResultFound  # the Python SQL toolkit and Object Relational Mapper


class NoteTaker():
    """Class to provide the taking note ability.
    """

    def __init__(self):
        """Initialization method of :class:`dragonfire.take_note.NoteTaker` class.
        """

        home = expanduser("~")  # Get the home directory of the user
        self.db = TinyDB(home + '/.dragonfire_db.json')  # This is where we store the database; /home/USERNAME/.dragonfire_db.json
        self.is_server = False
        self.db_session = None

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
                return

            if is_todolist:
                result = self.db.search((Query().is_todolist == is_todolist) & (Query().list_name == list_name))
                if not result:
                    return "*#$"  # for the recursive compare
                answer = ""
                for row in result:
                    answer += "item " + str(row['list_sequence']) + ": " + row['note'] + ". \n"
                return answer

                return

            result = self.db.search((Query().is_todolist == is_todolist) & (Query().is_reminder == is_reminder))
            if not result:
                return "There is no note"

            counter = 0
            answer = ""
            for row in result:
                counter += 1
                answer += "note " + str(counter) + ": " + row['note'] + ". \n"
            return answer



            # result = self.db.search(Query().note == note)  # make a database search by giving note string
            # if result:  # if there is a result
            #     answer = note  # the answer we will return
            #     return self.mirror(answer)  # mirror the answer (for example: I'M to YOU ARE)
            # else:
            #     return None  # if there is no result return None

    def db_upsert(self, note, category=None, remind_time=None, list_name=None, list_sequence=None, is_todolist=False, is_reminder=False, is_public=True, user_id=None):
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
                                                            NotePad.remind_time == remind_time).one_or_none()
            if not notepad:
                new_notepad = NotePad(note=note, is_todolist=is_todolist, list_name=list_name,
                                      list_sequence=list_sequence, is_reminder=is_reminder,
                                      user_id=user_id, is_public=is_public, category=category, remind_time=remind_time)
                self.db_session.add(new_notepad)
                self.db_session.commit()
            else:
                notepad.counter += 1
                self.db_session.commit()
        else:
            if not self.db.search((Query().note == note)):  # if there is no exacty record on the database then
                self.db.insert({
                    'note': note,
                    'category': category,
                    'is_reminder': is_reminder,
                    'list_name': list_name,
                    'is_todolist': is_todolist,
                    'remind_time': remind_time,
                    'list_sequence': list_sequence
                })  # insert the given data
        return ""
        # return "OK, I get it. " + self.mirror(com)# mirror the command(user's speech) and return it to say

    def db_delete(self, note, is_reminder, is_public=True, user_id=None):
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
            if self.db.remove(Query().note == self.fix_pronoun(note)):
                return "OK, I forgot everything I know about " + self.mirror(note)
            else:
                return "I don't remember anything about " + self.mirror(note)

    #   THIS CODE WILL BE DELETED
    # def mirror(self, answer):
    #     """Function to mirror the answer (for example: I'M to YOU ARE).
    #
    #     Args:
    #         answer (str):  Prepared answer that just before the actual return of :func:`respond` method.
    #
    #     Returns:
    #         str:  Response.
    #     """
    #
    #     result = []
    #     types = []
    #     types.append("")
    #     doc = self.nlp(answer)
    #     for token in doc:
    #         types.append(token.lemma_)
    #         if token.lemma_ == "-PRON-":  # if it's a pronoun, mirror it
    #             if token.text.upper() in self.pronouns:
    #                 result.append(self.pronouns[token.text.upper()].lower().strip())
    #                 continue
    #             if token.text.upper() in self.inv_pronouns:
    #                 result.append(self.inv_pronouns[token.text.upper()].lower().strip())
    #                 continue
    #         if (token.lemma_ == "be" or token.dep_ == "aux") and types[-2] == "-PRON-":  # if it's an auxiliary that comes right after a pronoun, mirror it
    #             if token.text.upper() in self.auxiliaries:
    #                 result.append(self.auxiliaries[token.text.upper()].lower().strip())
    #                 continue
    #             if token.text.upper() in self.inv_auxiliaries:
    #                 result.append(self.inv_auxiliaries[token.text.upper()].lower().strip())
    #                 continue
    #         result.append(token.text.strip())
    #     for i in range(len(result)):
    #         if result[i] == "i":
    #             result[i] = "I"
    #     result = ' '.join(result)  # concatenate the result
    #     return result.replace(" '", "'")  # fix for situations like "I 'AM", "YOU 'LL"