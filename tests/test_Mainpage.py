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


# If you want to test the program
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

    def test_generate_stock_pd_dataframe(self):
        number_of_stocks_google = generate_using_generate_stock_pd_dataframe_google()["count"]
        number_of_stocks_apple = generate_using_generate_stock_pd_dataframe_apple()["count"]
        assert number_of_stocks_google == number_of_stocks_apple
