__author__ = 'pbhandari'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
# my function for separating different kinds of variables
def variable_type(df, nominal_level = 3):
    categorical, numeric, nominal = [],[],[]
    for variable in df.columns.values:
        if np.issubdtype(np.array(df[variable]).dtype, int) or np.issubdtype(np.array(df[variable]).dtype, float):
            if len(np.unique(np.array(df[variable]))) <= nominal_level:
                nominal.append(variable)
            else:
                numeric.append(variable)
        else:
            categorical.append(variable)
    return numeric,categorical,nominal

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

def draw_histograms(df, variables, n_rows, n_cols):
    """
    Your code here to draw multiple histograms in a figure.
    variables includes a list of variables you need to draw histograms for.
    n_rows and n_cols specifies the number of subplots you need to have in a figure. For instance if n_rows =3 and n_cols =2,
    there will 3*2 = 6 subplots placed in a grid of 3 rows and 2 columns.
    subplot(321) is identical to subplot(3,2,1), which refers to the 1st subplot in a grid of 3 rows and 2 columns
    and subplot(325) refers to the 5th subplot in a grid of 3 rows and 2 columns

    histograms.png in the zip file is an figure that includes 3*3 subplots.
    This method has no return values
    """
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols)
    i=0
    for ax in axes.flat:
        ax.hist(df[variables[i]].dropna(),50, alpha=0.5)
        ax.set_title(variables[i])
        i=i+1

    plt.tight_layout()
    plt.show()



def draw_piecharts(df, variables, n_rows, n_cols):
    """
    Your code here to draw multiple pies in a figure.
    piecharts.png in the zip file is an figure that includes 2*1 subplots (pie charts).
    This method has no return values
    """
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols)
    i=0
    for ax in axes.flat:
        counts = df[variables[i]].dropna().value_counts()
        print counts
        ax.pie(counts,labels=counts.index, startangle=90)
        ax.set_title(variables[i])
        i=i+1

    plt.tight_layout()
    plt.show()

def add_log_transform(df, variable, indexplus = 1):
    log_variable = "log_" + variable
    """
    Your code here...
    Given a variable, this code will do log transformation. The name of the transformed variable is log_variable
    Indexplus helps to determine where we put the newly created variable. For instance, for this variable 'InqCnt06', we will create a new
    variable called "log_InqCnt06". We want to find the index of the variable 'InqCnt06'. Let's say its index is 4, then 'log_InqCnt06' will have
    index 4+indexplus = 5. We need to insert the newly generated variable to index 5 (right after the original variable)
    This method has no return value. You need to make change to df (data frame) in place.
    """
    index = df.columns.get_loc(variable)+indexplus
    df.insert(index, log_variable, map(lambda x: np.log(x+1), df[variable]))


def add_sqrt_transform(df, variable, indexplus =1):
    sqrt_variable = "sqrt_" + variable
    """
    Your code here...
    Given a variable, this code will do sqrt transformation. The name of the transformed variable is sqrt_variable
    Indexplus helps to determine where we put the newly created variable. For instance, for this variable 'InqCnt06', we will create a new
    variable called "sqrt_InqCnt06". We want to find the index of the variable 'InqCnt06'. Let's say its index is 4 and indexplus is set to be 2, then 'sqrt_InqCnt06' will have
    index 4+indexplus = 6. We need to insert the newly generated variable to index 6
    This method has no return value. You need to make change to df (data frame) in place.
    """
    index = df.columns.get_loc(variable)+indexplus
    df.insert(index, sqrt_variable, map(lambda x: np.sqrt(x), df[variable]))


def split_train_test_frame(df, test_size=.3):
    from sklearn.cross_validation import train_test_split
    df.reset_index(level=0, inplace=True)
    """
    Your code here...
    This method will split the dataframe df into two dataframes based on random sampling with test_size = test_size, one is training data and the other is test data.
    This method is different from the split_train_test_array method below in that the method splits df into two dataframes while split_train_test_array splits
    a 2d-Numpy array into numpy arrays.
    This method returns two data frames (train_, test_). Each includes both the features and the target variable. We don't need to split X and y in this method
    Hint: df.reset_index(level=0, inplace=True) add a column called "index" to df. You can then use train_test_split(df.values, test_size=test_size) to obtain two arrays.
    The first column of each array is the "index" column.
    You can then split the dataframe df based on the indices in the "index column". For instance, in the numpy array that represent training data, the first column can be something like
    [1,3,4,19...134]. These indices represents the row numbers of the rows that have been selected. You can then do dataframe indexing/slicing to select these rows
    to create your training dataframe.
    """
    train, test = train_test_split(df.values, test_size=test_size)
    train_ = df.iloc[train[:,0].astype(int).tolist()]
    test_ = df.iloc[test[:,0].astype(int).tolist()]
    del train_['index']
    del test_['index']
    #train_.to_csv("train.csv")
    #test_.to_csv("test.csv")
    return (train_, test_)

def split_train_test_array(arr, test_size=.3):
    from sklearn.cross_validation import train_test_split
    train, test = train_test_split(arr.values, test_size=test_size)
    train_X = train[:, :-1]
    #print train_X.shape
    train_y = train[:, -1]
    #print train_y.shape
    test_X = test[:,:-1]
    test_y = test[:, -1]
    return (train_X,train_y,test_X,test_y)

def split_x_y(train):
    train_X = train[:, :-1]
    train_y = train[:, -1]
    return (train_X,train_y)

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

def cap_variable(df, variable, num_std):
    upbound = df[variable].mean() + num_std * df[variable].std()
    df[variable] = df[variable].clip(upper = upbound)
