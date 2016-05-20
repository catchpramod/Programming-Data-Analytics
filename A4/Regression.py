import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
import re

# this function takes the drugcount dataframe as input and output a tuple of 3 data frames: DrugCount_Y1,DrugCount_Y2,DrugCount_Y3
def process_DrugCount(drugcount):
    drugcount['DrugCount'] = drugcount['DrugCount'].map(lambda(rd): int(str.replace(rd, '+', '')))
    DrugCount1 = drugcount[drugcount['Year'] == 'Y1']
    DrugCount2 = drugcount[drugcount['Year'] == 'Y2']
    DrugCount3 = drugcount[drugcount['Year'] == 'Y3']

    return DrugCount1, DrugCount2, DrugCount3

# this function converts strings such as "1- 2 month" to "1_2"
def replaceMonth(string):
    retVal = '_'.join(re.findall('\d+', string))
    return retVal

# this function processes a yearly drug count data
def process_yearly_DrugCount(aframe):
    processed_frame = None
    aframe = aframe.drop('Year', 1)
    aframe['DSFS'] = map(replaceMonth, list(aframe['DSFS']))
    dframe = pd.get_dummies(aframe['DSFS'], prefix='DSFS')
    processed_frame = pd.concat([aframe, dframe], axis=1)
    processed_frame = processed_frame.drop('DSFS',1)
    grouped = processed_frame.groupby('MemberID', as_index=False)
    processed_frame = grouped.aggregate(np.sum)
    processed_frame = processed_frame.rename(columns={'DrugCount': 'Total_DrugCount'})
    return processed_frame


# this is the function to split training dataset to training and test. You don't need to change the function
def split_train_test(arr, test_size=.3):
    train, test = train_test_split(arr, test_size=0.33)
    train_X = train[:, :-1]
    train_y = train[:, -1]
    test_X = test[:,:-1]
    test_y = test[:, -1]
    return (train_X,train_y,test_X,test_y)


# run linear regression. You don't need to change the function
def linear_regression((train_X,train_y,test_X,test_y)):
    regr = linear_model.LinearRegression()
    regr.fit(train_X, train_y)
    print 'Coefficients: \n', regr.coef_
    pred_y = regr.predict(test_X) # your predicted y values
    # The root mean square error
    mse = np.mean( (pred_y - test_y) ** 2)
    import math
    rmse = math.sqrt(mse)
    print ("RMSE: %.2f" % rmse)
    from sklearn.metrics import r2_score
    r2 = r2_score(pred_y, test_y)
    print ("R2 value: %.2f" % r2)


# for a real-valued variable, replace missing with median
def process_missing_numeric(df, variable):
    # below is the code I used in the lecture ("exploratory_analysis.py") for dealing with missing values of the variable "age".
    # You need to change the code below slightly
    df['variable_missing'] = np.where(df['Total_DrugCount'].isnull(), 1, 0)
    # df.insert(len(df.columns)-1,'variable_missing',variable_missing)
    median_DrugCount = df[variable].median()
    df[variable].fillna(median_DrugCount, inplace=True)


# This function prints the ratio of missing values for each variable. You don't need to change the function
def print_missing_variables(df):
    for variable in df.columns.tolist():
        percent = float(sum(df[variable].isnull()))/len(df.index)
        print variable+":", percent


def main():
    # print replaceMonth("1- 2 month")
    # sys.exit()
    pd.options.mode.chained_assignment = None # remove the warning messages regarding chained assignment. 
    daysinhospital = pd.read_csv('DaysInHospital_Y2.csv')
    drugcount = pd.read_csv('DrugCount.csv')
    li = map(process_yearly_DrugCount, process_DrugCount(drugcount))
    DrugCount_Y1_New = li[0]
    Master_Assn1 = None
    newColumns = ['MemberID', 'ClaimsTruncated', 'Total_DrugCount', 'DSFS_0_1', 'DSFS_1_2', 'DSFS_2_3', 'DSFS_3_4', 'DSFS_4_5', 'DSFS_5_6', 'DSFS_6_7', 'DSFS_7_8', 'DSFS_8_9', 'DSFS_9_10', 'DSFS_10_11', 'DSFS_11_12','DaysInHospital']
    Master_Assn1 = pd.merge(daysinhospital, DrugCount_Y1_New, how="left", on="MemberID", left_index=False, right_index=False)
    Master_Assn1 = Master_Assn1[newColumns]
    # print_missing_variables(Master_Assn1)
    # print Master_Assn1.head(3)
    '''outputs:
     MemberID  ClaimsTruncated  Total_DrugCount  DSFS_0_1  DSFS_1_2  DSFS_2_3  \
0  24027423                0                3         0         0         0
1  98324177                0                1         1         0         0
2  33899367                1               23         1         0         1

   DSFS_3_4  DSFS_4_5  DSFS_5_6  DSFS_6_7  DSFS_7_8  DSFS_8_9  DSFS_9_10  \
0         1         0         0         0         0         0          0
1         0         0         0         0         0         0          0
2         1         1         1         1         1         1          1

   DSFS_10_11  DSFS_11_12  DaysInHospital
0           0           0               0
1           0           0               0
2           1           0               1
    '''
    # test and delete
    process_missing_numeric(Master_Assn1, 'Total_DrugCount')
    # your code here for deal with missing values of the dummy variables. Please don't overthink this. You just need to write one line of code
    Master_Assn1 = Master_Assn1.fillna(0)
    Master_Assn1.drop('MemberID', axis=1, inplace=True)
    print Master_Assn1.head(3)
    arr = Master_Assn1.values
    linear_regression(split_train_test(arr))
    '''outputs:
    Coefficients:
[-0.05044987  0.01591138 -0.48598733 -0.15088138 -0.10255352 -0.08591492
 -0.080255   -0.07516292 -0.06195    -0.06551777 -0.06766854 -0.07096135
 -0.07170065 -0.07585565 -0.00627985]
RMSE: 0.26
R2 value: 0.57
    '''

if __name__ == '__main__':
    main()




