import streamlit as st

st.set_page_config(
    page_title="Multipage App",
    page_icon = ":)"
)

st.title("Main Page")

st.metric(label="Google", value="70 USD", delta="1.2 USD")

st.sidebar.success("Select a page above.")


