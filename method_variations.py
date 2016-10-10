#!/usr/bin/python2.7

import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

def create_feature_matrix(crime_data):
    print "Creating feature matrix..."
    features = numpy.column_stack((crime_data.date, crime_data.day, crime_data.district,
                                   crime_data.address, crime_data.x, crime_data.y))
    return features

# used this to adjust the number of rows included when diagnosing slow running time
def create_feature_matrix_debug(crime_data, rows):
    print "Creating feature matrix with subset of rows 0: " + rows + "..."
    features = numpy.column_stack((crime_data.date[0:rows], crime_data.day[0:rows], crime_data.district[0:rows],
                                   crime_data.address[0:rows], crime_data.x[0:rows], crime_data.y[0:rows]))
    return features

def create_rf(self, features, labels):
    rf = RandomForestClassifier(n_estimators=100)
    print "Fitting rf..."
    rf.fit(features, labels)
    joblib.dump(rf, 'saved_model/random_forest_model.pkl')
    return rf

def use_random_forest(features, labels, test_set, category_text_labels):
    # print "Setting up rf..."
    # rf = create_rf(features, labels)
    print "Loading saved model..."
    rf = joblib.load('saved_model/random_forest_model.pkl')
    # this is just to test that making a prediction works
    print "Making a prediction..."
    predictions = rf.predict_proba(test_set)
    # Test the random forest by classifying crimes from the same 
    # data we used to train. The score should be high (0.9) if 
    # everything is working correctly.
    score = rf.score(features[0:10, :], labels[0:10])
    print "The classification score is: ", score
    #write_predictions_to_file(predictions, category_text_labels, "data/predictions.csv")

def write_predictions_to_file(predictions, category_text_labels, filename):
    with open(filename, 'w') as predictions_file:
        predictions_file.write("Id")
        for label in category_text_labels:
            predictions_file.write(",%s" % label)
        predictions_file.write('\n')

    numpy.savetxt('data/output.csv', predictions, delimiter=',', fmt='%f')
