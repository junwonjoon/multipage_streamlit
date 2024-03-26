"""
Welcome to the main page
Author: Wonjoon Jun
Date: Mar 25, 2024
Please view README.md for more information.
"""
from requests import get
import datetime
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Wonjoon's Stock Graph",
    page_icon="📊"
)


def generate_stock_pd_dataframe(dict_stocks_ticker_: dict, stocks_ticker_select_: str, timespan_multiplier_select_: int,
                                timespan_select_: str,
                                start_date_select_: datetime, end_date_select_: datetime,
                                key: str) -> pd.DataFrame:
    if key == "0":
        key = st.secrets["API_KEY"]
    stocks_ticker = dict_stocks_ticker_[stocks_ticker_select_]
    multiplier = timespan_multiplier_select_
    timespan = timespan_select_
    from_date = start_date_select_
    to_date = end_date_select_

    json_data = get(
        f"https://api.polygon.io/v2/aggs/ticker/{stocks_ticker}/range/{multiplier}/"
        f"{timespan}/{from_date}/{to_date}?apiKey={key}").json()
    if json_data["status"] == "ERROR":
        st.write("Too many request were created, maximum request is 5 per minute, try again a minute later")
        exit()
    elif json_data["status"] == "NOT_AUTHORIZED":
        st.write(
            "Sorry, the range you have assigned contain too many steps! Please reduce the range of steps by "
            "increasing the multiplier or decrease the date difference")
        exit()
    else:
        average_stock_price = [element["vw"] for element in json_data["results"]]
        the_date_milliseconds = [element["t"] for element in json_data["results"]]
        human_readable_date = [datetime.datetime.fromtimestamp(element / 1000).strftime('%Y-%m-%d %H:%M:%S') for element
                               in the_date_milliseconds]
        data = {
            'Time': pd.to_datetime(human_readable_date),
            f'Average Stock Price of the {timespan}': average_stock_price
        }
        return pd.DataFrame(data)


st.title("Wonjoon's Stock Graph")
st.caption(
    "Welcome to my page! However, please keep that in mind that this uses a free API from polygon.io, "
    "therefore if you make too many request under one minute, the program might not function. "
    "Also, please keep that in mind that using multi chart is one API call per selection!")

dict_stocks_ticker = {"Apple Inc.": "AAPL",
                      "Microsoft Corporation": "MSFT",
                      "Amazon.com, Inc.": "AMZN",
                      "Google LLC": "GOOGL",
                      "Facebook, Inc.": "FB",
                      "Tesla, Inc.": "TSLA",
                      "Berkshire Hathaway Inc.": "BRK.B",
                      "Johnson & Johnson": "JNJ",
                      "Walmart Inc.": "WMT",
                      "Visa Inc.": "V"}

st.subheader("Select the company")
stocksTicker_select = st.radio(
    "What stock price do you want to see?",
    [key for key in dict_stocks_ticker.keys()])

st.subheader("Select the time period")

end_date_select = st.date_input("When should be the end date?",
                                datetime.datetime.now() - datetime.timedelta(days=1),
                                max_value=datetime.datetime.now() - datetime.timedelta(days=1))
st.write("The end date is", end_date_select)

# Due to the limitation of free API, I can only request information within 2years
start_date_select = st.date_input("When should be the start date?", datetime.date(2024, 1, 1),
                                  min_value=datetime.datetime.now() - datetime.timedelta(days=730),
                                  max_value=end_date_select)
st.write("The start date is", start_date_select)

st.subheader("Select the time increment")
timespan_select = st.select_slider(
    'Select the timespan',
    options=['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'],
    value='day')
st.write('You selected timespan as ', timespan_select)

st.subheader("Select the multiplier for the timespan")
timespan_multiplier_select = st.number_input('Enter the timespan multiplier', 1, step=1)
st.write('Timespan multiplier is:', timespan_multiplier_select)

if "user_input" or "name_of_company" or "list_of_inputs" not in st.session_state:
    st.session_state["user_input"] = ""
    st.session_state["name_of_company"] = ""
    st.session_state["list_of_inputs"] = ""

if st.button("Save", type="primary"):
    try:
        st.session_state["name_of_company"] = stocksTicker_select
        st.session_state["user_input"] = generate_stock_pd_dataframe(
            dict_stocks_ticker,
            stocksTicker_select,
            timespan_multiplier_select,
            timespan_select,
            start_date_select,
            end_date_select, "0"
        )
        st.write(st.session_state["user_input"])
        st.session_state["list_of_inputs"] = [dict_stocks_ticker,
                                              stocksTicker_select,
                                              timespan_multiplier_select,
                                              timespan_select,
                                              start_date_select,
                                              end_date_select]

    except KeyError as e:
        st.error(f"Saving error have occurred: Please refresh the page and try again")
        st.session_state["user_input"] = ""
        st.session_state["name_of_company"] = ""
        st.session_state["list_of_inputs"] = ""
    else:
        st.write("Your choice have been saved, now navigate to different page to view your results")
        st.page_link("pages/Page_1_-_Table_Generator.py", label="Table", icon="📊")
        st.page_link("pages/page_2_-_Chart_Generator.py", label="Chart", icon="📈")
        st.page_link("pages/page_3_-_Chart_With_Multi_Select.py", label="Multi Chart", icon="📈")
