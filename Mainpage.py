import streamlit as st
from requests import get
import datetime

def displayDelta(stocksTicker:str, startday:str, endday:str, key:str) ->None:
    json_data = get(f"https://api.polygon.io/v2/aggs/ticker/{stocksTicker}/range/1/day/{startday}/{endday}?apiKey={key}").json()
    if json_data["status"] == "ERROR":
        st.write("Too many request were created, maximum request is 5 per minute, try again a minute later")
    elif json_data["status"] == "NOT_AUTHORIZED":
        st.write("Sorry, the range you have assigned contain too many steps! Please reduce the range of steps by increasing the multiplier or decrease the date difference")
    else:
        average_stock_price = [element["vw"] for element in json_data["results"]]
        delta_to_print = average_stock_price[-1] - average_stock_price[-2]
        st.metric(label=f"{stocksTicker} compared to yesterday", value=average_stock_price[-1], delta=delta_to_print)
    
today = datetime.datetime.now() - datetime.timedelta(days=1)
two_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
key = st.secrets["API_KEY"]

displayDelta("aapl", two_days_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'), key)
displayDelta("googl", two_days_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'), key)

st.set_page_config(
    page_title="Multipage App",
    page_icon = ":)"
)



st.title("Main Page")




st.sidebar.success("Select a page above.")


