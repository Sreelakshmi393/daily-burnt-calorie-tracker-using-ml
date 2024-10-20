# Burnt Calorie Tracker Using Machine Learning

## Overview
Gym members lack an efficient and accurate method to track the calories they burn during workouts. Existing solutions are often manual, inaccurate, or not integrated with gym management systems, making it difficult for both members and instructors to monitor progress and adjust workout plans accordingly.

### Objective
- To develop a machine learning-based system that accurately tracks and predicts the calories burnt by gym members during their workouts.

- Gym members to track their daily calorie burn, track fitness goals, and monitor progress over time, while enabling trainers to adjust workout plans based on individual performance. 

- The solution will be implemented as a web application and can be integrated with existing gym management systems for real-time tracking and improved fitness management.



## Dataset 
https://www.kaggle.com/code/muskanjha/calories-burnt-prediction

## Workflow
![image](https://github.com/user-attachments/assets/2cd833a2-5fde-4376-9f80-4497604125f6)

## Modules used
- Pandas
- Numpy
- MatPlotlib
- Seaborn
  
## Perfomance of Algorithms
### - Linear Regressor
  |      Metric     |  Training Data  |   Testing Data  |
  |-----------------|-----------------|-----------------|
  |    R2-Score     |       0.968     |      0.964      |
  |       MAE       |       8.275     |      8.556      |
  |       MSE       |      125.10     |     139.346     |


### - RandomForest Regressor
  |      Metric     |  Training Data  |   Testing Data  |
  |-----------------|-----------------|-----------------|
  |    R2-Score     |       0.999     |      0.997      |
  |       MAE       |       0.640     |      1.799      |
  |       MSE       |       1.090     |      8.504      |


### - XGBoost Regressor
  |      Metric     |  Training Data  |   Testing Data  |
  |-----------------|-----------------|-----------------|
  |    R2-Score     |       0.999     |      0.998      |
  |       MAE       |       0.306     |      1.305      |
  |       MSE       |       0.190     |      3.955      |


## Updates

### 26/09/2024 - System Setup
- **Summary**: Installation of tools and platforms
- **Changes Made**:
  - [Change 1: Collected Dataset]
  - [Change 2: Set Ananconda Environment]
  - [Change 3: Installed tools like Pandas, Numpy, Matplotlib, Scikit-learn and Jupyter Notebook]
- **Impact**: System ready for building Machine Learning model.
- **Next Steps**: Data preprocessing.

### 03/10/2024 - Data Preprocessing
- **Summary**: Preperation an analysis of data for building Machine Learning model
- **Changes Made**:
  - [Change 1: Preprocessed data- filled Null values and label encoding of categorical column]
  - [Change 2: Visualized data using Matplotlib and Seaborn]
  - [Change 3: Choose algorithms to be tried out - Linear Regressor, RnadomForest Regressor, XGBoost Regressor]
- **Impact**: Prepared data for building Machine Learning model
- **Next Steps**: Building and evaluating models using each algorithm

### 03/10/2024 - Data Preprocessing
**Summary**: Preperation an analysis of data for building Machine Learning model
**Changes Made**:
  - [Change 1: Preprocessed data- filled Null values and label encoding of categorical column]
  - [Change 2: Visualized data using Matplotlib and Seaborn]
  - [Change 3: Choose algorithms to be tried out - Linear Regressor, RnadomForest Regressor, XGBoost Regressor]
**Impact**: Prepared data for building Machine Learning model
**Next Steps**: Building and evaluating models using each algorithm

## Installation
Instructions for installing and setting up the project.

## Usage
Details on how to use the project, including examples.

## Contributing 
Guidelines for contributing to the project.

## License
Information about the project's license.



      
