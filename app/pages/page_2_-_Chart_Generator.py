"""
This is a page 2
Author: Wonjoon Jun
Date: Mar 25, 2024
Please view README.md for more information.
"""
import streamlit as st
import pandas as pd

st.header("Welcome to the Chart Generator")
try:
    st.write(f'Here is a chart displaying information about {st.session_state["name_of_company"]}')
    df = pd.DataFrame(st.session_state["user_input"])
except KeyError:
    st.error('The requested key does not exist in the session state.\n'
             'Please go back to the main page to save your preference or try sometime later')
    st.page_link("Mainpage.py", label="Home", icon="🏠")

else:
    df.set_index('Time', inplace=True)
    st.line_chart(df)
