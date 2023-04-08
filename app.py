import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import pandas_datareader as data
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import plotly.graph_objs as go
import plotly.express as px
import requests
from streamlit_lottie import st_lottie


start = '2010-01-01'
end = '2023-04-10'


def main():
    st.set_page_config(page_title="My Streamlit App",page_icon=":chart_with_upwards_trend:" ,layout="wide")

if __name__ == "__main__":
    main()

css = '''
h1 {
    color: white;
    font-size: 50px;
    align: center;
    
}

p {
    color: white;
    font-size: 20px;
}

.sidebar .sidebar-content {
    background-color: #333;
    color: white;
}

.sidebar .sidebar-title, .sidebar .sidebar-item {
    color: white;
}
body {
    font-family: SaxMono;
    # font-size: 16px;
}
.stTextInput > div > div > input {
    width: 300px;
}
.main {
    # background-color: #eee;
    padding: 20px;
}
'''


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_stocks = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_kuhijlvx.json")
lottie_stocks2 = load_lottieurl("https://assets5.lottiefiles.com/private_files/lf30_F3v2Nj.json")
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


# st.set_page_config(layout="wide")
st.title(':chart_with_upwards_trend: Predictbay')
st.subheader('Welcome to our _Stocks Prediction_ WebApp')
st.markdown("<a href='https://github.com/deepraj21/Realtime-Stock-Predictor'><img src='https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'></a>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
left_col, right_col = st.columns(2)
with left_col:
    st.subheader("- What is the stock market?")
    st.write("The stock market is a place where publicly traded companies' stocks or shares are bought and sold. Investors purchase stocks in the hope of making a profit, either by selling them at a higher price or by earning dividends on their investment.")
    st.subheader("- How does the stock market work?")
    st.write("Companies issue stocks when they want to raise capital, or money, to fund their operations or expansion plans. These stocks are then traded on stock exchanges, which are platforms where buyers and sellers can trade stocks.")
    st.write("The price of a stock is determined by supply and demand. If there are more buyers than sellers, the price of the stock goes up. If there are more sellers than buyers, the price of the stock goes down.")
# Add a stock image in the right column
with right_col:
    st_lottie(lottie_stocks)


col1,col2 =st.columns(2)
with col1:
    st_lottie(lottie_stocks2)   
with col2:
    user_input = st.text_input('Enter a Valid stock Ticker', 'AAPL')
    df = yf.download(user_input, start, end)
    st.subheader('Data from 2010 - 2023')
    st.write(df.describe())



st.subheader('- Closing Price')
st.write("The closing price is reported by stock exchanges at the end of each trading day and is widely available through financial news outlets, online trading platforms, and other financial resources. It is important for investors to keep track of the closing price of stocks they are interested in to make informed investment decisions.")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines'))
fig.update_layout(title='Closing Price vs Time Chart',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  width=1000,
                  height=600)
st.plotly_chart(fig)

# st.subheader('Closing Price vs Time Chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name='MA100'))
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Close'))
fig.update_layout(title='Closing Price vs Time Chart with 100MA',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  width=1000,
                  height=600)
st.plotly_chart(fig)

# st.subheader('Closing Price vs Time Chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name='MA100'))
fig.add_trace(go.Scatter(x=df.index, y=ma200, mode='lines', name='MA200'))
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Close'))
fig.update_layout(title='Closing Price vs Time Chart with 100MA & 200MA',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  width=1000,
                  height=600)
st.plotly_chart(fig)

data_training = pd.DataFrame(df['Close'][0:int(len(df)*70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

scaler = MinMaxScaler(feature_range=(0, 1))

data_training_array = scaler.fit_transform(data_training)

x_train = []
y_train = []

for i in range(100, data_training_array.shape[0]):
    x_train.append(data_training_array[i-100: i])
    y_train.append(data_training_array[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

# load model
model = load_model('keras_model.h5')

past_100_days = data_training.tail(100)

final_df = past_100_days.append(data_testing, ignore_index=True)

input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

y_predict = model.predict(x_test)

scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predict = y_predict * scale_factor
y_test = y_test * scale_factor

st.subheader('Original VS predicted')
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df.index[int(len(df)*0.70):], y=y_test, name='Original Price'))
fig2.add_trace(go.Scatter(x=df.index[int(len(df)*0.70):], y=y_predict[:, 0], name='Predict'))
fig2.update_layout(title='Original VS predicted',
                   xaxis_title='Date',
                   yaxis_title='Price',
                   width=1000,
                   height=600)

st.plotly_chart(fig2)

   