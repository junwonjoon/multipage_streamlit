import streamlit as st
import pandas as pd

st.header("Welcome to the chart generator")
try:
    df = pd.DataFrame(st.session_state["user_input"])
except KeyError:
    st.error('The requested key does not exist in the session state.\n' 
             'Please go back to the main page to save your preference or try sometime later')
else:
    df.set_index('Time', inplace=True)
    st.line_chart(df)







