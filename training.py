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
from tools import build_datasets, build_baseline_mae


# Step 1: 读取数据集
X_train, X_test, y_train, y_test = build_datasets()

# Step 2: 构建DMatrix - dtain & dtest
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Step 3: 构建baseline model
build_baseline_mae(y_train, y_test)
print('================\n')

# Step 4: Training an XGBoost model
# The params dictionary
params = {
    # Best parameters from the result of modelling.
    'max_depth': 1,
    'min_child_weight': 2,
    'eta': 0.1,
    'subsample': 1,
    'colsample_bytree': 0.6,
    # Other parameters
    'objective':'reg:linear',
    'eval_metric': 'mae'
}
# max boosting iteration
num_boost_round=999
# train the model to find best iteration number
model = xgb.train(
    params,
    dtrain,
    num_boost_round=num_boost_round,
    evals=[(dtest, "Test")],
    early_stopping_rounds=10
)
print("Best MAE: {:.5f} in {} rounds".format(model.best_score, model.best_iteration+1))
print('================\n')

# Step 5: Train and save the best model
# train best model with best param dics & best number of round
num_boost_round = model.best_iteration + 1
params['silent'] = 1
best_model = xgb.train(
    params,
    dtrain,
    num_boost_round=num_boost_round,
    evals=[(dtest, "Test")]
)
mae = mean_absolute_error(best_model.predict(dtest), y_test)
print("MAE is {:.5f}".format(mae))

# save best model
best_model.save_model(constant.best_model)
print('Saved best model to', constant.best_model)
print('================\n')

