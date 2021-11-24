import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow.keras as tf
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import plotly.graph_objects as go
#import data_collect
import datetime
from keras.models import load_model
from tensorflow.python.eager.context import graph_mode

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')  #,dpi=700
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def find_pre(t):
    global df
    str1 = "E:/Test Minor Project/home/Data/pickles/"+ str(t) + str(".pickle")
    str2 = "E:/Test Minor Project/home/Data/Model/"+ str(t) + str("_RF.h5")
    str3 = "E:/Test Minor Project/home/Data/Model/"+ str(t) + str("_RF_Scaler.pickle")
    str4 = "E:/Test Minor Project/home/Data/Model/"+ str(t) + str("_RF_pred.pickle")
    
    df = pickle.load(open(str1,"rb"))
    model = pickle.load(open(str2,"rb"))
    scaler = pickle.load(open(str3,"rb"))
    x_pred = pickle.load(open(str4,"rb"))

    forecast = model.predict(x_pred)
    forecast = forecast.reshape(-1,1)
    forecast = scaler.inverse_transform(forecast)
    forecast = forecast.reshape(-1)

    df['Prediction'] = np.nan
    last_date = pd.to_datetime(df.index[-1])
    last_sec = last_date.timestamp()
    one_day_sec = 86400 
    next_sec = last_sec + one_day_sec 

    for i in forecast:
        next_date = datetime.datetime.fromtimestamp(next_sec)
        next_sec += 86400
        df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i] 

    df = pd.DataFrame(df)
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12,8))
    plt.plot(df['Close'], color='blue', label='Real')
    plt.plot(df['Prediction'], color='red', label='Prediction')
    str12 = str(t) +  ' Price Prediction for 7 base length'
    plt.title(str12)
    plt.legend()
    global graph
    graph = get_graph()
    fig = go.Figure()

    fig.add_trace(go.Scatter(y=df['Close'],x=df.index,
                        mode='lines',
                        name='Real'))
    fig.add_trace(go.Scatter(y=df['Prediction'],x=df.index,
                        mode='lines',
                        name='Prediction'))
    fig.show() 

    