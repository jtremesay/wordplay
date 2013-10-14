#-*- coding: utf-8 -*-

from dictionary import Dictionary

class Wordplay:
    def __init__(self):
        self.dico = Dictionary()

    def __del__(self):
        self.dico.close()


    def open(self, dictionary_path):
        self.dico.open(dictionary_path)


    def close(self):
        self.dico.close()


    def search_words(self, pattern):
        for word in self.dico.search_words(pattern):
            yield word


    def letters_for_three_words(self, word1_begin, word2_begin, word3_begin, word_end_len):
        word1_suffixes = set(self._search_suffixes(word1_begin, word_end_len))
        word2_suffixes = set(self._search_suffixes(word2_begin, word_end_len))
        word3_suffixes = set(self._search_suffixes(word3_begin, word_end_len))

        common_suffixes = word1_suffixes & word2_suffixes & word3_suffixes
        for common_suffix in sorted(common_suffixes):
            yield common_suffix


    def quatro(self, prefix1, suffix1, prefix2, suffix2, middleLength):
        word1_middle = set(self._search_middle(prefix1, suffix1, middleLength))
        word2_middle = set(self._search_middle(prefix2, suffix2, middleLength))

        common_middles = word1_middle & word2_middle
        for common_middle in sorted(common_middles):
            yield common_middle


    def _search_middle(self, prefix, suffix, middleLength):
        for word in self.dico.search_words(prefix + "_" * middleLength + suffix):
            middle = word[len(prefix):-len(suffix)]

            yield middle


    def _search_suffixes(self, word_begin, word_end_len):
        for word in self.dico.search_words(word_begin + "_" * word_end_len):
            suffix = word[-word_end_len:]

            yield suffix

    def search_anagrams(self, word):
        for anagram in self.dico.search_anagrams(word):
            yield anagram
