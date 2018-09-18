# -*- coding: utf-8 -*-

"""
    Author:   Ying
    Date:     2018/09
"""
import numpy as np
import pandas as pd
import constant
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from pandas import DataFrame


def build_datasets():
    """
        读取数据集
        返回training & testing数据集的X & y
    """
    # 读取数据集
    df = pd.read_csv(constant.dataset_file)
    print("Dataset has {} entries and {} features".format(*df.shape))

    # 构建training & testing数据集的X & y
    X = df.drop(constant.label, axis=1)
    y = df[constant.label]
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.1, random_state=42)

    return X_train, X_test, y_train, y_test


def build_baseline_mae(y_train, y_test):
    """
        构建baseline model
        返回baseline model的MAE值
    """
    # "Learn" the mean from the training data
    mean_train = np.mean(y_train)

    # Get predictions on the test set
    baseline_predictions = np.ones(y_test.shape) * mean_train

    # Compute MAE
    mae_baseline = mean_absolute_error(y_test, baseline_predictions)

    print("Baseline MAE is {:.5f}".format(mae_baseline))
    return


def build_prediction_diff(y_hat, y_test):
    """
        保存y_hat, y_test 为 .csv
        保存 prediction result 形式为 ['y_hat', 'y', 'diff']
    """
    # save y_hat {ndarray} as .csv file with column = 0
    y_hat = np.insert(y_hat, 0, values=0, axis=0)
    np.savetxt(constant.test_y_hat_file, y_hat, delimiter=",")
    print('Saved y_hat to', constant.test_y_hat_file)

    # save y_test {Series} as .csv with index = 0 ~ 276
    y = DataFrame()
    y['y'] = y_test
    y.to_csv(constant.test_y_file, index=None)
    print('Saved y_test result to', constant.test_y_file)

    # concat 2 data sets and compute diff
    df_y_hat = pd.read_csv(constant.test_y_hat_file)
    df_y = pd.read_csv(constant.test_y_file)
    df = pd.concat([df_y_hat, df_y], axis=1)
    df.columns = ['y_hat', 'y']
    df['diff'] = abs(df['y_hat'] - df['y'])

    # save df as prediction result
    df.to_csv(constant.prediction_file, index=None)
    print('Saved prediction result to', constant.prediction_file)
    print('================\n')

