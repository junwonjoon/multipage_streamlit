import streamlit as st
import pandas as pd
import datetime
from requests import get
from Mainpage import dict_stocksTicker

def generate_stock_dictionary(dict_stocksTicker:dict, stocksTicker_select:str, timespan_multiplier_select:int, timespan_select:str,
                   start_date_select:datetime, end_date_select:datetime, key:str = st.secrets["API_KEY"]) -> dict:
    stocksTicker = dict_stocksTicker[stocksTicker_select]
    multiplier = timespan_multiplier_select
    timespan = timespan_select
    from_date = start_date_select
    to_date = end_date_select

    json_data = get(f"https://api.polygon.io/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from_date}/{to_date}?apiKey={key}").json()
    if json_data["status"] == "ERROR":
        st.write("Too many request were created, maximum request is 5 per minute, try again a minute later")
    elif json_data["status"] == "NOT_AUTHORIZED":
        st.write("Sorry, the range you have assigned contain too many steps! Please reduce the range of steps by increasing the multiplier or decrease the date difference")
    else:
        average_stock_price = [element["vw"] for element in json_data["results"]]
        the_date_miliseconds = [element["t"] for element in json_data["results"]]
        human_readable_date = [datetime.datetime.fromtimestamp(element / 1000).strftime('%Y-%m-%d %H:%M:%S') for element in the_date_miliseconds]
        data = {
        'Time': pd.to_datetime(human_readable_date),
        f'Average Stock Price of the {timespan}': average_stock_price
        }
        return pd.DataFrame(data)


st.header("Welcome to the Multi Select Chart Generator")
st.subheader("Which company would you like to compare?")
st.subheader("(choose up to 3)")
list_of_user_input = st.session_state["list_of_inputs"]

options = st.multiselect(
    'Select the prices that you want to compare',
    [keys for keys in dict_stocksTicker.keys()],
    default = list_of_user_input[1], max_selections = 3,
    )
st.write('You selected:', options)
list_of_dict_stocks = []


st.write(generate_stock_dictionary(list_of_user_input[0],options[0], list_of_user_input[2], list_of_user_input[3],list_of_user_input[4], list_of_user_input[5]))
