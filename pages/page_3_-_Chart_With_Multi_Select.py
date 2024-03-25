import streamlit as st
import pandas as pd
from Mainpage import generate_stock_dictionary, dict_stocksTicker


st.header("Welcome to the Multi Select Chart Generator")
st.subheader("Which company would you like to compare? (choose up to 3)")
options = st.multiselect(
    'Select the prices that you want to compare',
    [keys for keys in dict_stocksTicker.keys()],
    default = None, max_selections = 3,
    )

st.write('You selected:', options)








