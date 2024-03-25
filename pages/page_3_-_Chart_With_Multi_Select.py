import streamlit as st
import pandas as pd
from Mainpage import generate_stock_dictionary, dict_stocksTicker


st.header("Welcome to the Multi Select Chart Generator")
st.subheader("Which company would you like to compare?")
st.subheader("(choose up to 3)")

options = st.multiselect(
    'Select the prices that you want to compare',
    [keys for keys in dict_stocksTicker.keys()],
    default = None, max_selections = 3,
    )

end_date_select = st.date_input("When should be the end date?", 
                                datetime.datetime.now() - datetime.timedelta(days=1), 
                                max_value= datetime.datetime.now() - datetime.timedelta(days=1))
st.write("The end date is", end_date_select)

#Due to the limitation of free API, I can only request information within 2years
start_date_select = st.date_input("When should be the start date?", datetime.date(2024, 1, 1), 
                                  min_value= datetime.datetime.now() - datetime.timedelta(days=730),
                                  max_value= end_date_select)
st.write("The start date is", start_date_select)

st.subheader("Select the time increment")
timespan_select = st.select_slider(
    'Select the timespan',
    options=['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'],
    value=('day'))
st.write('You selected timespan as ', timespan_select)

st.subheader("Select the multiplier for the timespan")
timespan_multiplier_select = st.number_input('Enter the timespan multiplier', 1, step = 1)
st.write('Timespan multiplier is:', timespan_multiplier_select)


st.write('You selected:', options)
list_of_dict_stocks = []
for items in options:
    list_of_dict_stocks.append(generate_stock_dictionary(items, timespan_multiplier_select, 
                               timespan_select,start_date_select, end_date_select))

st.write(list_of_dict_stocks)
