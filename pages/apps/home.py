# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 15:40:03 2021

@author: kevinse
"""

import streamlit as st
from espn_api.football import League
import pandas as pd

def app():
    st.markdown("## Oak Creek Fantasy Football League 2021")

    # Upload the dataset and save as csv
    st.markdown("### Use the sidebar to navigate to different apps") 
    st.write("\n")
    st.markdown("""
                ###
                ###
                All Time Standings:
                    """)
    
    #League ID will stay the same, change to the year you want
    league_id = 325857
    year = [2014,2015,2016,2017,2018,2019,2020,2021]
    teamStatslist=[]
    for x in year:
        league=League(league_id,x,espn_s2='AEA%2BOoISMFi3VyPnASwDn%2BI0nkKqrlc7wg69aEWg5J7xnVq6YVgI1g0LWsqcrN98plE1rgGA4NsGUgamwATuemg4Cw03a8%2FeQuHy5b2zmIsfnnjz%2F4hDfWR%2BnWwhEadhlHatG9vlRlNHxmEmTZuoZlKm6aSBGKYOYve3p7FNixgPhemWxcv4BPhzbFxDtetloODvlJ1B%2FZTgnqStZj8h8YtWkNUbqojvHzn81JvKMslzXOovT6zrNCJLChcL1oYYMNVtpxbX7Mh59D7m8cDQ8eGpcbaLD7UFrNPecKosHX4kDQ%3D%3D',
                      swid='{C227829A-0F4B-444C-949A-C736AE0EC19E}')
        
        #Grabs List of Owners, teams, wins, losses
        owner_list=[]
        team_list=[]
        winslist=[]
        losslist=[]
        tielist=[]
        standings=[]
        PF=[]
        PA=[]
        i=0
        while i<10:
            owner1=league.draft[i].team.owner
            owner_list.append(owner1)
            team1=league.draft[i].team.team_name
            team_list.append(team1)
            wins1=league.draft[i].team.wins
            winslist.append(wins1)
            losses1=league.draft[i].team.losses
            losslist.append(losses1)
            tie1=league.draft[i].team.ties
            tielist.append(tie1)
            standing1=league.draft[i].team.final_standing
            standings.append(standing1)
            PF1=league.draft[i].team.points_for
            PF.append(PF1)
            PA1=league.draft[i].team.points_against
            PA.append(PA1)
            i+=1
              
        #create dataframe
        teams={'Owners':owner_list,'Team Name':team_list,'Wins':winslist,'Losses':losslist,'Ties':tielist,
               'Final Standing':standings,'Points For':PF,'Points Against':PA,'Year':x}
        teams=pd.DataFrame(teams)
        teams['Margin']=teams['Points For']-teams['Points Against']
        teams['Year']=x
        teamStatslist.append(teams)
        # print(teams)
        
    teamStats=pd.concat(teamStatslist)
    #cleaning up data, making it so same owner is replicated
    teamStats=teamStats.replace('matt Last Name','Cole Grabowski')
    teamStats=teamStats.replace('Cole  Grabowski','Cole Grabowski')
    teamStats=teamStats.replace('Brad beisel','Brad Beisel')
    teamStats=teamStats.replace('brad beisel', 'Brad Beisel')
    teamStats=teamStats.replace('Kyle Putz','Kyle Markowiak')
    teamStats=teamStats.replace('kenneth gehl','Mitchell Gehl')

    #Getting Summary Statistics
    subsetdf=teamStats.groupby("Owners")["Wins","Losses","Ties","Points For","Points Against","Margin"].sum()
    subsetdf['Winning %']=(subsetdf['Wins']/(subsetdf['Wins']+subsetdf['Losses']+subsetdf['Ties']))
    subsetdf['AVG PF']=(subsetdf['Points For']/(subsetdf['Wins']+subsetdf['Losses']+subsetdf['Ties']))
    subsetdf['AVG PA']=(subsetdf['Points Against']/(subsetdf['Wins']+subsetdf['Losses']+subsetdf['Ties']))
    # subsetdf['AVG Margin']=(subsetdf['Margin']/(subsetdf['Wins']+subsetdf['Losses']+subsetdf['Ties']))
    SummaryStats=subsetdf.sort_values(by=['Wins'], ascending=False)
    SummaryStats.drop(['Points For', 'Points Against','Margin'], axis=1, inplace=True)
    
    st.dataframe(SummaryStats)