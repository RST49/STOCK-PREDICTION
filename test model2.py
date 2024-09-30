import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load and preprocess data (as before)
df = pd.read_csv("C:\\Users\\RST\\Desktop\\Minor project\\combined_final1.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Creating targets (shifting)
df['target_5min'] = df['Close'].shift(-5)
df['target_10min'] = df['Close'].shift(-10)
df['target_15min'] = df['Close'].shift(-15)
df = df.dropna()

features = ['Open', 'High', 'Low', 'Close']
target_5min = df['target_5min'].values
target_10min = df['target_10min'].values
target_15min = df['target_15min'].values

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(df[features])

def create_sequences(data, target, window_size):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i - window_size:i])
        y.append(target[i])
    return np.array(X), np.array(y)

window_size = 60
X, y_5min = create_sequences(scaled_features, target_5min, window_size)
_, y_10min = create_sequences(scaled_features, target_10min, window_size)
_, y_15min = create_sequences(scaled_features, target_15min, window_size)

X_train, X_test, y_train_5min, y_test_5min = train_test_split(X, y_5min, test_size=0.2, shuffle=False)
_, _, y_train_10min, y_test_10min = train_test_split(X, y_10min, test_size=0.2, shuffle=False)
_, _, y_train_15min, y_test_15min = train_test_split(X, y_15min, test_size=0.2, shuffle=False)

# Create an LSTM model within GPU context
def create_model():
    model = Sequential()
    model.add(LSTM(units=100, return_sequences=True, input_shape=(window_size, len(features))))
    model.add(LSTM(units=100))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Check if GPU is available
if len(tf.config.list_physical_devices('GPU')) > 0:
    print("GPU is available. Running on GPU.")

# Train the model on GPU (if available)
with tf.device('/GPU:0'):  # Ensure the model runs on the GPU
    model_5min = create_model()
    model_10min = create_model()
    model_15min = create_model()

    # Train the models
    model_5min.fit(X_train, y_train_5min, epochs=20, batch_size=64)
    model_10min.fit(X_train, y_train_10min, epochs=20, batch_size=64)
    model_15min.fit(X_train, y_train_15min, epochs=20, batch_size=64)

# Predictions (without inverse scaling since the targets are not scaled)
predictions_5min = model_5min.predict(X_test)
predictions_10min = model_10min.predict(X_test)
predictions_15min = model_15min.predict(X_test)

# Plotting the actual vs predicted results
plt.figure(figsize=(14, 8))
plt.plot(df['Date'].iloc[-len(y_test_5min):], y_test_5min, label='Actual Close (5 min)', color='blue')
plt.plot(df['Date'].iloc[-len(predictions_5min):], predictions_5min, label='Predicted Close (5 min)', color='red')
plt.title('5-minute Close Price Prediction (Without Normalization)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
