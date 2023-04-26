"""
    Here we do the modeling
"""
# Models
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
# Model evaluation
from sklearn.metrics import mean_squared_error, r2_score
# Data preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class MultiColumnLabelEncoder:
    def __init__(self, columns=None):
        self.columns = columns  # array of column names to encode

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        """
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname, col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)


def preprocess_data(yield_df_):
    production_variables_data = MultiColumnLabelEncoder(
        columns=['STATIONNAME', 'CROP', 'COUNTRY']).fit_transform(
        yield_df_)

    return production_variables_data


"""Data Splitting"""


def data_split(production_variables_data):
    y = production_variables_data['YA']
    X = production_variables_data.loc[:, ~production_variables_data.columns.str.contains('YA')]

    # take the columns of interest
    columns_of_interest = ['STATIONNAME', 'CROP', 'COUNTRY']
    X = X.loc[:, columns_of_interest]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    return X_train, X_test, y_train, y_test


decision_reg, forest_reg, log_reg = None, None, None

"""Models"""
"""=> Decision Tree"""


def decision_tree_model(X_train, y_train, X_test, y_test):
    global decision_reg
    decision_reg = tree.DecisionTreeRegressor(random_state=42)
    decision_reg = decision_reg.fit(X_train, y_train)

    y_pred_dt = decision_reg.predict(X_test)

    rmse = mean_squared_error(y_test, y_pred_dt)
    r2_dt = r2_score(y_test, y_pred_dt)

    print(f'\nDecision Tree Regressor: \nRMSE: {rmse} \nR^2 score: {r2_dt}')
    return decision_reg, rmse, r2_dt


"""=> Random Forest Regressor"""


def random_forest_model(X_train, y_train, X_test, y_test):
    global forest_reg
    forest_reg = RandomForestRegressor(random_state=42)
    forest_reg = forest_reg.fit(X_train, y_train)

    y_pred_rf = forest_reg.predict(X_test)

    forest_rmse = mean_squared_error(y_test, y_pred_rf)
    forest_r2 = r2_score(y_test, y_pred_rf)

    print(f'\n\nRandom Forest Regressor: \nRMSE: {forest_rmse} \nR^2 score: {forest_r2}')
    return forest_reg, forest_rmse, forest_r2


"""Multivariate Logistic Regressor"""


def logistic_regressor_model(X_train, y_train, X_test, y_test):
    global log_reg
    log_reg = LinearRegression()
    log_reg = log_reg.fit(X_train, y_train)

    y_pred_log = log_reg.predict(X_test)

    log_rmse = mean_squared_error(y_test, y_pred_log)
    log_r2 = r2_score(y_test, y_pred_log)

    print(f'\n\nMultivariate Logistic Regressor: \nRMSE: {log_rmse} \nR^2 score: {log_r2}')
    return log_reg, log_rmse, log_r2


# def predictions(X_test):
#     y_pred_dct = decision_reg.predict(X_test)
#     y_pred_forest = forest_reg.predict(X_test)
#     y_pred_log = log_reg.predict(X_test)
#     return y_pred_dct, y_pred_forest, y_pred_log

# import random
# for i in range(10):
#     x = random.randint(0, (len(X_test)-1))
#     print(f"X_test: {X_test.iloc[x]}")
