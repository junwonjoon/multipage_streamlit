"""
This is a test for main page
Author: Wonjoon Jun
Date: Mar 25, 2024
Please view README.md for more information.
"""
from unittest import TestCase
from streamlit.testing.v1 import AppTest
from Mainpage import generate_stock_pd_dataframe, dict_stocks_ticker

disabled_testAPIkey = "kehuG_96JtRHMrLsocZ10qjzqwHlSpsp"  # please replace this with your own key later.


def generate_using_generate_stock_pd_dataframe_apple():
    return generate_stock_pd_dataframe(dict_stocks_ticker, "Apple Inc.", 1, 'day', '2024-01-01', '2024-01-31',
                                       disabled_testAPIkey)


def generate_using_generate_stock_pd_dataframe_google():
    return generate_stock_pd_dataframe(dict_stocks_ticker, "Google LLC", 1, 'day', '2024-01-01', '2024-01-31',
                                       disabled_testAPIkey)


class Test(TestCase):
    def test_run_from_file(self):
        at = AppTest.from_file("./app/Mainpage.py")
        assert at.run()

    def test_dict_stocks_ticker_value(self):
        test_dict = {"Apple Inc.": "AAPL",
                     "Microsoft Corporation": "MSFT",
                     "Amazon.com, Inc.": "AMZN",
                     "Google LLC": "GOOGL",
                     "Facebook, Inc.": "FB",
                     "Tesla, Inc.": "TSLA",
                     "Berkshire Hathaway Inc.": "BRK.B",
                     "Johnson & Johnson": "JNJ",
                     "Walmart Inc.": "WMT",
                     "Visa Inc.": "V"}
        for boolean_value in [test_dict[keys] == dict_stocks_ticker[keys] for keys in test_dict.keys()]:
            assert boolean_value

    def test_generate_stock_pd_dataframe(self):
        df_google = generate_using_generate_stock_pd_dataframe_google()
        df_apple = generate_using_generate_stock_pd_dataframe_apple()
        assert len(df_google['Time']) == len(df_apple['Time'])
        assert len(df_google['Time']) > 0
