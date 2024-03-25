import streamlit as st
from requests import get
import pandas as pd

df = pd.DataFrame(st.session_state["user_input"][0])
st.table(df)

   




