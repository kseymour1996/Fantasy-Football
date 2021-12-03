# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 15:38:26 2021

@author: kevinse
"""

import streamlit as st

# Custom imports 
from multipage import MultiPage
from apps import home,data,finalstandings # import your pages here

# Create an instance of the app 
app = MultiPage()
st.set_page_config(layout="wide")

# Title of the main page
st.title("Fantasy Football Data Application")

# Add all your applications (pages) here
app.add_page("Home", home.app)
app.add_page("Year End Review", data.app)
app.add_page("Final Standings",finalstandings.app)
# app.add_page("Machine Learning", machine_learning.app)
# app.add_page("Data Analysis",data_visualize.app)
# app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()