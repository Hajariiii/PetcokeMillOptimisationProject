import numpy as np
from pyswarm import pso
import pandas as pd
import joblib
import datetime
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative paths to the model and data files
model_path = os.path.join(current_dir, "xgboost_model.joblib")
data_path = os.path.join(current_dir, "data.xlsx")

# Load the model and read the data file
model = joblib.load(model_path)
df = pd.read_excel(data_path)
def visualise():
    powerlist, speedlist, temperaturelist, dplist, feedlist, ratelist, chainlist = [ df[i].astype(float).tolist() for i in ['Mill Power', 'Main Drive Speed','Input Temperature','DP Mill','Coal Mill Feed Rate', 'Exhaust Air Flow Rate', 'Transport Chain Speed' ]]
    datelist = df['Date'].tolist()

    return datelist, powerlist, speedlist, temperaturelist,dplist, feedlist, ratelist, chainlist

def predict_output(input1, input2, input3):
    input_df = pd.DataFrame({

        'Input Temperature': [float(input1)],
        'Exhaust Air Flow Rate': [float(input2)],
        'Transport Chain Speed': [float(input3)]
    })

    predictions = model.predict(input_df)

    output1 = float(predictions[0][0])
    output2 = float(predictions[0][1])

    return output1, output2


def fitness_function(X, y_desired, model):
        array = np.array([X])
        y_pred = model.predict(array)
        return np.sum(np.abs(y_pred - y_desired))

lb = [170,32000,410]
ub=[210,36000,550]

def opt_func(targetpower, targetspeed):

    y1 = float(targetpower)
    y2 = float(targetspeed)
    y_desired = np.array([y1, y2])
    print(f"Your target is :( Mill Power = {y1} & Main Drive Speed = {y2} )")
    optimizer= pso(fitness_function, lb = lb,ub = ub, 
                   args=(y_desired, model), maxiter=70)
    x_opt = optimizer[0]

    # print("Optimized inputs:", x_opt)
    # array = np.array([x_opt])
    # BESToutput1, BESToutput2 = model.predict(array)[0]
    # print("Corresponding outputs:", BESToutput1, BESToutput2)

    # BESToutput1 = float(BESToutput1)
    # BESToutput2 = float(BESToutput2)
    return  x_opt