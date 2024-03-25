import streamlit as st
from requests import get
import pandas as pd

st.header("Welcome to the table generator")
df = pd.DataFrame(st.session_state["user_input"])
st.table(df)

   




