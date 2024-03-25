import streamlit as st
from requests import get
import pandas as pd

st.header("Welcome to the chart generator")
df2 = pd.DataFrame(st.session_state["user_input"])
df2.set_index('Time', inplace=True)
st.line_chart(df2, color = '#ef4423')






