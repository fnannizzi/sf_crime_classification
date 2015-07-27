#!/usr/bin/python

from collections import namedtuple
from numpy import loadtxt
from string_replace_in_file import string_replace_in_file

class PreprocessingCreateLabels:
    def __init__(self):
        self.data = namedtuple('crime_data', ['category', 'district', 'address'])

    def create_and_write_labels(self, data_filename, labels_filename):
        self.load_data(data_filename)
        self.create_label_sets()
        self.write_label_sets_to_file(labels_filename)

    def load_data(self, filename):
        dtype = [('category', 'S30'), ('pd_district', 'S20'), ('address', 'S50')]
        lowercase_converter = lambda x: x.lower()
        converters = {1: lowercase_converter, 4: lowercase_converter,
                      6: lowercase_converter}
        usecols = (1, 4, 6)

        self.data.category, self.data.district, self.data.address = \
            loadtxt(filename, dtype=dtype, delimiter=',',
                    converters=converters, skiprows=1, usecols=usecols, unpack=True)

    @staticmethod
    def make_unique_sorted_list(data):
        new_list = list(set(data))
        new_list.sort()
        return new_list

    def create_label_sets(self):
        # TODO: rewrite this to return labels list, don't need to make these class members
        self.category_text_labels = self.make_unique_sorted_list(self.data.category)
        self.district_text_labels = self.make_unique_sorted_list(self.data.district)
        self.address_text_labels = self.make_unique_sorted_list(self.data.address)

    @staticmethod
    def write_list_to_file(opened_file, string_list, description):
        opened_file.write(description + ' ' + str(len(string_list)) + '\n')
        for s in string_list:
            opened_file.write(s + '\n')

    def write_label_sets_to_file(self, filename):
        with open(filename, 'w') as opened_file:
            self.write_list_to_file(opened_file, self.category_text_labels, 'category')
            self.write_list_to_file(opened_file, self.district_text_labels, 'district')
            self.write_list_to_file(opened_file, self.address_text_labels, 'address')


# Because commas are used as a column delimiter in this dataset, we need to remove commas that appear
# within columns. For instance, the description field often contains commas which are not intended as
# delimiters.
class PreprocessingRemoveCommas:
    text_pattern = ["([a-zA-Z0-9<>$&;\.\(\)/\- ]+)",
                    "([a-zA-Z0-9<>$&;\.\(\)/\-, ]+)"]
    match_pattern = [r"\"" + text_pattern[0] + "," + text_pattern[1] + "\"",
                     r"\"" + text_pattern[0] + "," + text_pattern[0] + "\""]
    replace_pattern = r'"\1 \2"'
    max_num_commas = 4

    def do_match_and_replace(self, filename):
        for pattern_index in range(0, self.max_num_commas):
            string_replace_in_file(filename,
                                   self.match_pattern[0],
                                   self.replace_pattern)
        string_replace_in_file(filename,
                               self.match_pattern[1],
                               self.replace_pattern)

def remove_commas(filename):
    print "Removing commas from " + filename + "..."
    preprocessingRemoveCommas = PreprocessingRemoveCommas()
    preprocessingRemoveCommas.do_match_and_replace(filename)

def extract_label_sets(data_filename, labels_filename):
    print "Extracting label sets from " + data_filename + "..."
    preprocessingCreateLabels = PreprocessingCreateLabels()
    preprocessingCreateLabels.create_and_write_labels(data_filename, labels_filename)

if __name__ == "__main__":
    remove_commas("data/train.csv")
    remove_commas("data/test.csv")
    extract_label_sets("data/train.csv", "data/text_labels.csv")