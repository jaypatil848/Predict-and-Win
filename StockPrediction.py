# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 14:11:54 2022

@author: DELL
"""


import plotly.express as px
import pandas as pd
import pandas_datareader as data
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import yfinance as yf
import plotly.graph_objs as plot
import mplfinance as mpf
import warnings

warnings.filterwarnings('ignore')

# Customizing the sidebar with CSS
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 20px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content .block-container {
        background-color: #f8f9fa;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.05);
    }
    .sidebar .sidebar-content .block-container:first-child {
        margin-top: 0;
    }
    .sidebar .sidebar-content .block-container:last-child {
        margin-bottom: 0;
    }
    .sidebar .sidebar-content .block-container h2 {
        margin-top: 0;
        margin-bottom: 10px;
        color: #333333;
    }
    .sidebar .sidebar-content .block-container ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    .sidebar .sidebar-content .block-container ul li {
        margin-bottom: 5px;
    }
    .sidebar .sidebar-content .block-container ul li a {
        text-decoration: none;
        color: #333333;
        font-weight: bold;
    }
    .sidebar .sidebar-content .block-container ul li a:hover {
        color: #007bff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.title('Navigation')
navigation = st.sidebar.radio('Go to:', ('Home', 'Market Trends', 'Prediction'))

if navigation == 'Home':
    st.write('Welcome to the Home page!')
    st.write('Please enter a stock ticker and select a navigation option from the sidebar.')
    
# Project title
st.title(f'Which Stock are you Looking For:')
user_input = st.text_input('Enter Stock Ticker From Yahoo Finance', '')

##Date formatting
start_date_str = st.date_input('Start Date', datetime(2015, 1, 1))
end_date_str = st.date_input('End Date', datetime.today())
start_date = datetime.combine(start_date_str, datetime.min.time())
end_date = datetime.combine(end_date_str, datetime.max.time())

df = pd.DataFrame()  # Define an empty DataFrame


if user_input:
    # Data downloading
    df = yf.download(user_input, start=start_date, end=end_date)
    # Project title
    st.subheader(f'Data for {user_input} from {start_date_str} to {end_date_str}')
    
    # Button to show the data
    if st.button("Prices & Volumes"):
        st.write(df.describe())
    if st.button("Close"):
        st.write("")



if navigation == 'Market Trends':
    if user_input:
        st.title(f'Advanced Charts for {user_input}')
        #Tabs to show different graphs
        tab1,tab2,tab3,tab4,tab5 = st.tabs(["Line chart","Candlestick Chart","Moving Averages","RSI","Bollinger Bands"])

        with tab1:
            st.subheader(f'Price variation over the years For : {user_input} from {start_date_str} to {end_date_str}')
            st.subheader(f'Closing Price vs Time chart for {user_input}')       
            fig_line=px.line(df["Close"])
            st.plotly_chart(fig_line)
        
        
        with tab2:
            st.subheader(f'Candlestick Chart For: {user_input} from {start_date_str} to {end_date_str}')
            #declare figure
            fig = plot.Figure()
            plt.figure(figsize=(30,30))
            #Candlestick
            fig.add_trace(plot.Candlestick(x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'], name = 'market data'))
            # Add titles
            fig.update_layout(yaxis_title='Stock Price (Indian Rupees per Shares)')
            
            # X-Axes
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(step="all")
                    ])
                )
            )
            st.plotly_chart(fig,theme=None, use_container_width=False)

        with tab3:
            st.subheader(f'Moving Averages For: {user_input} from {start_date_str} to {end_date_str}')
            df['SMA100'] = df['Close'].rolling(window=20).mean()
            df['EMA100'] = df['Close'].ewm(span=20, adjust=False).mean()
            fig_MA = mpf.figure(figsize=(10, 8))
            ax1 = fig_MA.add_subplot(1, 1, 1)
            ax1.plot(df.index, df['Close'], color='lightblue', label='Daily Close Price')
            ax1.plot(df.index, df['SMA100'], color='green', label='SMA 20')
            ax1.plot(df.index, df['EMA100'], color='red', label='EMA 20')
            ax1.legend()
            st.pyplot(fig_MA)

        with tab4:
            st.subheader(f'Relative Strength Index For: {user_input} from {start_date_str} to {end_date_str}')
            df['RSI'] = 100 - (100 / (1 + (df['Close'].diff(1) / df['Close'].shift(1)).fillna(0)))
            fig_RSI = mpf.figure(figsize=(10, 8))
            ax2 = fig_RSI.add_subplot(1, 1, 1)
            ax2.plot(df.index, df['Close'], color='lightblue', label='Daily Close Price')
            ax2.plot(df.index, df['RSI'], color='purple', label='RSI')
            ax2.axhline(60, color='red', linestyle='--')
            ax2.axhline(30, color='green', linestyle='--')
            ax2.legend()
            st.pyplot(fig_RSI)

        with tab5:
            st.subheader(f'Bollinger Bands For: {user_input} from {start_date_str} to {end_date_str}')
            rolling_mean = df['Close'].rolling(window=20).mean()
            rolling_std = df['Close'].rolling(window=20).std()
            upper_band = rolling_mean + 2 * rolling_std
            lower_band = rolling_mean - 2 * rolling_std
            fig_BB = mpf.figure(figsize=(10, 8))
            ax3 = fig_BB.add_subplot(1, 1, 1)
            ax3.plot(df.index, df['Close'], color='lightblue', label='Daily Close Price')
            ax3.plot(df.index, rolling_mean, color='green', label='SMA 20')
            ax3.plot(df.index, upper_band, color='red', label='Upper Bollinger Band')
            ax3.plot(df.index, lower_band, color='orange', label='Lower Bollinger Band')
            ax3.fill_between(df.index, lower_band, upper_band, color='gray', alpha=0.1)
            ax3.legend()
            st.pyplot(fig_BB)

if navigation == 'Prediction':
    st.title(f'Prediction for {user_input}')
       



 
 
































