import streamlit as st
from requests import get
import pandas as pd

st.header("Welcome to the table generator")
df = pd.DataFrame(st.session_state["user_input"])
df.set_index('Time', inplace=True)
st.line_chart(df, color = '#ef4423')






