import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
import math


def variable_type(df, nominal_level=3):
    categorical, numeric, nominal = [], [], []
    for variable in df.columns.values:
        if np.issubdtype(np.array(df[variable]).dtype, int) or np.issubdtype(np.array(df[variable]).dtype, float):
            if len(np.unique(np.array(df[variable]))) <= nominal_level:
                nominal.append(variable)
            else:
                numeric.append(variable)
        else:
            categorical.append(variable)
    return numeric, categorical, nominal


def draw_histograms(df, variables, n_rows, n_cols):
    # draw histogram for multiple variables
    fig = plt.figure(figsize=(15, 45))
    total_subplots = n_rows * n_cols
    for i in range(0, total_subplots):
        ax = fig.add_subplot(n_rows, n_cols, i+1)
        df[variables[i]].hist(bins=20, ax=ax)
        plt.title('Histogram of ' +variables[i])
        # plt.xlabel(variables[i])
        plt.ylabel('Frequency')

    fig.savefig("histograms.png",bbox_inches='tight',pad_inches=1)
    plt.close(fig)
    # plt.show()


def draw_piecharts(df, variables, n_rows, n_cols):
    fig = plt.figure(figsize=(15, 7))
    total_subplots = n_rows * n_cols
    for i in range(0, total_subplots):
        ax = fig.add_subplot(n_rows, n_cols, i+1)
        df[variables[i]].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title(variables[i])
    fig.savefig("piecharts.png",bbox_inches='tight',pad_inches=1)
    plt.close(fig)
    # plt.show()

def add_log_transform(df, variable, indexplus = 1):
    log_variable = "log_" + variable
    data_list = df[variable].tolist()
    transformed_data = map(lambda x: np.log(x+1), data_list)
    new_index = df.columns.get_loc(variable) + indexplus
    df.insert(new_index, log_variable, transformed_data)


def add_sqrt_transform(df, variable, indexplus = 2):
    sqrt_variable = "sqrt_" + variable
    data_list = df[variable].tolist()
    transformed_data = map(lambda x: np.sqrt(x), data_list)
    new_index = df.columns.get_loc(variable) + indexplus
    df.insert(new_index, sqrt_variable, transformed_data)


# find variables with missing values
def variables_with_missing(df):
    result = []
    col_names = df.columns.tolist()
    for variable in col_names:
        percent = float(sum(df[variable].isnull()))/len(df.index)
        #print variable+":", percent
        if percent != 0:
            result.append(variable)
    return result


def missing_imputation_for_numeric(df, numeric_with_na):
    for var in numeric_with_na:
        if "log_" in var or "sqrt_" in var:
            process_missing_numeric_no_dummy(df, var)
        else:
            process_missing_numeric_with_dummy(df, var)
    return


def process_missing_numeric_with_dummy(df, variable):
    missing_variable = variable + "_missing"
    df[missing_variable] = np.where(df[variable].isnull(),1,0)
    median = df[variable].median()
    df[variable].fillna(median, inplace= True)
    return df


def process_missing_numeric_no_dummy(df, variable):
    median = df[variable].median()
    df[variable].fillna(median, inplace= True)
    return df

def split_train_test_frame(df, test_size=.3):
    from sklearn.cross_validation import train_test_split
    df.reset_index(level=0, inplace=True)
    train, test = train_test_split(df.values, test_size=test_size)
    train_ = df.iloc[train[:,0].astype(int).tolist()]
    test_ = df.iloc[test[:,0].astype(int).tolist()]
    #print train_
    del train_['index']
    del test_['index']
    #train_.to_csv("train.csv")
    #test_.to_csv("test.csv")
    return (train_, test_)


def split_x_y(train):
    train_X = train[:, :-1]
    train_y = train[:, -1]
    return (train_X,train_y)


def select_among_origin_log_sqrt(train):
    vars = train.columns.tolist()
    train_x, train_y = split_x_y(train.values)
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


def model_fit_and_predict(train, test, model, attributes=None):
    train_x, train_y = split_x_y(train.values)
    test_x, test_y = split_x_y(test.values)
    model.fit(train_x, train_y)
    pred_y = model.predict(test_x)
    print "Model Used: \n"
    print model
    print 'Classification Report:'
    print(metrics.classification_report(test_y, pred_y))
    print 'Accuracy =', metrics.accuracy_score(test_y, pred_y)


def fit_and_report(x,y,model):
    model.fit(x, y)
    predicted = model.predict(x)
    mse = np.mean((predicted-y)**2)
    rmse = math.sqrt(mse)
    r2 = r2_score(predicted, y)
    print "Model Used: \n"
    print model
    print ("RMSE: %.2f" % rmse)
    print ("R2 value: %.2f" % r2)

def variable_selection_model_fitting(train, test, model, columns):
    train_x, train_y = split_x_y(train.values)
    test_x, test_y = split_x_y(test.values)
    selection_model = LogisticRegression()

    rfecv = RFECV(estimator=model, step=1, cv=StratifiedKFold(train_y, 10),
              scoring='accuracy')
    selector = rfecv.fit(train_x, train_y)
    rfe_features = []
    print rfecv.n_features_
    for col, selected in zip(columns, rfecv.get_support()):
        if selected:
            rfe_features.append(col)
    print rfe_features

    return rfe_features
