import streamlit as st
import pandas as pd
import datetime
from Mainpage import generate_stock_dictionary, stocksTicker_select, dict_stocksTicker, timespan_multiplier_select, timespan_select,start_date_select, end_date_select


st.header("Welcome to the Multi Select Chart Generator")
st.subheader("Which company would you like to compare?")
st.subheader("(choose up to 3)")

options = st.multiselect(
    'Select the prices that you want to compare',
    [keys for keys in dict_stocksTicker.keys()],
    default = stocksTicker_select, max_selections = 3,
    )

st.write('You selected:', options)
list_of_dict_stocks = []
for items in options:
    list_of_dict_stocks.append(generate_stock_dictionary(dict_stocksTicker,items, timespan_multiplier_select, timespan_select,start_date_select, end_date_select))

st.write(list_of_dict_stocks)
