#!/usr/bin/python2.7

import numpy
import calendar
from datetime import datetime
from collections import namedtuple
from sklearn import svm
import time


def load_data(known_categories, category_text_labels):
    # dtype = [('date', 'S20'),('category', 'S20'),('description', 'S100'),
    #          ('day', 'S11'),('pd_district', 'S20'),('resolution', 'S50'),
    #          ('address', 'S50'),('x', 'f10'),('y', 'f10')]

    dtype = [('date', 'S20'), ('category', 'S30'),
             ('day', 'S11'), ('pd_district', 'S20'),
             ('address', 'S50'), ('x', 'f10'), ('y', 'f10')]
    epoch_date = datetime(1970,1,1)
    datetime_converter = lambda x: (datetime.strptime(x, '%Y-%m-%d %H:%M:%S') - epoch_date).total_seconds()
    lowercase_converter = lambda x: x.lower()

    if known_categories:
        category_converter = lambda x: category_text_labels.index(x.lower())
    else:
        category_converter = lowercase_converter

    # convert day names to uppercase so we can do comparison against data
    lowercase_days = [day.lower() for day in calendar.day_name]
    day_converter = lambda x: lowercase_days.index(x.lower())

    crime_data = namedtuple('crime_data', ['date', 'category', 'category_text_labels',
                                           'day', 'district', 'district_text_labels',
                                           'address', 'address_text_labels', 'x', 'y'])
    crime_data.date, crime_data.category, crime_data.day, crime_data.district, crime_data.address, crime_data.x, crime_data.y \
        = numpy.loadtxt('train.csv', dtype, delimiter=',',
                        converters={0: datetime_converter, 1: category_converter,
                                    3: day_converter, 4: lowercase_converter,
                                    6: lowercase_converter},
                        skiprows=1, usecols=(0, 1, 3, 4, 6, 7, 8), unpack=True)

    # TODO: clean this up
    if not known_categories:
        # get the unique categories of crime to use as class labels
        crime_data.category_text_labels = list(set(crime_data.category))
        crime_data.category = [crime_data.category_text_labels.index(cat) for cat in crime_data.category]

    crime_data.district_text_labels = list(set(crime_data.district))
    crime_data.district = [crime_data.district_text_labels.index(dist) for dist in crime_data.district]

    crime_data.address_text_labels = list(set(crime_data.address))
    crime_data.address = [crime_data.address_text_labels.index(addr) for addr in crime_data.address]

    return crime_data

def train(crime_data):
    start = time.time()

    print "Creating feature matrix..."
    features = numpy.column_stack((crime_data.date, crime_data.day, crime_data.district,
                                   crime_data.address, crime_data.x, crime_data.y))
    print "Starting to train SVM..."
    svm_classifier = svm.SVC()
    svm_classifier.fit(features, crime_data.category)

    end = time.time()
    print "Time to fit SVM: " + (end - start) + " seconds."
    return svm_classifier


def main():
    # grabbed this from a previous run of the data
    # TODO: factor known information out, load this from a file
    categories = ['driving under the influence', 'weapon laws', 'recovered vehicle',
                  'secondary codes', 'warrants', 'prostitution', 'drug/narcotic',
                  'embezzlement', 'trespass', 'bribery', 'non-criminal',
                  'disorderly conduct', 'other offenses', 'runaway', 'suicide',
                  'liquor laws', 'vehicle theft', 'sex offenses non forcible',
                  'vandalism', 'gambling', 'sex offenses forcible', 'kidnapping',
                  'family offenses', 'assault', 'larceny/theft', 'burglary',
                  'missing person', 'extortion', 'fraud', 'arson', 'trea',
                  'bad checks', 'loitering', 'stolen property', 'robbery',
                  'forgery/counterfeiting', 'pornography/obscene mat', 'suspicious occ',
                  'drunkenness']

    crime_data = load_data(known_categories=True, category_text_labels=categories)
    svm_classifer = train(crime_data=crime_data)


if __name__ == "__main__":
    main()