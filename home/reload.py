import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import pickle
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow.keras as tf
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

def crypto_data(tickers):
    end = datetime.date.today()
    start = end - datetime.timedelta(730)
    global df
    df = yf.download(tickers, start = start, end = end)
    db_name = "E:/Test Minor Project/home/Data/"+str(tickers)+"_Data.csv"
    df.to_csv(db_name)
    return df

def reload():
    print("----reload-----")
    tickers = ['BTC-INR','ETH-INR','DOGE-INR','XRP-INR']
    for i in tickers:
        df = crypto_data(i)
        str1 = "E:/Test Minor Project/home/Data/pickles/"+ str(i) + str(".pickle")
        df_file = open(str1,"wb")
        print(str1)
        pickle.dump(df,df_file)
        mo_lstm(df,i)
        mo_rf(df,i)

def mo_lstm(df,i):
    x = np.array(df[['Close','Volume']])
    y = df['Close'].shift(-100)
    y = np.array(y).reshape(-1,1)

    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    y = scaler.fit_transform(y)

    x = x.reshape((len(x), 2, 1))
    print(x.shape)

    x_train_test = x[:-100,:,:]
    y_train_test = y[:-100,:]
    x_pred = x[-100:,:]
    y_pred = y[-100:,:]

    x_train, x_test, y_train, y_test = train_test_split(x_train_test, y_train_test, train_size=0.8,shuffle=False)

    model = Sequential()
    model.add(tf.layers.LSTM(units=32, activation='relu',return_sequences=True,input_shape=(2,1), dropout=0.02))
    model.add(tf.layers.LSTM(units=32, return_sequences=True,dropout=0.2))
    model.add(tf.layers.LSTM(units=32, dropout=0.2))
    model.add(tf.layers.Dense(units=1))
    model.summary()

    model.compile(optimizer='adam', loss='mean_squared_error',metrics=['accuracy'])
    train = model.fit(x_train, y_train, epochs=10, batch_size=32)

    accuracy = train.history['accuracy']
    loss = train.history['loss']
    epoch_count = range(1, len(loss) + 1)
    # plt.figure(figsize=(12,8))
    # plt.plot(epoch_count, loss)
    # plt.legend(['Training Loss'])
    # plt.xlabel('Epoch')
    # plt.ylabel('Loss')
    # plt.title("Loss with epoch")
    # plt.show()

    pred = model.predict(x_test)
    # plt.figure(figsize=(12,8))
    # plt.plot(y_test, color='blue', label='Real')
    # plt.plot(pred, color='red', label='Prediction')
    # plt.title('Bitcoin Predicted Price')
    # plt.legend()
    # plt.show()

    pred_tr = scaler.inverse_transform(pred)
    y_test_tr = scaler.inverse_transform(y_test)
    # print(pred_tr.shape, y_test_tr.shape)
    # plt.figure(figsize=(12,8))
    # plt.plot(y_test_tr, color='blue', label='Real')
    # plt.plot(pred_tr, color='red', label='Prediction')
    # plt.title('Actual Price V/S Predicted Price')
    # plt.legend()
    # plt.show()

    errors = abs(pred - y_test)
    print('Average absolute error:', round(np.mean(errors), 2), 'degrees.')
    mape = 100 * (errors / y_test)
    accuracy = 100 - np.mean(mape)
    print('Accuracy:', round(accuracy, 2), '%.')
    str2 = "E:/Test Minor Project/home/Data/Model/"+ str(i) + str("_LSTM.h5")
    str3 = "E:/Test Minor Project/home/Data/Model/"+ str(i) + str("_LSTM_Scaler.pickle")
    str4 = "E:/Test Minor Project/home/Data/Model/"+ str(i) + str("_LSTM_pred.pickle")
    #model.save("Data/Model/BTC_INR_LSTM.h5")
    model.save(str2)
    # pickle.dump(scaler,open("Data/Model/BTC_INR_LSTM_Scaler.pickle","wb"))
    # pickle.dump(x_pred,open("Data/Model/BTC_INR_LSTM_pred.pickle","wb"))
    pickle.dump(scaler,open(str3,"wb"))
    pickle.dump(x_pred,open(str4,"wb"))
    
def mo_rf(df,i):
    x = np.array(df[['Close','Volume']])
    y = df['Close'].shift(-100)
    y = np.array(y).reshape(-1,1)

    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    y = scaler.fit_transform(y)

    x_train_test = x[:-100,:]
    y_train_test = y[:-100]
    x_pred = x[-100:,:]
    y_pred = y[-100:]

    x_train, x_test, y_train, y_test = train_test_split(x_train_test, y_train_test, train_size=0.8, shuffle=False)
    model = RandomForestRegressor()
    model.fit(x_train, y_train)

    pred = model.predict(x_test)
    # plt.figure(figsize=(12,8))
    # plt.plot(y_test, color='blue', label='Real')
    # plt.plot(pred, color='red', label='Prediction')
    # plt.title('Actual Price V/S Predicted Price')
    # plt.legend()
    # plt.show()

    pred = pred.reshape(-1,1)
    pred_tr = scaler.inverse_transform(pred)
    y_test_tr = scaler.inverse_transform(y_test)
    print(pred_tr.shape, y_test_tr.shape)
    # plt.figure(figsize=(12,8))
    # plt.plot(y_test_tr, color='blue', label='Real')
    # plt.plot(pred_tr, color='red', label='Prediction')
    # plt.title('Actual Price V/S Predicted Price')
    # plt.legend()
    # plt.show()
    str2 = "E:/Test Minor Project/home/Data/Model/"+ str(i) + str("_RF.h5")
    str3 = "E:/Test Minor Project/home/Data/Model/"+ str(i) + str("_RF_Scaler.pickle")
    str4 = "E:/Test Minor Project/home/Data/Model/"+ str(i) + str("_RF_pred.pickle")
    pickle.dump(model,open(str2,"wb"))
    pickle.dump(scaler,open(str3,"wb"))
    pickle.dump(x_pred,open(str4,"wb"))
    errors = abs(pred - y_test)
    print('Average absolute error:', round(np.mean(errors), 2), 'degrees.')
    mape = 100 * (errors / y_test)
    accuracy = 100 - np.mean(mape)
    print('Accuracy:', round(accuracy, 2), '%.')