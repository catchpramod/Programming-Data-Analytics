__author__ = 'pbhandari'
import pandas as pd
import numpy as np
import assign5_util as util
import sys
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

def read_data():
    df = pd.read_csv('credit.csv') # Please change this
    assert isinstance(df, pd.DataFrame) # for pycharm code completion
    #print df.head()
    #print df.describe()
    # remove duplicates
    df = df.drop_duplicates()
    # remove rows with dependent variable missing
    df = df.dropna(subset=['TARGET'])
    return df

def missing_imputation_for_numeric(df, numeric_with_na):
    for var in numeric_with_na:
        if "log_" in var or "sqrt_" in var:
            util.process_missing_numeric_no_dummy(df, var)
        else:
            util.process_missing_numeric_with_dummy(df, var)
    return

def select_among_origin_log_sqrt(train):
    vars = train.columns.tolist()
    train_x, train_y = util.split_x_y(train.values)
    from sklearn.ensemble import ExtraTreesClassifier
    clf = ExtraTreesClassifier()
    clf.fit(train_x, train_y)
    #print clf.feature_importances_
    variables_with_importance = tuple(zip( clf.feature_importances_, vars))
    #print variables_with_importance
    variables = []
    i=0
    while i < len(variables_with_importance):
        if i + 2 > len(variables_with_importance)-1:
            variables.append(variables_with_importance[i][1])
            i+=1
        elif variables_with_importance[i+1][1] == "log_" + variables_with_importance[i][1]:
            li = list(variables_with_importance[i: (i+3)])
            variables.append(sorted(li, reverse=True)[0][1])
            i=i+3
        else:
            variables.append(variables_with_importance[i][1])
            i+=1
    return variables

def train_test_keep_some_vars(train, test, variables):
    train_new = train[variables]
    test_new = test[variables]
    return (train_new, test_new)

def variable_selection_model_fitting(train, test, model):
    train_x, train_y = util.split_x_y(train.values)
    test_x, test_y = util.split_x_y(test.values)
    selection_model = LogisticRegression()
    """
    Your code here...
    Your need to do variable select first using RFECV (Recursive Feature Elimination with Cross-value) to select variable. The model you used to select variables should
    be logistic regression (Please do not use SVC since we have a quite large dataset, SVC is very slow)
    After variable selection, you again fit a logistic regression model with selected variables and print the classification report and the accuracy of the model.
    This method has no return values
    """
    rfecv = RFECV(estimator=selection_model, step=1, cv=StratifiedKFold(train_y, 2),
                  scoring='accuracy')
    selector = rfecv.fit(train_x,train_y)
    print("Optimal number of features : %d" % rfecv.n_features_)
    train_x_new = selector.transform(train_x)
    test_x_new = selector.transform(test_x)
    # print train_x_new.shape
    # print test_x_new.shape

    model.fit(train_x_new, train_y)
    # make predictions
    expected = test_y
    predicted = model.predict(test_x_new)
    print "Classification Report: "
    print(metrics.classification_report(expected, predicted))
    print "Confusion Matrix: "
    print(metrics.confusion_matrix(expected, predicted))
    print ("Accuracy: %.3f" % metrics.accuracy_score(expected, predicted))

def main():
    # Step 1. Import data
    df = read_data()
    # Step 2. Explore data
    # 2.1. Get variable names
    col_names = df.columns.tolist()
    # 2.2. Classify variables into numeric, categorical (with strings), and nominal
    numeric,categorical,nominal = util.variable_type(df)

    print "numeric:", numeric # ['ID', 'DerogCnt', 'CollectCnt', 'InqCnt06', 'InqTimeLast', 'InqFinanceCnt24', 'TLTimeFirst', 'TLTimeLast', 'TLCnt03', 'TLCnt12', 'TLCnt24', 'TLCnt', 'TLSum', 'TLMaxSum', 'TLSatCnt', 'TLDel60Cnt', 'TLBadCnt24', 'TL75UtilCnt', 'TL50UtilCnt', 'TLBalHCPct', 'TLSatPct', 'TLDel3060Cnt24', 'TLDel90Cnt24', 'TLDel60CntAll', 'TLOpenPct', 'TLBadDerogCnt', 'TLDel60Cnt24', 'TLOpen24Pct']
    print "categorical:", categorical # no categorical
    print "nominal:", nominal # ['TARGET', 'BanruptcyInd']

    # 2.3. Draw histogram for numeric variables

    # util.draw_histograms(df, ['DerogCnt', 'CollectCnt', 'InqCnt06', 'InqTimeLast', 'InqFinanceCnt24', 'TLTimeFirst', 'TLTimeLast', 'TLCnt03', 'TLCnt12'], 3,3)
    # util.draw_histograms(df, ['TLCnt24', 'TLCnt', 'TLSum', 'TLMaxSum', 'TLSatCnt', 'TLDel60Cnt', 'TLBadCnt24', 'TL75UtilCnt', 'TL50UtilCnt' ], 3,3)
    # util.draw_histograms(df, ['TLBalHCPct', 'TLSatPct', 'TLDel3060Cnt24', 'TLDel90Cnt24', 'TLDel60CntAll', 'TLOpenPct', 'TLBadDerogCnt', 'TLDel60Cnt24', 'TLOpen24Pct'], 3,3)

    # 2.4. Identify variables that have skewed distribution and need to be log or sqrt-transformed
    variables_needs_tranform = ['DerogCnt', 'CollectCnt', 'InqCnt06', 'InqTimeLast', 'InqFinanceCnt24', 'TLTimeFirst', 'TLTimeLast', 'TLCnt03', 'TLCnt12', 'TLCnt24', 'TLCnt', 'TLSum', 'TLMaxSum', 'TLDel60Cnt', 'TLBadCnt24', 'TL75UtilCnt', 'TL50UtilCnt', 'TLBalHCPct', 'TLSatPct', 'TLDel3060Cnt24', 'TLDel90Cnt24', 'TLDel60CntAll', 'TLBadDerogCnt', 'TLDel60Cnt24', 'TLOpen24Pct']
    # 2.5. Draw pie charts for categorical variables

    # util.draw_piecharts(df, [ 'TARGET', 'BanruptcyInd'], 1,2)

    # Step 3. Transform variables
    '''
       your code here...
       You need to do log tranformation and sqrt transformation for the variable in the list variables_needs_tranform.
       Please call the method add_log_transform and add_sqrt_transform you defined in assign5_util.py
    '''
    map(lambda x: util.add_log_transform(df,x), variables_needs_tranform)
    map(lambda x: util.add_sqrt_transform(df,x), variables_needs_tranform)

    # 3.3 Missing value imputation
    numeric,categorical,nominal = util.variable_type(df)
    variables_with_na = util.variables_with_missing(df)
    numeric_with_na = []
    nominal_with_na = []
    '''
    you code here, you need
    1. find numeric variables with missing values and add the variables to the list numeric_with_na
    2. find nominal variable with missing values and add the variables to the list nominal_with_na. In our dataset, we have none.
    '''
    numeric_with_na = [ item for item in numeric if item in variables_with_na ]
    nominal_with_na = [ item for item in nominal if item in variables_with_na ]
    print numeric_with_na
    print nominal_with_na
    missing_imputation_for_numeric(df, numeric_with_na) # do missing value imputation
    # after transformation and missing value imputation, we clean our data. we put the target variable as the last column
    vars = ['DerogCnt', 'log_DerogCnt', 'sqrt_DerogCnt', 'CollectCnt', 'log_CollectCnt', 'sqrt_CollectCnt', 'BanruptcyInd', 'InqCnt06', 'log_InqCnt06', 'sqrt_InqCnt06', 'InqTimeLast', 'log_InqTimeLast', 'sqrt_InqTimeLast', 'InqFinanceCnt24', 'log_InqFinanceCnt24', 'sqrt_InqFinanceCnt24', 'TLTimeFirst', 'log_TLTimeFirst', 'sqrt_TLTimeFirst', 'TLTimeLast', 'log_TLTimeLast', 'sqrt_TLTimeLast', 'TLCnt03', 'log_TLCnt03', 'sqrt_TLCnt03', 'TLCnt12', 'log_TLCnt12', 'sqrt_TLCnt12', 'TLCnt24', 'log_TLCnt24', 'sqrt_TLCnt24', 'TLCnt', 'log_TLCnt', 'sqrt_TLCnt', 'TLSum', 'log_TLSum', 'sqrt_TLSum', 'TLMaxSum', 'log_TLMaxSum', 'sqrt_TLMaxSum', 'TLSatCnt', 'TLDel60Cnt', 'log_TLDel60Cnt', 'sqrt_TLDel60Cnt', 'TLBadCnt24', 'log_TLBadCnt24', 'sqrt_TLBadCnt24', 'TL75UtilCnt', 'log_TL75UtilCnt', 'sqrt_TL75UtilCnt', 'TL50UtilCnt', 'log_TL50UtilCnt', 'sqrt_TL50UtilCnt', 'TLBalHCPct', 'log_TLBalHCPct', 'sqrt_TLBalHCPct', 'TLSatPct', 'log_TLSatPct', 'sqrt_TLSatPct', 'TLDel3060Cnt24', 'log_TLDel3060Cnt24', 'sqrt_TLDel3060Cnt24', 'TLDel90Cnt24', 'log_TLDel90Cnt24', 'sqrt_TLDel90Cnt24', 'TLDel60CntAll', 'log_TLDel60CntAll', 'sqrt_TLDel60CntAll', 'TLOpenPct', 'TLBadDerogCnt', 'log_TLBadDerogCnt', 'sqrt_TLBadDerogCnt', 'TLDel60Cnt24', 'log_TLDel60Cnt24', 'sqrt_TLDel60Cnt24', 'TLOpen24Pct', 'log_TLOpen24Pct', 'sqrt_TLOpen24Pct', 'TLMaxSum_missing', 'TL50UtilCnt_missing', 'TLOpenPct_missing', 'TLBalHCPct_missing', 'TLSum_missing', 'TL75UtilCnt_missing', 'TLSatCnt_missing', 'TLCnt_missing', 'TLSatPct_missing', 'TLOpen24Pct_missing', 'InqTimeLast_missing', 'TARGET']
    df = df[vars]
    # Step 4. Split data into training and test
    train, test = util.split_train_test_frame(df, test_size=.5)
    # Step 5. First round of variable selection - for a variable that has been log and sqrt transformed, we obtained two additional
    # variables log_variable and sqrt_variable. Among the log_variable, sqrt_variable, and the variable itself, we want to select one
    # that is the most important based on tree-based feature selection
    variables = select_among_origin_log_sqrt(train)
    variables.append("TARGET") # we add the target variable to the variable list
    # We filter out the variables that are not selected.
    train_new, test_new = train_test_keep_some_vars(train, test, variables)
    print "Length: ", len(variables)
    # Step 6. Second round variable selection and fit a logistic regression model.
    model = LogisticRegression()
    variable_selection_model_fitting(train_new, test_new, model)
    # Step 7. Model comparison with the model with original variables that have not been log or sqrt transformed.
    print "----------results with original variables -------------------"
    # These are the original variables
    orig_variables =  [ 'BanruptcyInd', 'DerogCnt', 'CollectCnt', 'InqCnt06', 'InqTimeLast', 'InqFinanceCnt24', 'TLTimeFirst', 'TLTimeLast', 'TLCnt03', 'TLCnt12', 'TLCnt24', 'TLCnt', 'TLSum', 'TLMaxSum', 'TLSatCnt', 'TLDel60Cnt', 'TLBadCnt24', 'TL75UtilCnt', 'TL50UtilCnt', 'TLBalHCPct', 'TLSatPct', 'TLDel3060Cnt24', 'TLDel90Cnt24', 'TLDel60CntAll', 'TLOpenPct', 'TLBadDerogCnt', 'TLDel60Cnt24', 'TLOpen24Pct', 'TLMaxSum_missing', 'TL50UtilCnt_missing', 'TLOpenPct_missing', 'TLBalHCPct_missing', 'TLSum_missing', 'TL75UtilCnt_missing', 'TLSatCnt_missing', 'TLCnt_missing', 'TLSatPct_missing', 'TLOpen24Pct_missing', 'InqTimeLast_missing', 'TARGET']
    train_new, test_new= train_test_keep_some_vars(train, test, orig_variables)
    variable_selection_model_fitting(train_new, test_new, model)

if __name__ == "__main__":
    main()










