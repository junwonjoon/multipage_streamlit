import streamlit as st
from requests import get
import datetime
import pandas as pd


if st.button("Generate Table", type="primary"):
    df = pd.DataFrame(st.session_state["user_input"])
    st.table(df)

   




