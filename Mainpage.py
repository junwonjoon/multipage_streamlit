import streamlit as st
from requests import get
import datetime

def displayDelta(stocksTicker:str, startday:str, endday:str) ->None:
    key = st.secrets["API_KEY_MAINPAGE"]
    json_data = get(f"https://api.polygon.io/v2/aggs/ticker/{stocksTicker}/range/1/day/{startday}/{endday}?apiKey={key}").json()
    if json_data["status"] == "ERROR":
        st.header("Hi welcome to the stocks page")
        pass
    else:
        average_stock_price = [element["vw"] for element in json_data["results"]]
        st.write(average_stock_price)
        if len(average_stock_price) > 2:
            delta_to_print = float(average_stock_price[-1]) - float(average_stock_price[-2])
            st.metric(label=f"{stocksTicker} compared to yesterday", value=average_stock_price[-1], delta=delta_to_print)
    
today = datetime.datetime.now() - datetime.timedelta(days=1)
two_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)

displayDelta("AAPL", str(two_days_ago.strftime('%Y-%m-%d')), str(today.strftime('%Y-%m-%d')))
displayDelta("GOOGL", str(two_days_ago.strftime('%Y-%m-%d')), str(today.strftime('%Y-%m-%d')))

st.set_page_config(
    page_title="Multipage App",
    page_icon = ":)"
)



st.title("Main Page")




st.sidebar.success("Select a page above.")


