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
    data = numpy.loadtxt('train.csv', dtype, delimiter=',',
                         converters={0: datetime_converter}, skiprows=1, usecols=(0,1,3,4,6,7,8))

    # quick test to make sure this works
    print data[0:3]


load_data()