import streamlit as st
from requests import get
import pandas as pd

st.header("Welcome to The Table Generator")
st.subheader(f"Here is a table displaying information about {st.session_state["name_of_company"]}")
try:
    df = pd.DataFrame(st.session_state["user_input"])
except KeyError:
    st.error('The requested key does not exist in the session state.\n' 
             'Please go back to the main page to save your preference or try sometime later')
else:
    st.table(df)

   




