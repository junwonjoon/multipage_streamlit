import streamlit as st
from requests import get
import pandas as pd

st.header(f"displaying information about {st.session_state["user_input"][1]}")
df = pd.DataFrame(st.session_state["user_input"][0])
st.table(df)

   




