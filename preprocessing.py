#!/usr/bin/python

import re
import os
import shutil
import unittest

class Preprocessing:
    # TODO: This is terrible and redundant but got frustrated trying to combine these
    # into one regex, so will come back to this later.
    text_pattern = ["([a-zA-Z0-9<>$&;\.\(\)/\- ]+)",
                    "([a-zA-Z0-9<>$&;\.\(\)/\-, ]+)"]
    match_pattern = [r"\"" + text_pattern[0] + "," + text_pattern[1] + "\"",
                     r"\"" + text_pattern[0] + "," + text_pattern[0] + "\""]
    replace_pattern = r'"\1 \2"'
    max_num_commas = 4

    def do_match_and_replace(self, filename):
        for pattern_index in range(0, self.max_num_commas):
            self.replace_in_file(filename, 
                                 self.match_pattern[0],
                                 self.replace_pattern)
        self.replace_in_file(filename,
                             self.match_pattern[1],
                             self.replace_pattern)

    # Help from http://stackoverflow.com/questions/1597649/replace-strings-in-files-by-python
    @staticmethod
    def replace_in_file(filename, match_pattern, replace_pattern):
        out_filename = filename + ".tmp"
        with open(filename) as in_file:
            out_file = open(out_filename, 'w')
            for line in in_file:
                out_file.write(re.sub(match_pattern, replace_pattern, line))
            out_file.close()
            os.rename(out_filename, filename)

class TestPreprocessing(unittest.TestCase):

    def test_match_and_replace(self):
        # copy existing testfile so we don't overwrite it
        shutil.copyfile("unit_test_data/comma_replace_data_test.csv", 
                        "unit_test_data/comma_replace_data_test_preprocessed.csv")

        preprocessing = Preprocessing()
        preprocessing.do_match_and_replace("unit_test_data/comma_replace_data_test_preprocessed.csv")
        
        post_lines = self.get_lines_from_file("unit_test_data/comma_replace_data_test_preprocessed.csv")
        gold_lines = self.get_lines_from_file("unit_test_data/comma_replace_data_gold.csv")
        # loop isn't necessary but makes reading failures much easier
        for line_index in range(0, len(gold_lines)):
            self.assertEqual(gold_lines[line_index], post_lines[line_index])


    def get_lines_from_file(self, filename):
        with open(filename) as in_file:
            lines = in_file.readlines()
        return lines


