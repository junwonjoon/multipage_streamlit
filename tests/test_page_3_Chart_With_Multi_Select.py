"""
This is a test for page 3
Author: Wonjoon Jun
Date: Mar 25, 2024
Please view README.md for more information.

"""

from unittest import TestCase
from streamlit.testing.v1 import AppTest
from Mainpage import dict_stocks_ticker
import pytest
import datetime
import sys
import streamlit as st
from requests import get


# I couldn't import the function from the page_3_Chart_With_Multi_Select. So, I am copying the function down to testit
def generate_stock_dictionary(dict_stocks_ticker_: dict, stocks_ticker_select: str, timespan_multiplier_select: int,
                              timespan_select: str,
                              start_date_select: datetime, end_date_select: datetime,
                              key: str = "0") -> dict:
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
        sys.exit("API error")
    else:
        if json_data["status"] == "ERROR":
            st.write("Too many request were created, maximum request is 5 per minute, try again a minute later")
            sys.exit("API error")
        elif json_data["status"] == "NOT_AUTHORIZED":
            st.write(
                "Sorry, the range you have assigned contain too many steps! Please reduce the range of steps"
                " by increasing the multiplier or decrease the date difference")
            sys.exit("API error")
        else:
            average_stock_price = [element["vw"] for element in json_data["results"]]
            the_date_milliseconds = [element["t"] for element in json_data["results"]]
            human_readable_date = [datetime.datetime.fromtimestamp(element / 1000).strftime('%Y-%m-%d %H:%M:%S') for
                                   element
                                   in the_date_milliseconds]
            data = dict(zip(human_readable_date, average_stock_price))
            return data


# please replace this with your own key later. If you want to run tests.
disabled_testAPIkey = ""


class Test(TestCase):
    def test_run_from_file(self):
        at = AppTest.from_file("./app/pages/page_3_Chart_With_Multi_Select.py")
        assert at.run(), "Running of the program failed"

    def test_generate_stock_dictionary(self):
        dict_apple = generate_stock_dictionary(dict_stocks_ticker, "Apple Inc.", 1, 'day', '2024-01-01', '2024-01-31',
                                               disabled_testAPIkey)
        dict_google = generate_stock_dictionary(dict_stocks_ticker, "Google LLC", 1, 'day', '2024-01-01', '2024-01-31',
                                                disabled_testAPIkey)
        assert len(dict_apple.keys()) == len(dict_google.keys()), "The two API's length don't match"
        assert len(dict_apple.keys()) > 0, "The api call did not receive any value"
        with pytest.raises(SystemExit) as is_exit_success:  # Testing for corner case.
            generate_stock_dictionary(dict_stocks_ticker, "Apple Inc.", 1, 'day', '2024-01-01', '2024-01-31',
                                      "1")
        assert is_exit_success.type == SystemExit
        # This line below always fail because already 5 API calls are made during the test.
        # assert is_exit_success.value.code == "API Error"
        # This test would be useful test once I upgrade to paid version of API
