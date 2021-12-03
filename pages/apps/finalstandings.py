# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 20:23:35 2021

@author: kevinse
"""

import streamlit as st
import pandas as pd

def app():
    x=pd.read_csv(f'https://raw.githubusercontent.com/kseymour1996/Fantasy-Football/master/Data/finalstandings.csv')
    y=pd.read_csv(f'https://raw.githubusercontent.com/kseymour1996/Fantasy-Football/master/Data/YoYRecords.csv')
    years=[2021,2020,2019,2018,2017,2016,2015,2014]
    selected_year=st.sidebar.selectbox('Year',years)
    df=x[(x['Year']==selected_year)]
    df=df.drop(df.columns[[0]],axis=1)
    df=df.replace('matt Last Name','Cole Grabowski')
    df=df.replace('Cole  Grabowski','Cole Grabowski')
    df=df.replace('Brad beisel','Brad Beisel')
    df=df.replace('brad beisel', 'Brad Beisel')
    df=df.replace('Kyle Putz','Kyle Markowiak')
    df=df.replace('kenneth gehl','Mitchell Gehl')
    df=df.sort_values(by=['Final Standing'], ascending=True)
    st.markdown("""
                ###
                Here are this year's standings
    
                """)
    st.dataframe(df)
    
    df2=y[(y['Year']==selected_year)]
    df2=df2.drop(df2.columns[[0]],axis=1)
    df2=df2.replace('matt Last Name','Cole Grabowski')
    df2=df2.replace('Cole  Grabowski','Cole Grabowski')
    df2=df2.replace('Brad beisel','Brad Beisel')
    df2=df2.replace('brad beisel', 'Brad Beisel')
    df2=df2.replace('Kyle Putz','Kyle Markowiak')
    df2=df2.replace('kenneth gehl','Mitchell Gehl')
    df2=df2.sort_values(by=['Points For'], ascending=False)
    df3=df2.sort_values(by=['Points Against'],ascending=False)
    df4=df2[(df2['Final Standing']==1)]
    tempdf1=pd.DataFrame(df2.iloc[0]).astype(str)
    tempdf2=pd.DataFrame(df3.iloc[0]).astype(str)
    tempdf3=pd.DataFrame(df4.iloc[0]).astype(str)
    # st.write("""
    #          ###
    #          League Champion:
    #              """)
    # st.dataframe(tempdf3)
    # st.write("""
    #          Most Points Scored:""")
    # st.dataframe(tempdf1)
    # st.write("""
    #          Most Points Against:""")
    # st.dataframe(tempdf2)

    st.write("""
             ###
             League Champion, Most Points Scored, and Most Points Against:
                 """)
    col1,col2,col3=st.columns([3,3,3])
    col1.write(tempdf3)
    col2.write(tempdf1)
    col3.write(tempdf2)