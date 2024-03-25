import streamlit as st
from requests import get
import datetime
import pandas as pd

def generate_stockdictionary(dict_stocksTicker:dict, timespan_multiplier_select:int, timespan_select:str,
                   start_date_select:datetime, end_date_select:datetime) -> dict:
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
        # st.write(json_data)
        average_stock_price = [element["vw"] for element in json_data["results"]]
        the_date_miliseconds = [element["t"] for element in json_data["results"]]
        human_readable_date = [datetime.datetime.fromtimestamp(element / 1000).strftime('%Y-%m-%d %H:%M:%S') for element in the_date_miliseconds]
        # st.write(average_stock_price)
        # st.write(human_readable_date)
        data = {
        'Time': pd.to_datetime(human_readable_date),
        f'Average Stock Price of the {timespan}': average_stock_price
        }
        return pd.DataFrame(data)

st.title("Stock Price!")
dict_stocksTicker ={"Apple Inc.": "AAPL",
                    "Microsoft Corporation": "MSFT",
                    "Amazon.com, Inc.": "AMZN",
                    "Google LLC": "GOOGL",
                    "Facebook, Inc.": "FB",
                    "Tesla, Inc.": "TSLA",
                    "Berkshire Hathaway Inc.": "BRK.B",
                    "Johnson & Johnson": "JNJ",
                    "Walmart Inc.": "WMT",
                     "Visa Inc.": "V"}

# key = st.secrets["API_KEY"]
key = "c4NLm5QgWNWDBWp530A_Ypnxc6PHmmtD"
stocksTicker_select = st.radio(
    "What stock price do you want to see?",
    [key for key in dict_stocksTicker.keys()])

end_date_select = st.date_input("When should be the end date?", 
                                datetime.datetime.now() - datetime.timedelta(days=1), 
                                max_value= datetime.datetime.now() - datetime.timedelta(days=1))
st.write("The end date is", end_date_select)

#Due to the limitation of free API, I can only request information within 2years
start_date_select = st.date_input("When should be the start date?", datetime.date(2024, 1, 1), 
                                  min_value= datetime.datetime.now() - datetime.timedelta(days=730),
                                  max_value= end_date_select)
st.write("The start date is", start_date_select)



timespan_select = st.select_slider(
    'Select the timespan',
    options=['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'],
    value=('day'))
st.write('You selected timespan as ', timespan_select)


timespan_multiplier_select = st.number_input('Enter the timespan multiplier', 1, step = 1)
st.write('Timespan multiplier is:', timespan_multiplier_select)

if st.button("Generate Chart", type="primary"):
    data = generate_stockdictionary(dict_stocksTicker, timespan_multiplier_select, timespan_select,start_date_select, end_date_select)
    df = pd.DataFrame(data)
    df.set_index('Time', inplace=True)
    st.line_chart(df, color = '#ef4423')






