import pandas as pd
from flask import Flask, request, jsonify

from YieldPrediction.DataModeling.base_data import yield_df
from YieldPrediction.DataModeling.base_model import preprocess_data, data_split, decision_tree_model, random_forest_model, logistic_regressor_model

app = Flask(__name__)

X_train, X_test, y_train, y_test = None, None, None, None
decision_reg, forest_reg, log_reg = None, None, None
dt_rmse, forest_rmse, log_rmse = None, None, None
dt_r2, forest_r2, log_r2 = None, None, None
SETUP_COMPLETE = False


def setup():
    global X_train, X_test, y_train, y_test

    # preprocess the data
    production_variables_data = preprocess_data(yield_df)

    # Data split
    X_train, X_test, y_train, y_test = data_split(production_variables_data)


def build_models():
    global decision_reg, forest_reg, log_reg
    global dt_rmse, forest_rmse, log_rmse
    global dt_r2, forest_r2, log_r2
    global SETUP_COMPLETE

    # dt
    decision_reg, dt_rmse, dt_r2 = decision_tree_model(X_train, y_train, X_test, y_test)

    # random forest
    forest_reg, forest_rmse, forest_r2 = random_forest_model(X_train, y_train, X_test, y_test)

    # logistic model
    log_reg, log_rmse, log_r2 = logistic_regressor_model(X_train, y_train, X_test, y_test)

    SETUP_COMPLETE = True


def predictions(x_test):
    y_pred_dct = decision_reg.predict(x_test)
    y_pred_forest = forest_reg.predict(x_test)
    y_pred_log = log_reg.predict(x_test)
    return y_pred_dct, y_pred_forest, y_pred_log


def yield_localization(area, predicted_yield):
    final_area = 0
    ha = 10000  # 1 hac is 10000m^2
    if "," in area:
        # assume dimensions were given
        w, l = area.split(',')
        final_area = (int(w) * int(l))/ha  # convert to hac
    else:
        final_area = float(area)

    # convert the yield in kgs and divide by land size
    farm_yield = (predicted_yield*1000)*final_area

    # Convert into 90kg bags
    bags = farm_yield / 90

    return farm_yield, bags


@app.route('/predict', methods=['POST'])
def api():
    station = request.form['station']
    crop = request.form['crop']
    country = request.form['country']
    area = request.form['area']

    if not SETUP_COMPLETE:
        print('Setting up the environment')
        setup()
        build_models()

    # Do something with the station, crop, and country data
    # create the dataframe and preprocess
    data = [{
        "STATIONNAME": station,
        "CROP": crop,
        "COUNTRY": country
    }]
    df = pd.DataFrame(data)
    production_variables_data = preprocess_data(df)

    # Make the prediction
    dct, forest, linear = predictions(production_variables_data)

    # Decision Fusion
    average_prediction = (dct[0] + forest[0] + linear[0]) / 3
    print(f"average_prediction: {average_prediction}")

    farm_yields, farm_bags = None, None

    if area:
        farm_yields, farm_bags = yield_localization(area, average_prediction)

    response_string = f"The average yield prediction for {station} is approximately {average_prediction:.2f} tonnes/ha"\
                      f" For your plot size {area} ha we predict {farm_yields:.2f} kg which is approximately {farm_bags:.1f}" \
                      f" 90kg bags of {crop}"

    # return jsonify({'response': response_string})
    return response_string

"""
    Evidence:
    => some average yield estimates from the Kenya Agricultural and Livestock Research Organization (KALRO). 
    According to KALRO, the average yield of maize in Kenya is around 1,600 kg per hectare (ha) for rainfed production, 
    and 2,700 kg per ha for irrigated production.
    
    Ref2: => https://www.yieldgap.org/gygaviewer/index.html
"""

# if __name__ == '__main__':
#     app.run(debug=True)
