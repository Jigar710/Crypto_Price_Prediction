import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def get_graph():
    buffer = BytesIO()
    buffer.flush()
    plt.savefig(buffer, format='png')  #,dpi=700
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def data_collect(t):
    global df
    str1 = "E:/Test Minor Project/home/Data/pickles/"+ str(t) + str(".pickle")
    df = pickle.load(open(str1,"rb"))
    plot_collection(t,df)

def plot_collection(tickers,df):
    plt.figure(figsize=(12,6),dpi=110)
    str = "Price of " + tickers
    print(str)
    sns.lineplot(x=df.index,y="Close", data=df).set_title(str)
    #plt.show()
    global graph
    graph = get_graph()

#data_collect("DOGE-INR")