# -*- coding: utf-8 -*-

"""
    Author:   Ying
    Date:     2018/09
"""
import numpy as np
import pandas as pd
import xgboost as xgb
import constant
from tools import build_datasets, build_baseline_mae


# Step 1: 读取数据集
X_train, X_test, y_train, y_test = build_datasets()

# Step 2: 构建DMatrix - dtain & dtest
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Step 3: 构建baseline model
build_baseline_mae(y_train, y_test)
print('================\n')

# Step 4: Tuning an XGBoost model
# The params dictionary
params = {
    # Parameters that we are going to tune.
    'max_depth': 1,
    'min_child_weight': 2,
    'eta': 0.1,
    'subsample': 1,
    'colsample_bytree': 0.6,
    # Other parameters
    'objective':'reg:linear',
    'eval_metric': 'mae'
}

num_boost_round=999

# - 4.1 simple train with linear model
# model = xgb.train(
#     params,
#     dtrain,
#     num_boost_round=num_boost_round,
#     evals=[(dtest, "Test")],
#     early_stopping_rounds=10
# )
#
# print("Best MAE: {:.5f} with {} rounds".format(
#                  model.best_score,
#                  model.best_iteration+1))
# print('================\n')

#  - 4.2 xgb cross-validation
# cv_results = xgb.cv(
#     params,
#     dtrain,
#     num_boost_round=num_boost_round,
#     seed=42,
#     nfold=5,
#     metrics={'mae'},
#     early_stopping_rounds=10,
#     verbose_eval=True,
# )
#
# print(cv_results)
# print('================\n')


# - 4.3 Parameters max_depth and min_child_weight
#   - max_depth: 9
#   - min_child_weight: 3
#
# gridsearch_params = [
#     (max_depth, min_child_weight)
#     for max_depth in range(1, 4)
#     for min_child_weight in range(1, 3)
# ]
#
# params['silent'] = 1
# # Define initial best params and MAE
# min_mae = float("Inf")
# best_params = None
# for max_depth, min_child_weight in gridsearch_params:
#     print("CV with max_depth={}, min_child_weight={}".format(
#                              max_depth,
#                              min_child_weight))
#
#     # Update our parameters
#     params['max_depth'] = max_depth
#     params['min_child_weight'] = min_child_weight
#
#     # Run CV
#     cv_results = xgb.cv(
#         params,
#         dtrain,
#         num_boost_round=num_boost_round,
#         seed=42,
#         nfold=5,
#         metrics={'mae'},
#         early_stopping_rounds=10
#     )
#
#
#     # Update best MAE
#     mean_mae = cv_results['test-mae-mean'].min()
#     boost_rounds = cv_results['test-mae-mean'].idxmin()
#     print("\tMAE {} for {} rounds".format(mean_mae, boost_rounds))
#     if mean_mae < min_mae:
#         min_mae = mean_mae
#         best_params = (max_depth,min_child_weight)
#
# print("Best params: {}, {}, MAE: {}".format(best_params[0], best_params[1], min_mae))
# print('================\n')


# - 4.4 Parameters subsample and colsample_bytree
#   - subsample: 1
#   - colsample_bytree: 0.8
#
# gridsearch_params = [
#     (subsample, colsample)
#     for subsample in [i/10. for i in range(5,11)]
#     for colsample in [i/10. for i in range(5,11)]
# ]
#
# min_mae = float("Inf")
# best_params = None
# params['silent'] = 1
#
# # We start by the largest values and go down to the smallest
# for subsample, colsample in reversed(gridsearch_params):
#     print("CV with subsample={}, colsample={}".format(
#                              subsample,
#                              colsample))
#
#     # We update our parameters
#     params['subsample'] = subsample
#     params['colsample_bytree'] = colsample
#
#     # Run CV
#     cv_results = xgb.cv(
#         params,
#         dtrain,
#         num_boost_round=num_boost_round,
#         seed=42,
#         nfold=5,
#         metrics={'mae'},
#         early_stopping_rounds=10
#     )
#
#     # Update best score
#     mean_mae = cv_results['test-mae-mean'].min()
#     boost_rounds = cv_results['test-mae-mean'].argmin()
#     print("\tMAE {} for {} rounds".format(mean_mae, boost_rounds))
#     if mean_mae < min_mae:
#         min_mae = mean_mae
#         best_params = (subsample,colsample)
#
# print("Best params: {}, {}, MAE: {}".format(best_params[0], best_params[1], min_mae))
# print('================\n')


# - 4.5 Parameter ETA
#   - ETA: 0.1 (0.034535 with 281 rounds)
#   - ETA: 0.05 (0.034252 with 592 rounds)
# This can take some time…
min_mae = float("Inf")
best_params = None
params['silent'] = 1

for eta in [.3, .2, .1, .05, .01, .005]:
    print("CV with eta={}".format(eta))

    # We update our parameters
    params['eta'] = eta

    # Run and time CV
    cv_results = xgb.cv(
            params,
            dtrain,
            num_boost_round=num_boost_round,
            seed=42,
            nfold=5,
            metrics=['mae'],
            early_stopping_rounds=10
    )

    # Update best score
    mean_mae = cv_results['test-mae-mean'].min()
    boost_rounds = cv_results['test-mae-mean'].argmin()
    print("\tMAE {} for {} rounds\n".format(mean_mae, boost_rounds))
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_params = eta

print("Best params: {}, MAE: {}".format(best_params, min_mae))
print('================\n')



