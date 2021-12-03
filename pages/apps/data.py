# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 15:41:02 2021

@author: kevinse
"""
import streamlit as st
import pandas as pd
import warnings
from pandas.core.common import SettingWithCopyWarning
import matplotlib.pyplot as plt
import plotly.express as px
from espn_api.football import League
import numpy as np


def app():
    st.title('Year in Review')

    st.markdown("""
                This is for showing the start/sit accuracies for each owner in the selected season
                """)
    st.sidebar.header('User Input')
    ownerlist=['Kevin Seymour',
     'Cole  Grabowski',
     'kenneth gehl',
     'Brad beisel',
     'Robby Donarski',
     'Matthew Rabiega',
     'Kyle Markowiak',
     'Erik Seymour',
     'Mitchell Schlidt',
     'Tyler Knapp']
    selected_team=st.sidebar.selectbox('Team',ownerlist)
    
    yearlist=[2021,2020,2019,2018,2017,2016,2015,2014]
    selected_year=st.sidebar.selectbox('Year',yearlist)

    if (selected_year==2021 or selected_year==2020 or selected_year==2019):
        testdf=pd.read_csv(f'https://raw.githubusercontent.com/kseymour1996/Fantasy-Football/master/Data/FFData{selected_year}.csv')
        testdf=testdf.iloc[: , 1:]
        testdf.loc[testdf.Position =='RB/WR/TE', 'Position']='FLEX'
        testdf.Position=pd.Categorical(testdf.Position,categories=['QB','RB','WR','TE','FLEX','D/ST','K','BE'])
        testdfactual=testdf.sort_values('Position')
        playerdata=pd.read_csv('https://raw.githubusercontent.com/kseymour1996/Fantasy-Football/master/Data/FantasyPros_Data.csv')
    
        accuracydf=[]
        startersdf=[]
        subsetdflist=[]
        ownerlist=testdfactual['Owner'].unique().tolist()
        allaccuracy=[]
        # owner='Erik Seymour'
    
        for owner in ownerlist:
            allaccuracy=[]
            q=1
            while q<12:
                
                ES=testdfactual.loc[(testdfactual['Owner']==owner)&(testdfactual['Week']==q)]
                ES['Starter or bench']=['Bench' if x=='BE' else 'Starter' for x in ES['Position']]
                ES=pd.merge(ES,playerdata[['Player','Position Eligibility']], on='Player',how='left')
                ES=ES.reindex(columns=['Position Eligibility','Starter or bench','Position','Player','Score','Owner','Week','Year'])
                
                
                
                # df=pd.read_excel(r'\\ds\home\kevinse\Desktop\Python Testing\Scripts\FF\lineuptest.xlsx')
                subsetdf=ES.loc[ES['Starter or bench']=='Starter']
                subsetdf=subsetdf.sort_values(by=['Score'],ascending=False)
                subsetdf.Position=pd.Categorical(subsetdf.Position,categories=['QB','RB','WR','TE','FLEX','D/ST','K'])
                subsetdf=subsetdf.sort_values('Position')
                subsetdf = subsetdf[subsetdf['Position Eligibility'].notna()]
                subsetdflist.append(subsetdf)
                
                x=ES[['Position Eligibility','Starter or bench','Position','Player','Score','Owner','Week','Year']].values.tolist()
                
                rblist=[]
                
                for l in x:
                    y=l[0]
                    if y=='RB/FLEX':
                        rblist.append(l)
                        
                rblist=sorted(rblist, key=lambda x: x[4],reverse=True)
                starterrb=rblist[:2]
                flexlist=rblist[2:]
                
                qblist=[]
                
                for l in x:
                    y=l[0]
                    if y=='QB':
                        qblist.append(l)
                        
                qblist=sorted(qblist, key=lambda x: x[4],reverse=True)
                starterqb=qblist[:1]
                
                wrlist=[]
                
                for l in x:
                    y=l[0]
                    if y=='WR/FLEX':
                        wrlist.append(l)
                        
                wrlist=sorted(wrlist, key=lambda x: x[4],reverse=True)
                starterwr=wrlist[:2]
                extrawr=wrlist[2:]
                for z in extrawr:
                    flexlist.append(z)
                # flexlist.append(wrlist[2:])
                
                telist=[]
                
                for l in x:
                    y=l[0]
                    if y=='TE/FLEX':
                        telist.append(l)
                        
                telist=sorted(telist, key=lambda x: x[4],reverse=True)
                starterte=telist[:1]
                flexlist.append(telist[1:])
                
                klist=[]
                
                for l in x:
                    y=l[0]
                    if y=='K':
                        klist.append(l)
                        
                klist=sorted(klist, key=lambda x: x[4],reverse=True)
                starterk=klist[:1]
                
                dlist=[]
                
                for l in x:
                    y=l[0]
                    if y=='D/ST':
                        dlist.append(l)
                        
                dlist=sorted(dlist, key=lambda x: x[4],reverse=True)
                starterd=dlist[:1]
                
                flexlist=flexlist[:-1]
                flexlist=sorted(flexlist, key=lambda x: x[4],reverse=True)
                starterflex=flexlist[:1]
                
                
                starters=[]
                starters.append(starterqb[0])
                starters.append(starterrb[0])
                starters.append(starterrb[1])
                starters.append(starterwr[0])
                starters.append(starterwr[1])
                starters.append(starterte[0])
                starters.append(starterflex[0])
                starters.append(starterd[0])
                starters.append(starterk[0])
                starters=pd.DataFrame(starters)
                starters.columns=['Position Eligibility','Starter or bench','Position','Name','Score','Owner','Week','Year']
                
                    
                t1=sorted(subsetdf['Player'].values.tolist())
                t2=sorted(starters['Name'].values.tolist())
                startersdf.append(starters)
                t=[]
                for i in t2:
                    if i in t1:
                        # print(i)
                        t.append(i)
                
                accuracy=round(((len(t)/9)*100),2)
                accuracy=str(accuracy)
                # print('Your Start/Sit Accuracy is '+accuracy+' %.')
                # accuracy = len([t1[i] for i in range(0, len(t1)) if t1[i] == t2[i]]) / len(t1)
                # accuracy=round((accuracy*100),2)
                # accuracy=str(accuracy)
                # print('Your Start/Sit Accuracy is '+accuracy+' %.')
                allaccuracy.append(float(accuracy))
                q+=1
            
            # print(sum(allaccuracy)/11)
            df=pd.DataFrame({'Owner':owner,'Percentage':(sum(allaccuracy)/11)}, index=[[0]])
            accuracydf.append(df)
    
        startersdf=pd.concat(startersdf)
        subsetdflist=pd.concat(subsetdflist)
    
        #plotting pie chart
        accuracydf=pd.concat(accuracydf)
    
    
        st.dataframe(accuracydf.loc[accuracydf['Owner']==selected_team])
        xdf=pd.DataFrame(accuracydf.loc[accuracydf['Owner']==selected_team])
        xdf['Diff']=100-xdf['Percentage']
    
# =============================================================================
#         Inserting the schedule matrix
# ============================================================================
        x=pd.read_csv(f'https://raw.githubusercontent.com/kseymour1996/Fantasy-Football/master/Data/ScheduleMatrix{selected_year}.csv')
        x=x.rename(columns={'Unnamed: 0':'Index'})
        x=x.set_index('Index')
    
    
        # =============================================================================
        # Plotting the bar chart with actual vs 'perfect' scores
        # =============================================================================
        boxscores=pd.read_excel(f'https://raw.githubusercontent.com/kseymour1996/Fantasy-Football/master/Data/weeklymatchups.csv')
        ##### need to get this for each individual year. right now it is only basing it off of 2021.
        ##### also need to rerun when the season is over to get all the weeks data.
        weeks=[1,2,3,4,5,6,7,8,9,10,11,12,13]
        df7=[]
        for week in weeks:
            owner=selected_team
            df3=subsetdflist.loc[(subsetdflist['Owner']==owner)&(subsetdflist['Week']==week)]
            df3=df3[['Owner','Score']]
            
            df4=startersdf.loc[(startersdf['Owner']==owner)&(startersdf['Week']==week)]
            df4=df4[['Owner','Score']]
            
            p=boxscores.loc[(boxscores['Home Team']==selected_team)|(boxscores['Away Team']==selected_team)]
            p=p.loc[p['Week']==week]
            
            #### find a way to get the opposing team, and then get the opposing team score
            if p['Home Team'].iloc[0]==selected_team:
                opposing_team=p['Away Team'].iloc[0]
            else:
                opposing_team=p['Home Team'].iloc[0]
            
            
            df6=subsetdflist.loc[(subsetdflist['Owner']==opposing_team)&(subsetdflist['Week']==week)]
            df6=df6[['Owner','Score']]
            
            df5=pd.DataFrame({'Actual':sum(df3['Score']),'Perfect':sum(df4['Score']),'Opponent':sum(df6['Score']),'Week':week},index=[0])
            df7.append(df5)
        # df3=subsetdf[['Owner','Score']]
        # df4=starters[['Owner','Score']]
        # df5=pd.DataFrame({'Actual':sum(df3['Score']),'Perfect':sum(df4['Score']),'Week':q-1},index=[0])
        # df5.set_index('Week', inplace=True)
    
    
        # =============================================================================
        # Work on incorporating this into the loop with lists in order to get each person's starter lists 
        ### in order to update the chart effectively
        #### find a way to get opponent score in there as well
        # =============================================================================
    
        df7=pd.concat(df7)
        bar_chart=px.bar(df7,x='Week',y=['Actual','Perfect','Opponent'],title='Actual Points vs Hypothetical Points vs Opponent Points')
        bar_chart.update_layout(barmode='group')
        bar_chart.update_layout(yaxis_range=[0,200])
        st.plotly_chart(bar_chart)
        st.write('"Vs. Other Schedules". Read Left to Right.')
        st.dataframe(x)
        # st.bar_chart(df5)
    elif (selected_year!=2021 or selected_year!=2020 or selected_year!=2019):
        st.write("Data is not available for this year.")
