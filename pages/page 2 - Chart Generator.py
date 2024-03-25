import streamlit as st
from requests import get
import datetime
import pandas as pd


df = pd.DataFrame(st.session_state["user_input"])
df.set_index('Time', inplace=True)
st.line_chart(df, color = '#ef4423')






