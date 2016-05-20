import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn import linear_model, svm, cross_validation
from sklearn import tree
from sklearn.metrics import confusion_matrix


# load data return 2d array
from sklearn.metrics import classification_report
from sklearn.metrics.metrics import accuracy_score


def load_data(filename):
    df = pd.read_csv(filename)
    arr = df.values
    # print arr[:,:arr.shape[1]-1]
    # print arr[:,arr.shape[1]-1:]
    # print arr[-1:]
    return arr


# Split data into training and test (validation). The default size of test data is 0.3.
# return train_X (a 2d array that includes the independent variable values), train_y (a 1d array that includes the dependent
# variable values), and similarly test_X and test_Y
def split_train_test(arr, test_size = 0.3):
    train_X,test_X,train_y, test_y =  train_test_split(arr[:,:arr.shape[1]-1], arr[:,arr.shape[1]-1:], test_size=test_size)
    print "Training dimensions: "
    print train_X.shape
    print train_y.shape
    print "Testing dimensions: "
    print test_X.shape
    print test_y.shape
    return train_X,train_y, test_X, test_y

#Fitting logistic regression model using training data and test data
def fit_logistic(train_X, train_y, test_X, test_y):
    logreg = linear_model.LogisticRegression()
    logreg = logreg.fit(train_X, train_y.flat)
    pred_y = logreg.predict(test_X)

    # print classification reports
    # print accuracy
    # The format should be

    print classification_report(test_y, pred_y)
    print accuracy_score(test_y,pred_y)

    """
    Classification Report:
             precision    recall  f1-score   support

        0.0       0.80      0.89      0.85      4932
        1.0       0.75      0.60      0.67      2676

    avg / total       0.78      0.79      0.78      7608

    Accuracy: 0.788512092534"""
    # don't worry about the values. Random sampling may lead to different varlue
    show_confusion_matrix(test_y,pred_y)
    return pred_y # predicted y values

# fit logistic regression with cross-validation. This function takes a 2d array as an input. You need to first split it
# into train_x and train_y, and then do cross validation. This function does not return anything
def fit_logistic_cv(arr, cv=5):
    # print accuracy, precision, recall and f1
    # format should be
    ''' output:
    accuracy: 0.7901
    precision: 0.7598
    recall: 0.5894
    f1: 0.6637
    '''
    train_X = arr[:,:arr.shape[1]-1]
    train_y = arr[:,arr.shape[1]-1:].flat
    regr = linear_model.LogisticRegression()
    accuracy = cross_validation.cross_val_score(regr, train_X, train_y, cv=cv)
    precision = cross_validation.cross_val_score(regr, train_X, train_y, cv=cv, scoring='precision')
    recall = cross_validation.cross_val_score(regr, train_X, train_y, cv=cv, scoring='recall')
    f1 = cross_validation.cross_val_score(regr, train_X, train_y, cv=cv, scoring='f1')
    print "ouptut: "
    print "accuracy: " , (accuracy.mean())
    print "precision: " , (precision.mean())
    print "recall: " , (recall.mean())
    print "f1: " , (f1.mean())






# this function takes predicted y values and actual y values in the test data as inputs. It does not return anything
def show_confusion_matrix(test_y, pred_y):
    # first print confusion matrix
    # Show confusion matrix graph in a separate window


    # Compute confusion matrix
    cm = confusion_matrix(test_y,pred_y)

    print(cm)

    # Show confusion matrix in a separate window
    plt.matshow(cm)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    return

#Fitting decision tree model using training data and test data
def fit_decision_tree(train_X, train_y, test_X, test_y):
    # print classification reports
    # print accuracy
    # The format should be
    """
    Classification Report:
             precision    recall  f1-score   support

        0.0       0.80      0.89      0.85      4932
        1.0       0.75      0.60      0.67      2676

    avg / total       0.78      0.79      0.78      7608

    Accuracy: 0.788512092534"""
    dtc = tree.DecisionTreeClassifier()
    dtc = dtc.fit(train_X,train_y.flat)
    pred_y = dtc.predict(test_X)

    print classification_report(test_y, pred_y)
    print accuracy_score(test_y,pred_y)


    # create the graph - Here you just need to create the dot file. Please uncomment my code below

    from sklearn.externals.six import StringIO
    f = open('tre.dot','w')
    tree.export_graphviz(dtc, out_file=f) # please change your_tree_model_fit with the variable you used above
    f.close()

# use the function below to test your fit_logistic_train_test
def test_logistic_train_test():
    data_filename = "magic04.csv"
    train_X, train_y, test_X, test_y = split_train_test(load_data(data_filename),test_size =0.4)
    fit_logistic(train_X, train_y, test_X, test_y)
    '''
    Classification Report:
             precision    recall  f1-score   support

        0.0       0.80      0.89      0.85      4932
        1.0       0.75      0.60      0.67      2676

    avg / total       0.78      0.79      0.78      7608

    Accuracy: 0.788512092534
    '''

# use the function below to test your fit_logistic_cv
def test_logistic_cv():
    data_filename = "magic04.csv"
    fit_logistic_cv(load_data(data_filename))
    ''' output:
    accuracy: 0.7901
    precision: 0.7598
    recall: 0.5894
    f1: 0.6637
    '''

# use the function below to test your fit_decision_tree
def test_decision_tree():
    data_filename = "magic04.csv"
    train_X, train_y, test_X, test_y = split_train_test(load_data(data_filename))
    fit_decision_tree(train_X,train_y,test_X,test_y)
    """
    Classification Report:
             precision    recall  f1-score   support

        0.0       0.85      0.86      0.85      3662
        1.0       0.75      0.72      0.73      2044

    avg / total       0.81      0.81      0.81      5706

    Accuracy: 0.811777076761
    """

def main():
    # test_logistic_train_test()
    # test_logistic_cv()
    test_decision_tree()

if __name__ == '__main__':
    main()
"""def model_fit_linear(algorii)
regr = linear_model.LinearRegression()
# Train the model using the training sets
regr.fit(train_X, train_y)

# <headingcell level=2>

# 6. Making prediction using test data and getting evaluation measures

# <codecell>

# The coefficients
print 'Coefficients: \n', regr.coef_
pred_y = regr.predict(test_X) # your predicted y values

# The root mean square error
mse = np.mean( (pred_y - test_y) ** 2)
rmse = math.sqrt(mse)
print ("RMSE: %.2f" % rmse)

from sklearn.metrics import r2_score
r2 = r2_score(pred_y, test_y)
print ("R2 value: %.2f" % r2)"""






