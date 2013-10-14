#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from dictionary import Dictionary
import sys


if len(sys.argv) != 3:
    sys.exit("Usage: generate_dictionary.py <input file> <ouput dictionary>")

with open(sys.argv[1], 'r') as input_file:
    d = Dictionary()
    d.open(sys.argv[2])
    d.clear()

    for word in input_file:
        d.add_word(word.replace("\r", "").replace("\n", ""))

    d.save()
    d.close()