"""
This is a page 3
Author: Wonjoon Jun
Date: Mar 25, 2024
Please view README.md for more information.
"""
import streamlit as st
import pandas as pd
import datetime
from requests import get


# It is little different from the main page
def generate_stock_dictionary(dict_stocks_ticker_: dict, stocks_ticker_select: str, timespan_multiplier_select: int,
                              timespan_select: str,
                              start_date_select: datetime, end_date_select: datetime,
                              key: str) -> dict:
    if key == "0":
        key = st.secrets["API_KEY_3"]
    stocks_ticker = dict_stocks_ticker_[stocks_ticker_select]
    multiplier = timespan_multiplier_select
    timespan = timespan_select
    from_date = start_date_select
    to_date = end_date_select
    try:
        json_data = get(
            f"https://api.polygon.io/v2/aggs/ticker/{stocks_ticker}/range/{multiplier}/"
            f"{timespan}/{from_date}/{to_date}?apiKey={key}").json()
    except Exception:
        st.error("Failed to call API")
        raise RuntimeError
    else:
        if json_data["status"] == "ERROR":
            st.write("Too many request were created, maximum request is 5 per minute, try again a minute later")
            raise RuntimeError
        elif json_data["status"] == "NOT_AUTHORIZED":
            st.write(
                "Sorry, the range you have assigned contain too many steps! Please reduce the range of steps"
                " by increasing the multiplier or decrease the date difference")
            raise RuntimeError
        else:
            average_stock_price = [element["vw"] for element in json_data["results"]]
            the_date_milliseconds = [element["t"] for element in json_data["results"]]
            human_readable_date = [datetime.datetime.fromtimestamp(element / 1000).strftime('%Y-%m-%d %H:%M:%S') for
                                   element
                                   in the_date_milliseconds]
            data = dict(zip(human_readable_date, average_stock_price))
            return data


st.header("Welcome to the Multi Select Chart Generator")
try:
    list_of_user_input = st.session_state["list_of_inputs"]
except KeyError:
    st.error('The requested key does not exist in the session state.\n'
             'Please go back to the main page to save your preference')
    st.page_link("Mainpage.py", label="Home", icon="🏠")
    exit()
except AssertionError:
    st.error('The session does not contain information, please go back to the main page to save your preference')
    st.page_link("Mainpage.py", label="Home", icon="🏠")
    exit()
except Exception:
    st.error("Unknown error have occurred please contact junwonjoon41@gmail.com, if the error persists")
    raise RuntimeError
else:
    st.subheader("Which company would you like to compare?")
    st.subheader("(choose up to 3)")

    options = st.multiselect(
        'Select the prices that you want to compare',
        [keys for keys in list_of_user_input[0].keys()],
        default=list_of_user_input[1], max_selections=3, )

    if st.button("Generate plot"):
        dfs = []  # List to store DataFrames
        for item in options:
            try:
                df = generate_stock_dictionary(list_of_user_input[0], item, list_of_user_input[2],
                                               list_of_user_input[3],
                                               list_of_user_input[4], list_of_user_input[5])
            except IndexError:
                st.error("Please go back to the main page to save the perimeter for the graph.")
            except KeyError:
                st.error("Couldn't load the entire dataset. There is currently a problem loading the full set of API")
            except Exception:
                st.error("Refresh the page please. "
                         "Unknown error have occurred. Please contact junwonjoon41@gmail.com, if the error persists")
                raise RuntimeError
            else:
                dfs.append(df)
        keys = list(dfs[0].keys())
        # This line and below is from chatGPT
        try:
            data_for_df = {f'Series{i}': [d[key] for key in keys] for i, d in enumerate(dfs)}
        except KeyError:
            st.write("Error in converting the data, please try again a minute later!")
            raise RuntimeError
        except Exception:
            st.error("Refresh the page please. "
                     "Unknown error have occurred. Please contact junwonjoon41@gmail.com, if the error persists")
            raise RuntimeError
        else:
            df = pd.DataFrame(data_for_df, index=pd.to_datetime(keys))
            st.line_chart(df)
            st.write(f"series{i} = {options[i]}" for i in range(len(options)))
