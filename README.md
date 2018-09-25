# XGBoost

### TODO List

25/09/2018

- [x] add feature to training data: water level (R047)
- [x] label: use diff
- [ ] train offline model in time order (data in 2 months for base model, and data in next month for time series training process)
- [ ] evaluation: use result value in last time + diff (current label) as the result in current time and compute MAE

## Data Exploration
##### Graph:
a: the time series data for Chlorines and flow
* output_3_files.csv (8641)
* output_all_data.csv (8641)

b: The time series data is truncated for water-inlet periods 
- output_2_days_water_inlet.csv (69)
 - Graph - output_2_days_water_inlet.csv ( for Graph )

 File Name | Content | Source file
:---: | :---: | :---:
output_2_days_water_inlet.csv | 2 periods of data | 03_2 _days _data

## Data pre-processing

File Name | Content | Source file
:---: | :---: | :---:
output_3_files.csv | pump open data | 02_pre-processing
output_all_data.csv | all data | 02_pre-processing
output_open_4_data.csv | pump open with levels data| 02_pre-processing
output_all_4_data.csv | all data with levels | 02_pre-processing
modelling_dataset.csv | original label | 04_build_dataset
modelling_diff_dataset.csv | diff label | 04_build_dataset
modelling_only_open_diff_dataset_levels.csv | diff label only open data with levels | 06_build_dataset_with_4_files
modelling_diff_dataset_levels.csv | diff label with levels and 2h close data | 06_build_dataset_with_4_files

## Modelling
#### modelling.py
- 4.1 simple train with linear model
- 4.2 xgb cross-validation
- 4.3 Parameters max_depth and min_child_weight

Param | Value 
:---: | :---: |
max_depth | 9
min_child_weight | 3
MAE | 0.038

- 4.4 Parameters subsample and colsample_bytree

Param | Value 
:---: | :---: |
subsample | 1
colsample_bytree | 0.9
MAE | 0.037404


- 4.5 Parameter ETA

 ETA | MAE | Round
:---: | :---: | :---:
 0.3 | 0.037404 | 99
 0.2 | 0.035976 | 145
 0.1 | 0.034535 | 281
 0.05 | 0.034252 | 592
 0.01 | 0.347448 | 998


#### training.py
Train and save the best model
- best model: my_model.model
#### testing.py
Use saved model to do prediction

Content | File Name
:---: | :---: 
test_y_hat_file | test_y_hat.csv
test_y_file | test_y.csv
prediction_file | prediction_result.csv (['y_hat', 'y', 'diff'])
