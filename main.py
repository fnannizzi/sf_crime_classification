#!/usr/bin/python

import numpy
from datetime import datetime

def load_data():
    #dtype = [('date', 'S20'),('category', 'S20'),('description', 'S100'),
    #          ('day', 'S11'),('pd_district', 'S20'),('resolution', 'S50'),
    #          ('address', 'S50'),('x', 'f10'),('y', 'f10')]

    dtype = [('date', 'S20'),('category', 'S20'),
             ('day', 'S11'),('pd_district', 'S20'),
             ('address', 'S50'),('x', 'f10'),('y', 'f10')]
    datetime_converter = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    date,category,day,pd_district,address,x,y = numpy.loadtxt('train.csv', dtype, delimiter=',',
                                                              converters={0: datetime_converter},
                                                              skiprows=1, usecols=(0,1,3,4,6,7,8), unpack=True)


    # TODO: clean up here
    category = convert_all_to_upper(category)
    day = convert_all_to_upper(day)
    pd_district = convert_all_to_upper(pd_district)
    address = convert_all_to_upper(address)

    # get the unique categories of crime to use as class labels
    category_labels = set(category)
    print category_labels # check to make sure it looks reasonable



def convert_all_to_upper(string_list):
    return [x.upper() for x in string_list]




load_data()