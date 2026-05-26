import pandas as pd 
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import pickle

data=pd.read_csv(r'C:\Users\trabe\Desktop\PFE\prediction\jet_fuel_prices.csv',parse_dates=["date"])
data=data.drop("source",axis=1)

price=data["price_usd_per_gallon"]
scaler = MinMaxScaler()
yscaled = scaler.fit_transform(price.values.reshape(-1, 1))

def create_sequences(data, window):
    x, y = [], []
    for i in range(len(data) - window):
        x.append(data[i:i+window])
        y.append(data[i+window])
    return np.array(x), np.array(y)

window = 24
x, y = create_sequences(yscaled, window)

modellstm = Sequential([
    LSTM(128, input_shape=(window,1), return_sequences=True),
    Dropout(0.2),
    LSTM(64, return_sequences=False),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1)
])
modellstm.compile(optimizer='adam', loss='mse')

modellstm.fit(x, y,epochs=100,batch_size=16,validation_split=0.1,
            callbacks=[EarlyStopping(monitor='val_loss',patience=15,restore_best_weights=True)],
            verbose=1)
modellstm.save("models/lstm_price.keras")

with open("models/scaler_price.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("models/window.pkl", "wb") as f:
    pickle.dump(window,f)