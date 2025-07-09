import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error,r2_score
from statsmodels.tsa.arima.model import ARIMA
import numpy as np 
from sklearn.preprocessing import StandardScaler
from datetime import datetime,timedelta
import pandas as pd 


import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler


def get_data(ticker):
    
    # default interval is months ---manually interval to days 
    stock_data = yf.download(ticker, start='2024-01-01', end=datetime.today().strftime('%Y-%m-%d'), interval='1d')
    
    # drop null values from Close Price 
    return stock_data[['Close']].dropna()


def stationary_check(close_price):
    adf_test = adfuller(close_price)
    p_value = round(adf_test[1], 3)
    return p_value


def get_differencing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    while p_value > 0.05: # Limit differencing to avoid over-differencing
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationary_check(close_price)
    return d,p_value


def fit_model(data, differencing_order):
    data = pd.Series(data).dropna()
    
    try:
        model = ARIMA(data, order=(30, differencing_order, 30))  # Keep (p,d,q) small to ensure stability
        model_fit = model.fit()
    except Exception as e:
        print("Model fitting failed:", e)
        return pd.Series([np.nan]*30)

    forecast = model_fit.get_forecast(steps=30)
    predictions = forecast.predicted_mean
    return predictions


def evaluate_model(original_price, differencing_order):
    if len(original_price) < 60:
        raise ValueError("Not enough data to split into train/test for evaluation.")
    
    train_data = original_price[:-30]
    test_data = original_price[-30:]
    predictions = fit_model(train_data, differencing_order)

    predictions = predictions[:len(test_data)]
    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    return round(rmse, 2)


def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    return scaled_data.flatten(), scaler  # Return 1D array for ARIMA


def inverse_scaling(scaler, scaled_data):
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1, 1))
    return close_price.flatten()


def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)
    forecast_index = pd.date_range(start=datetime.now(), periods=30, freq='D')
    forecast_df = pd.DataFrame({'Date': forecast_index, 'Close': predictions}).set_index('Date')

    return forecast_df,predictions,forecast_index



def get_rolling_mean(close_price):
    rolling_price =close_price.rolling(window=7).mean().dropna()
    
    return rolling_price

