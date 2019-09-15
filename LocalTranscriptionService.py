import genericpath
import os
import re
import time
import threading
import sqlite3
from aqt import mw
from .IpaTranscriptionService import GenericTranscriptionService


class LocalTranscriptions(GenericTranscriptionService):
    def __init__(self, text_to_translate_to_ipa: str):
        super().__init__('Local Transcription Service', 'Meu github aqui')
        self.text_to_translate_word_list = re.split(" ", re.sub("[!@#$%^&*(),'‘’.?\":{}|<>]", "", text_to_translate_to_ipa))
        self.remote_db = mw.col.db
        self.remote_cursor = mw.col.db.cursor()
        self.attach_local_db()


    def set_path_local_db(self, use_absolute_path: bool, db_file = 'ipa.db') -> str:
        local_db_file =  db_file
        plugin_dir_name = 'ankitophonetics-master'
        relative_path = '../../addons21/'
        absolute_path = os.path.abspath(relative_path) + '/' + plugin_dir_name + '/' + db_file
        if use_absolute_path:
            return absolute_path
        return relative_path + plugin_dir_name + '/' + db_file

    def attach_local_db(self,):
        local_db_file = (self.set_path_local_db(use_absolute_path=False),)
        query = """ATTACH DATABASE ? AS ipadb;"""
        try:
            self.remote_cursor.execute(query, local_db_file)
        except sqlite3.OperationalError as e:
            print(e)
        
    def translate_to_ipa(self) -> str:
        return self.mount_ipa_sentence()

    def mount_ipa_sentence(self) -> str:
        ipa_sentence = ''
        for word in self.text_to_translate_word_list:
            if ipa_sentence == '':
                try:
                    ipa_sentence = ipa_sentence + "" + self.search_word(word)[0]
                except IndexError:
                    ipa_sentence = ipa_sentence + "" + word
            else:
                try:
                    ipa_sentence = ipa_sentence + " " + self.search_word(word)[0]
                except IndexError:
                    ipa_sentence = ipa_sentence + " " + word
        return ipa_sentence

    def search_word(self, word) -> list:
        query = """SELECT ipa_word FROM ipadb.ipa WHERE english_word=?"""
        self.remote_cursor.execute(query, [word.lower()])
        list_of_ipa_words = []
        for db_word in self.remote_cursor.fetchall():
            list_of_ipa_words.append(re.sub("ɹ", "r", db_word[0]))
        return list_of_ipa_words

    

        

