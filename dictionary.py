#-*- coding: utf-8 -*-

import sqlite3
from unidecode import unidecode

class Dictionary:
    def __init__(self):
        self.connection = None


    def __del__(self):
        self.close()


    def open(self, path):
        """Opening a dictionary"""
        # Close previous database
        self.close()

        # Opening database
        self.connection = sqlite3.connect(path)

        # Create tables if needed
        cursor_table_exit = self.connection.cursor()
        cursor_table_exit.execute("SELECT COUNT(*) FROM `sqlite_master` WHERE `type`='table' AND `name`='words'")
        if cursor_table_exit.fetchone()[0] == 0:
            cursor_create_table = self.connection.cursor()
            cursor_create_table.execute("CREATE TABLE `words` (`word` TEXT PRIMARY KEY NOT NULL, `anagram`);")
            cursor_create_table.execute("CREATE INDEX `words_anagrams_idx` ON `words`(`anagram`);")
            cursor_create_table.close()
        cursor_table_exit.close()


    def close(self):
        """Closing a dictionary"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None


    def clear(self):
        """Clearing the dictionary"""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM `words`;")
        cursor.close()


    def save(self):
        """Saving the dictionary"""
        self.connection.commit()


    def add_word(self, word):
        """Add a word to the dictionnary"""
        word = self.normalize_word(word)

        cursor = self.connection.cursor()
        cursor.execute("INSERT OR IGNORE INTO `words` (`word`, `anagram`) VALUES (?, ?);", (word, "".join(sorted(word))))
        cursor.close()


    def remove_word(self, word):
        """Remove a word from the dictionary"""
        word = self.normalize_word(word)

        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM `words` WHERE `word` = ?;", (word,))
        cursor.close()


    def word_exits(self, word):
        """Check if a word exists"""
        word = self.normalize_word(word)

        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM `words` WHERE `word` = ?;", (word,))
        word_exits = cursor.fetchone()[0] > 0
        cursor.close()

        return word_exits


    def get_words(self):
        """Iterate over the dictionary"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT `word` FROM `words` ORDER BY `word` ASC;")
        for line in cursor:
            yield line[0]

        cursor.close()


    def search_words(self, pattern):
        """Search words matching a pattern"""

        pattern = self.normalize_word(pattern)

        cursor = self.connection.cursor()
        cursor.execute("SELECT `word` FROM `words` WHERE `word` LIKE ? ORDER BY `word` ASC;", (pattern,))
        for line in cursor:
            yield line[0]

        cursor.close()


    def search_anagrams(self, ref_word):
        """Find anagrams of a word"""
        ref_word = self.normalize_word(ref_word)
        ref_word_ordered = "".join(sorted(ref_word))

        cursor = self.connection.cursor()
        cursor.execute("SELECT `word` FROM `words` WHERE `anagram` = ? ORDER BY `word` ASC;", (ref_word_ordered,))
        for line in cursor:
            yield line[0]

        cursor.close()


    @staticmethod
    def normalize_word(word):
        """Normalize a word (removing accents, lowercasing, etc...)"""
        return unidecode(word).lower()
