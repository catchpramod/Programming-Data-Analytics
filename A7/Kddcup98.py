import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression, SGDClassifier,RidgeCV, Ridge
from sklearn import grid_search
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import r2_score
from sklearn.svm import SVR
import math
import utils as util
import sys


def load_data():
    df = pd.read_csv('kddcup98.csv')
    return df

def classification_task(data, target):
    data['TARGET_B'] = target
    var_names = data.columns.tolist()
    print 'Variable Names are:\n', var_names
    numeric, categorical, nominal = util.variable_type(data)
    print 'Numeric Variables:\n', numeric
    print 'Categorical Variables:\n', categorical
    print 'Nominal Variables:\n', nominal

    #clean 'DemMedHomeValue' and 'DemMedIncome'
    data['DemMedHomeValue'] = data['DemMedHomeValue'].replace('[\$,]', '', regex=True).astype(float)
    data['DemMedIncome'] = data['DemMedIncome'].replace('[\$,]', '', regex=True).astype(float)
    numeric, categorical, nominal = util.variable_type(data)

    print "After cleanup\n"
    print 'Numeric Variables:\n', numeric
    print 'Categorical Variables:\n', categorical
    print 'Nominal Variables:\n', nominal

    print "Total Numeric variables: ",len(numeric)
    util.draw_histograms(data, numeric, 11, 2)

    # Replace DemAge with 0 value to np.nan
    data['DemAge']= [ (np.nan if n==0 else n) for n in data['DemAge']]

    skewed_vars = ['GiftCnt36', 'GiftCntAll', 'GiftCntCard36', 'GiftCntCardAll', 'GiftAvgLast', 'GiftAvg36', 'GiftAvgAll', 'GiftAvgCard36', 'PromCntCard12', 'PromCntCard36', 'DemMedHomeValue', 'DemMedIncome']
    util.draw_piecharts(data, categorical, 1, 3)

    #Transform categorical variables

    dummies_StatusCat96NK = pd.get_dummies(data['StatusCat96NK'], prefix='StatusCat96NK')
    dummies_DemGender = pd.get_dummies(data['DemGender'], prefix='DemGender')
    dummies_DemHomeOwner = pd.get_dummies(data['DemHomeOwner'], prefix='DemHomeOwner')
    dummies_StatusCatStarAll = pd.get_dummies(data['StatusCatStarAll'], prefix='StatusCatStarAll')

    cols_to_drop = ['StatusCat96NK', 'DemGender', 'DemHomeOwner', 'StatusCatStarAll']

    map(lambda col: data.drop(col, axis=1, inplace=True), cols_to_drop)
    df = pd.concat([data, dummies_StatusCat96NK, dummies_DemGender, dummies_DemHomeOwner, dummies_StatusCatStarAll], axis=1)
    map(lambda x: util.add_log_transform(df, x), skewed_vars)
    map(lambda x: util.add_sqrt_transform(df, x), skewed_vars)
    numeric, categorical, nominal = util.variable_type(df)
    variables_with_na = util.variables_with_missing(df)
    numeric_with_na = []
    [numeric_with_na.append(n) for n in numeric if n in variables_with_na]
    util.missing_imputation_for_numeric(df, numeric_with_na)
    df.drop('TARGET_B', axis=1, inplace=True)
    return_df = df.copy()

    df['TARGET_B'] = target

    #variables with log/sqrt transformation
    var_ls_trans=[]
    for v in skewed_vars:
        var_ls_trans.append(v)
        var_ls_trans.append("log_"+v)
        var_ls_trans.append("sqrt_"+v)

    #split into train/test
    train, test = util.split_train_test_frame(df, test_size=.4)
    selected_log_sqrt = util.select_among_origin_log_sqrt(train)
    print 'Selected Variables among log and sqrt transformed: \n', selected_log_sqrt

    selected_log_sqrt.append("TARGET_B")
    train_new, test_new = util.train_test_keep_some_vars(train, test, selected_log_sqrt)
    model = LogisticRegression()
    selected_variables = util.variable_selection_model_fitting(train_new, test_new, model, selected_log_sqrt)
    print 'Selected variables after RFECV:\n', selected_variables
    print len(selected_variables)
    print train_new.shape
    train_new, test_new = util.train_test_keep_some_vars(train_new, test_new, selected_variables)
    print train_new.shape
    model = LogisticRegression()
    util.model_fit_and_predict(train_new, test_new, model)

    rfc = RandomForestClassifier()
    max_depth = np.linspace(5, 10, 5)
    n_estimators = [10, 20, 30, 40, 50]
    parameter_grid = [{'n_estimators': n_estimators, 'max_depth': max_depth}]
    train_x, train_y = util.split_x_y(train_new.values)
    model = grid_search.GridSearchCV(rfc, parameter_grid, n_jobs=10, cv=10, scoring='r2')
    model.fit(train_x, train_y)
    model = RandomForestClassifier(n_estimators=model.best_estimator_.n_estimators)
    util.model_fit_and_predict(train_new, test_new, model)

    model = DecisionTreeClassifier()
    util.model_fit_and_predict(train_new, test_new, model)

    return return_df

def regression_task(data,target):
    data['TARGET_D']=target
    data = data.dropna(subset=['TARGET_D'])

    selected_log_sqrt = util.select_among_origin_log_sqrt(data)
    print 'Selected Variables among log and sqrt transformed: \n', selected_log_sqrt


    data.reset_index(level=0, inplace=True)
    del(data['index'])
    selected_log_sqrt.append("TARGET_D")
    df_data = data[selected_log_sqrt]

    x, y = util.split_x_y(df_data.values)
    clf = RidgeCV(alphas=[0.1, 1.0, 10.0], cv=100)
    clf.fit(x, y)
    model = Ridge(alpha=clf.alpha_)
    util.fit_and_report(x,y,model)

    model = LinearRegression()
    util.fit_and_report(x,y,model)

    model = SVR(C=1.0, epsilon=0.2)
    util.fit_and_report(x,y,model)

    return

def main():
    df_data = load_data()
    target_b= df_data["TARGET_B"]
    target_d= df_data["TARGET_D"]
    data_no_target = df_data.drop('TARGET_B', 1)
    data_no_target.drop('TARGET_D', 1, inplace=True)
    cleaned_df = classification_task(data_no_target, target_b)
    regression_task(cleaned_df, target_d)

if __name__ == '__main__':
    main()