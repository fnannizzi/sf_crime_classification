#!/usr/bin/python

import shutil
import unittest
from preprocessing import PreprocessingRemoveCommas

class TestPreprocessingRemoveCommas(unittest.TestCase):
    def test_match_and_replace(self):
        print "Begin unittest for TestPreprocessingRemoveCommas..."
        # copy existing testfile so we don't overwrite it
        shutil.copyfile("unit_test_data/comma_replace_data_test.csv",
                        "unit_test_data/comma_replace_data_test_preprocessed.csv")

        preprocessing = PreprocessingRemoveCommas()
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

if __name__ == "__main__":
    unittest.main()
