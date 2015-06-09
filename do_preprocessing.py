#!/usr/bin/python

from preprocessing import Preprocessing

def do_preprocessing(filename="train.csv"):
    print "Beginning preprocessing..."
    preprocessing = Preprocessing()
    preprocessing.do_match_and_replace(filename)
    print "Finished with preprocessing of " + filename + "."

do_preprocessing()