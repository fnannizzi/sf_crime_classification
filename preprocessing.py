#!/usr/bin/python

import re
import os
import shutil
import unittest

class Preprocessing:
    # TODO: This is terrible and redundant but got frustrated trying to combine these
    # into one regex, so will come back to this later.
    text_pattern = "([a-zA-Z0-9<>$&-;\.\(\)/ ]+)";
    match_patterns = [r"\"" + text_pattern + "," + text_pattern + "\"",
                      r"\"" + text_pattern + "," + text_pattern + "," + text_pattern + "\"",
                      r"\"" + text_pattern + "," + text_pattern + "," + text_pattern + 
                        "," + text_pattern + "\"",
                      r"\"" + text_pattern + "," + text_pattern + "," + text_pattern + 
                        "," + text_pattern + "," + text_pattern + "\""];
    replace_patterns = [r"\1 \2", r"\1 \2 \3", r"\1 \2 \3 \4", r"\1 \2 \3 \4 \5"];
    num_patterns = len(match_patterns);

    def do_match_and_replace(self, filename):
        for pattern_index in range((self.num_patterns-1), 0, -1):
            self.replace_in_file(filename, 
                                 self.match_patterns[pattern_index], 
                                 self.replace_patterns[pattern_index]);

    # Help from http://stackoverflow.com/questions/1597649/replace-strings-in-files-by-python
    def replace_in_file(self, filename, match_pattern, replace_pattern):
        out_filename = filename + ".tmp";
        with open(filename) as file:
            out_file = open(out_filename, 'w');
            for line in file:
                print re.sub(match_pattern, replace_pattern, line)
                out_file.write(re.sub(match_pattern, replace_pattern, line));
            out_file.close();
            os.rename(out_filename, filename);

class TestPreprocessing(unittest.TestCase):

    def test_match_and_replace(self):
        # copy existing testfile so we don't overwrite it
        shutil.copyfile("unit_test_data/comma_replace_data_test.csv", 
                        "unit_test_data/comma_replace_data_test_preprocessed.csv");

        preprocessing = Preprocessing();
        preprocessing.do_match_and_replace("unit_test_data/comma_replace_data_test_preprocessed.csv");
        
        postlines = self.get_lines_from_file("unit_test_data/comma_replace_data_test_preprocessed.csv");
        goldlines = self.get_lines_from_file("unit_test_data/comma_replace_data_gold.csv");
        # loop isn't necessary but makes reading failures much easier
        for line_index in range(0, len(goldlines)):
            self.assertEqual(postlines[line_index], goldlines[line_index]);


    def get_lines_from_file(self, filename):
        with open(filename) as file:
            lines = file.readlines();
        return lines;


def do_preprocessing(filename="train.csv"):
    print "Beginning preprocessing...";
    preprocessing = Preprocessing();
    preprocessing.do_match_and_replace(filename);
    print "Finished with preprocessing of " + filename + ".";

