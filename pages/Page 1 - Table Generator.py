import streamlit as st
from requests import get
import pandas as pd

st.header("Welcome to the table generator")
try:
    df = pd.DataFrame(st.session_state["user_input"])
except KeyError:
    # Handle the case where the key does not exist
    st.error('The requested key does not exist in the session state.')
    # Optionally, set a default value or perform other fallback operations
else:
    st.table(df)

   




