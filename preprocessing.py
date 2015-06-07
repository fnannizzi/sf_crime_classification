#!/usr/bin/python

import re
import os
import shutil
import unittest

class Preprocessing:
    # TODO: This is terrible and redundant but got frustrated trying to combine these
    # into one regex, so will come back to this later.
    text_pattern = "([a-zA-Z0-9<>$&\.\(\)/ ]*)";
    match_patterns = [r"\"" + text_pattern + "," + text_pattern + "\"",
                      r"\"" + text_pattern + "," + text_pattern + "," + text_pattern + "\"",
                      r"\"" + text_pattern + "," + text_pattern + "," + text_pattern + 
                      "," + text_pattern + "\"",
                      r"\"" + text_pattern + "," + text_pattern + "," + text_pattern + 
                      "," + text_pattern "," + text_pattern + "\""];
    replace_patterns = [r"\1 \2", r"\1 \2 \3", r"\1 \2 \3 \4", r"\1 \2 \3 \4 \5"];
    num_patterns = len(match_patterns);

    def do_match_and_replace(self, filename):
        for pattern_index in range(0, self.num_patterns):
            self.replace_in_file(filename, 
                                 self.match_patterns[pattern_index], 
                                 self.replace_patterns[pattern_index]);

    # Help from http://stackoverflow.com/questions/1597649/replace-strings-in-files-by-python
    def replace_in_file(self, filename, match_pattern, replace_pattern):
        out_filename = filename + ".tmp";
        with open(filename) as file:
            out_file = open(out_filename, 'w');
            for line in file:
                out_file.write(re.sub(match_pattern, replace_pattern, line));
            out_file.close();
            os.rename(out_filename, filename);

class TestPreprocessing(unittest.TestCase):

    

