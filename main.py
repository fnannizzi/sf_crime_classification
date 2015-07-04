#!/usr/bin/python

import numpy
import calendar
from datetime import datetime


def load_data(known_categories, category_text_labels):
    #dtype = [('date', 'S20'),('category', 'S20'),('description', 'S100'),
    #          ('day', 'S11'),('pd_district', 'S20'),('resolution', 'S50'),
    #          ('address', 'S50'),('x', 'f10'),('y', 'f10')]

    dtype = [('date', 'S20'),('category', 'S30'),
             ('day', 'S11'),('pd_district', 'S20'),
             ('address', 'S50'),('x', 'f10'),('y', 'f10')]
    datetime_converter = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    lowercase_converter = lambda x: x.lower()

    if known_categories:
        category_converter = lambda x: category_text_labels.index(x.lower())
    else:
        category_converter = lowercase_converter

    # convert day names to uppercase so we can do comparison against data
    lowercase_days = [day.lower() for day in calendar.day_name]
    day_converter = lambda x: lowercase_days.index(x.lower())

    date_data,category_data,day_data,district_data,\
    address_data,x_data,y_data = numpy.loadtxt('train.csv', dtype, delimiter=',',
                                               converters={0: datetime_converter, 1: category_converter,
                                                           3: day_converter, 4: lowercase_converter,
                                                           6: lowercase_converter},
                                               skiprows=1, usecols=(0,1,3,4,6,7,8), unpack=True)


    if not known_categories:
        # get the unique categories of crime to use as class labels
        category_text_labels = set(category_data);
        category_data = [category_text_labels.index(cat) for cat in category_data];

    print category_data




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
              'drunkenness'];

load_data(known_categories=True, category_text_labels=categories)