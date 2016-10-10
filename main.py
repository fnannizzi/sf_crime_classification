#!/usr/bin/python2.7

import numpy
from datetime import datetime
from collections import namedtuple
from calendar import day_name
from method_variations import create_feature_matrix, use_random_forest

def load_data(category_text_labels, district_text_labels, address_text_labels):

    dtype = [('date', 'S20'), ('category', 'S30'),
             ('day', 'S11'), ('pd_district', 'S20'),
             ('address', 'S50'), ('x', 'f10'), ('y', 'f10')]
    epoch_date = datetime(1970,1,1)
    datetime_converter = lambda x: (datetime.strptime(x, '%Y-%m-%d %H:%M:%S') - epoch_date).total_seconds()

    # Random forests require numeric input, so convert data inputs to numeric by
    # making a list of unique inputs and using the index of each input instead.
    # There is a risk of creating false relationships when doing this - i.e. 
    # if Tenderloin = 1 and Central = 2, Central appears to be 2*Tenderloin,
    # which makes no sense.
    category_converter = lambda x: category_text_labels.index(x.lower())
    district_converter = lambda x: district_text_labels.index(x.lower())
    address_converter = lambda x: address_text_labels.index(x.lower())

    # convert day names to lowercase so we can do comparison against data
    lowercase_days = [day.lower() for day in day_name]
    day_converter = lambda x: lowercase_days.index(x.lower())

    crime_data = namedtuple('crime_data', ['date', 'category', 'category_text_labels',
                                           'day', 'district', 'district_text_labels',
                                           'address', 'address_text_labels', 'x', 'y'])
    crime_data.date, crime_data.category, crime_data.day, crime_data.district, \
    crime_data.address, crime_data.x, crime_data.y \
        = numpy.loadtxt('train.csv', dtype, delimiter=',',
                        converters={0: datetime_converter, 1: category_converter,
                                    3: day_converter, 4: district_converter,
                                    6: address_converter},
                        skiprows=1, usecols=(0, 1, 3, 4, 6, 7, 8), unpack=True)

    return crime_data

def read_labels_from_file(labels_file):
    labels_list = []
    line = labels_file.readline()
    num_labels = int(line.split()[1])
    for line_num in range(0, num_labels):
        labels_list.append(labels_file.readline().strip())

    return labels_list

def main():

    district_text_labels = []
    address_text_labels = []
    # read in labels from a text file
    # knowing the possible labels in advance allows us to apply a converter to numbers while reading data
    with open("data/text_labels.csv", 'r') as labels_file:
        category_text_labels = read_labels_from_file(labels_file)
        district_text_labels = read_labels_from_file(labels_file)
        address_text_labels = read_labels_from_file(labels_file)

    crime_data = load_data(category_text_labels, district_text_labels, address_text_labels)
    features = create_feature_matrix(crime_data)

    # Test using first 10 rows of features, a poor test but enough to make sure things aren't imploding
    use_random_forest(features, crime_data.category, features[0:10, :], category_text_labels)


if __name__ == "__main__":
    print "Starting up..." 
    main()
