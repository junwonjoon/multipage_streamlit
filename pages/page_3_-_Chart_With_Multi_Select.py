import streamlit as st
import pandas as pd
import datetime
from Mainpage import generate_stock_dictionary, dict_stocksTicker


st.header("Welcome to the Multi Select Chart Generator")
st.subheader("Which company would you like to compare?")
st.subheader("(choose up to 3)")
list_of_user_input = st.session_state["list_of_inputs"]

options = st.multiselect(
    'Select the prices that you want to compare',
    [keys for keys in dict_stocksTicker.keys()],
    default = list_of_user_input[1], max_selections = 3,
    )
st.write('You selected:', options)
list_of_dict_stocks = []


st.write(generate_stock_dictionary(list_of_user_input[0],options[0], list_of_user_input[2], list_of_user_input[3],list_of_user_input[4], list_of_user_input[5]))
