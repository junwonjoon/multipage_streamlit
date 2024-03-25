import streamlit as st
from requests import get
import pandas as pd

st.header(f"displaying information about {st.session_state["company_name"]}")
df = pd.DataFrame(st.session_state["user_input"])
st.table(df)

   




