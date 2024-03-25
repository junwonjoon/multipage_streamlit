"""
This is a test for main page
Author: Wonjoon Jun
Date: Mar 25, 2024
Please view README.md for more information.
"""
from unittest import TestCase
from streamlit.testing.v1 import AppTest
class Test(TestCase):
    def test_ui_title_and_header(self):
        at = AppTest.from_file("./app/Mainpage.py")
        at.run()
        assert True


