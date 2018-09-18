# -*- coding: utf-8 -*-

"""
    Author:   Ying
    Date:     2018/09
"""
import numpy as np
import pandas as pd
import xgboost as xgb
import constant
from sklearn.metrics import mean_absolute_error
from tools import build_datasets, build_baseline_mae, build_prediction_diff

# Step 1: 读取数据集
X_train, X_test, y_train, y_test = build_datasets()

# Step 2: 构建DMatrix - dtain & dtest
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Step 3: 构建baseline model
build_baseline_mae(y_train, y_test)
print('================\n')

# Step 4: 使用训练好的model进行预测
# load model
loaded_model = xgb.Booster()
loaded_model.load_model(constant.best_model)
# And use it for predictions.
y_hat = loaded_model.predict(dtest)
mae = mean_absolute_error(loaded_model.predict(dtest), y_test)
print("Prediction MAE is {:.5f}".format(mae))
print('================\n')

# Step 5: 保存prediction结果
build_prediction_diff(y_hat, y_test)