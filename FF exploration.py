# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 08:18:36 2021

@author: kevinse
"""


# =============================================================================
# Actual Starting Code
# =============================================================================
from espn_api.football import League
import pandas as pd
#League ID will stay the same, change to the year you want
league_id = 325857
year = [2014,2015,2016,2017,2018,2019,2020,2021]
teamStatslist=[]
for x in year:
    league=League(league_id,2021,espn_s2='AEA%2BOoISMFi3VyPnASwDn%2BI0nkKqrlc7wg69aEWg5J7xnVq6YVgI1g0LWsqcrN98plE1rgGA4NsGUgamwATuemg4Cw03a8%2FeQuHy5b2zmIsfnnjz%2F4hDfWR%2BnWwhEadhlHatG9vlRlNHxmEmTZuoZlKm6aSBGKYOYve3p7FNixgPhemWxcv4BPhzbFxDtetloODvlJ1B%2FZTgnqStZj8h8YtWkNUbqojvHzn81JvKMslzXOovT6zrNCJLChcL1oYYMNVtpxbX7Mh59D7m8cDQ8eGpcbaLD7UFrNPecKosHX4kDQ%3D%3D',
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

#Getting Summary Statistics
subsetdf=teamStats.groupby("Owners")["Wins","Losses","Ties","Points For","Points Against","Margin"].sum()
subsetdf['Winning %']=(subsetdf['Wins']/(subsetdf['Wins']+subsetdf['Losses']+subsetdf['Ties']))
subsetdf['AVG PF']=(subsetdf['Points For']/(subsetdf['Wins']+subsetdf['Losses']+subsetdf['Ties']))
subsetdf['AVG PA']=(subsetdf['Points Against']/(subsetdf['Wins']+subsetdf['Losses']+subsetdf['Ties']))
# subsetdf['AVG Margin']=(subsetdf['Margin']/(subsetdf['Wins']+subsetdf['Losses']+subsetdf['Ties']))
SummaryStats=subsetdf.sort_values(by=['Wins'], ascending=False)


# =============================================================================
# Draft stats
# =============================================================================
year = [2014,2015,2016,2017,2018,2019,2020,2021]
AllDraftHistory=[]
i=0
for x in year:
    league=League(league_id,x,espn_s2='AEA%2BOoISMFi3VyPnASwDn%2BI0nkKqrlc7wg69aEWg5J7xnVq6YVgI1g0LWsqcrN98plE1rgGA4NsGUgamwATuemg4Cw03a8%2FeQuHy5b2zmIsfnnjz%2F4hDfWR%2BnWwhEadhlHatG9vlRlNHxmEmTZuoZlKm6aSBGKYOYve3p7FNixgPhemWxcv4BPhzbFxDtetloODvlJ1B%2FZTgnqStZj8h8YtWkNUbqojvHzn81JvKMslzXOovT6zrNCJLChcL1oYYMNVtpxbX7Mh59D7m8cDQ8eGpcbaLD7UFrNPecKosHX4kDQ%3D%3D',
                  swid='{C227829A-0F4B-444C-949A-C736AE0EC19E}')
    d=league.draft
    playerpicks=[]
    namelist=[]
    i=0
    while i<len(d):
        name=league.draft[i].playerName
        playerpicks.append(name)
        o=league.draft[i].team.owner
        namelist.append(o)
        i+=1
        
    drafthistory={"Owners":namelist,"Players":playerpicks}
    drafthistory=pd.DataFrame(drafthistory)
    drafthistory['Year']=x
    drafthistory['Pick #']=drafthistory.index +1
    AllDraftHistory.append(drafthistory)
    
drafthistory=pd.concat(AllDraftHistory)
drafthistory=drafthistory.replace('matt Last Name','Cole Grabowski')
drafthistory=drafthistory.replace('Cole  Grabowski','Cole Grabowski')
drafthistory=drafthistory.replace('Brad beisel','Brad Beisel')
drafthistory=drafthistory.replace('brad beisel', 'Brad Beisel')

playerpos=drafthistory['Players'].tolist()
# =============================================================================
# player information
# =============================================================================
testlist=[]
year=2020
league=League(league_id,year,espn_s2='AEA%2BOoISMFi3VyPnASwDn%2BI0nkKqrlc7wg69aEWg5J7xnVq6YVgI1g0LWsqcrN98plE1rgGA4NsGUgamwATuemg4Cw03a8%2FeQuHy5b2zmIsfnnjz%2F4hDfWR%2BnWwhEadhlHatG9vlRlNHxmEmTZuoZlKm6aSBGKYOYve3p7FNixgPhemWxcv4BPhzbFxDtetloODvlJ1B%2FZTgnqStZj8h8YtWkNUbqojvHzn81JvKMslzXOovT6zrNCJLChcL1oYYMNVtpxbX7Mh59D7m8cDQ8eGpcbaLD7UFrNPecKosHX4kDQ%3D%3D',
              swid='{C227829A-0F4B-444C-949A-C736AE0EC19E}')
for player in playerpos:
    try:
        p=league.player_info(player).position
        testlist.append(p)
    except AttributeError:
        p='NAN'
        testlist.append(p)
        continue

position_df=pd.DataFrame({'Players':playerpos,'Position':testlist})
# NANCleanupList=position_df.loc[position_df['Position']=='NAN']
# NANCleanupList=NANCleanupList.sort_values(by=['Players'])

drafthistory=drafthistory.merge(position_df, on='Players', how='left')
drafthistory=drafthistory.drop_duplicates()
KM=drafthistory[(drafthistory['Owners']=='Brad Beisel')&(drafthistory['Players']=='Justin Tucker')]
JT=drafthistory[(drafthistory['Players']=='Travis Kelce')]
# =============================================================================
# Final Standings
# =============================================================================
year = [2014,2015,2016,2017,2018,2019,2020]
year=[2021]
finalstandings=[]
i=0

for x in year:
    league=League(league_id,x,espn_s2='AEA%2BOoISMFi3VyPnASwDn%2BI0nkKqrlc7wg69aEWg5J7xnVq6YVgI1g0LWsqcrN98plE1rgGA4NsGUgamwATuemg4Cw03a8%2FeQuHy5b2zmIsfnnjz%2F4hDfWR%2BnWwhEadhlHatG9vlRlNHxmEmTZuoZlKm6aSBGKYOYve3p7FNixgPhemWxcv4BPhzbFxDtetloODvlJ1B%2FZTgnqStZj8h8YtWkNUbqojvHzn81JvKMslzXOovT6zrNCJLChcL1oYYMNVtpxbX7Mh59D7m8cDQ8eGpcbaLD7UFrNPecKosHX4kDQ%3D%3D',
                  swid='{C227829A-0F4B-444C-949A-C736AE0EC19E}')
    t=league.teams
    testlist=[]
    names=[]
    i=0
    while i<len(league.teams):
        tm=league.teams[i].final_standing
        testlist.append(tm)
        tn=league.teams[i].owner
        names.append(tn)
        i+=1
    
    standings=pd.DataFrame({'Owners':names,'Final Standing': testlist,'Year':x})
    finalstandings.append(standings)
    
finalstandings=pd.concat(finalstandings)
    
# =============================================================================
# Gathering more information
# =============================================================================
test=drafthistory[drafthistory['Pick #'] <11]
test['concat']=test['Owners']+test['Year'].astype(str)
test2=finalstandings    
test2=test2.replace('matt Last Name','Cole Grabowski')
test2=test2.replace('Cole  Grabowski','Cole Grabowski')
test2=test2.replace('Brad beisel','Brad Beisel')
test2=test2.replace('brad beisel', 'Brad Beisel')
test2['concat']=test2['Owners']+test2['Year'].astype(str)    
test3=test.merge(test2, on='concat', how='left')    
test4=test3.drop(columns=['concat','Owners_y','Year_y'])
test5=test4.groupby('Pick #', as_index=False)['Final Standing'].mean().round(2)   
    
#separating into pick statistics
pickslots=test4.drop(columns=['Owners_x','Players','Year_x','Position'])
HighPlacement=pickslots.groupby(['Pick #'],as_index=False).min() 
LowPlacement=pickslots.groupby(['Pick #'],as_index=False).max()    
Overall= HighPlacement.merge(LowPlacement, on='Pick #')   
Overall=Overall.rename(columns={'Final Standing_x': 'Highest Finish','Final Standing_y': 'Lowest Finish'})
Overall=Overall.merge(test5)
Overall=Overall.rename(columns={'Final Standing': 'Average Finish'})

test6=drafthistory
test6['concat']=test6['Owners']+test6['Players']

test6=test6['concat'].value_counts().reset_index()

# =============================================================================
# Box Scores, only works 2019 onwards. work on 2014-2018 with scoreboard()
# =============================================================================
year = [2019,2020,2021]
boxscores=[]

# j=1
# bs=league.box_scores(1)


for x in year:
    league=League(league_id,x,espn_s2='AEA%2BOoISMFi3VyPnASwDn%2BI0nkKqrlc7wg69aEWg5J7xnVq6YVgI1g0LWsqcrN98plE1rgGA4NsGUgamwATuemg4Cw03a8%2FeQuHy5b2zmIsfnnjz%2F4hDfWR%2BnWwhEadhlHatG9vlRlNHxmEmTZuoZlKm6aSBGKYOYve3p7FNixgPhemWxcv4BPhzbFxDtetloODvlJ1B%2FZTgnqStZj8h8YtWkNUbqojvHzn81JvKMslzXOovT6zrNCJLChcL1oYYMNVtpxbX7Mh59D7m8cDQ8eGpcbaLD7UFrNPecKosHX4kDQ%3D%3D',
                  swid='{C227829A-0F4B-444C-949A-C736AE0EC19E}')
    i=0
    j=1
    while j<15:
        bs=league.box_scores(j)
    
        for b in bs:
            HS=bs[i].home_score
            AS=bs[i].away_score
            OwnHome=bs[i].home_team.owner
            OwnAway=bs[i].away_team.owner
            test7=pd.DataFrame({'Home Team':OwnHome,'Away Team':OwnAway,'Home Score': HS,'Away Score': AS,'Week':j,'Year':x}, index=[0])
            boxscores.append(test7)
            i+=1
        j+=1
        i=0
    
boxscores=pd.concat(boxscores)
# boxscores['Year']=year
boxscores=boxscores.reset_index(drop=True)
boxscores.loc[boxscores['Home Score']>boxscores['Away Score'],'Winning Team']=boxscores['Home Team']
boxscores.loc[boxscores['Home Score']<boxscores['Away Score'],'Winning Team']=boxscores['Away Team']
boxscores['Margin of Victory']=(boxscores['Home Score']-boxscores['Away Score']).abs()






# working on getting 2014-2018 data
year=[2014,2015,2016,2017,2018]
boxscores2=[]

for x in year:
    league=League(league_id,x,espn_s2='AEA%2BOoISMFi3VyPnASwDn%2BI0nkKqrlc7wg69aEWg5J7xnVq6YVgI1g0LWsqcrN98plE1rgGA4NsGUgamwATuemg4Cw03a8%2FeQuHy5b2zmIsfnnjz%2F4hDfWR%2BnWwhEadhlHatG9vlRlNHxmEmTZuoZlKm6aSBGKYOYve3p7FNixgPhemWxcv4BPhzbFxDtetloODvlJ1B%2FZTgnqStZj8h8YtWkNUbqojvHzn81JvKMslzXOovT6zrNCJLChcL1oYYMNVtpxbX7Mh59D7m8cDQ8eGpcbaLD7UFrNPecKosHX4kDQ%3D%3D',
                  swid='{C227829A-0F4B-444C-949A-C736AE0EC19E}')
    i=0
    j=1
    while j<15:
        bs=league.scoreboard(j)
    
        for b in bs:
            HS=bs[i].home_score
            AS=bs[i].away_score
            OwnHome=bs[i].home_team.owner
            OwnAway=bs[i].away_team.owner
            test7=pd.DataFrame({'Home Team':OwnHome,'Away Team':OwnAway,'Home Score': HS,'Away Score': AS,'Week':j,'Year':x}, index=[0])
            boxscores2.append(test7)
            i+=1
        j+=1
        i=0
    
boxscores2=pd.concat(boxscores2)
# boxscores['Year']=year
boxscores2=boxscores2.reset_index(drop=True)
boxscores2.loc[boxscores2['Home Score']>boxscores2['Away Score'],'Winning Team']=boxscores2['Home Team']
boxscores2.loc[boxscores2['Home Score']<boxscores2['Away Score'],'Winning Team']=boxscores2['Away Team']
boxscores2['Margin of Victory']=(boxscores2['Home Score']-boxscores2['Away Score']).abs()
boxscores2=boxscores2[boxscores2.Week <14]
boxscores2=boxscores2[:-5]

#merging two boxscores files
boxscores=pd.concat([boxscores,boxscores2])
boxscores['HighScore']=boxscores[['Home Score','Away Score']].max(axis=1)
boxscores['Total Points']=boxscores['Home Score']+boxscores['Away Score']
#getting rid of games that aren't played yet
boxscores=boxscores[boxscores['Total Points']!=0]


# =============================================================================
# Records
# =============================================================================
#highest weekly score
print(boxscores.loc[:, ['Home Score', 'Away Score']].max().max())
boxscores['Away Score'].nlargest(5)
boxscores.iloc[boxscores['Away Score'].idxmax()]
boxscores.nlargest(5, columns= ['Home Score','Away Score'])

#Highest Margin of Victory
boxscores.iloc[boxscores['Margin of Victory'].idxmax()]
boxscores['Margin of Victory'].nlargest(5)
boxscores.nlargest(5, columns= ['Margin of Victory'])

#try to get the lineups and scores of the highest and biggest margin
test=season2019.loc[(season2019['Week']==11) & (season2019['Owner']=='Cole Grabowski')]






#grabbing individual lineup
# i=0
# n=0
year = 2021
testlist=[]
weeks=[1,2,3,4,5,6]
# weeks=[13,14]
league=League(league_id,year,espn_s2='AEA%2BOoISMFi3VyPnASwDn%2BI0nkKqrlc7wg69aEWg5J7xnVq6YVgI1g0LWsqcrN98plE1rgGA4NsGUgamwATuemg4Cw03a8%2FeQuHy5b2zmIsfnnjz%2F4hDfWR%2BnWwhEadhlHatG9vlRlNHxmEmTZuoZlKm6aSBGKYOYve3p7FNixgPhemWxcv4BPhzbFxDtetloODvlJ1B%2FZTgnqStZj8h8YtWkNUbqojvHzn81JvKMslzXOovT6zrNCJLChcL1oYYMNVtpxbX7Mh59D7m8cDQ8eGpcbaLD7UFrNPecKosHX4kDQ%3D%3D',
              swid='{C227829A-0F4B-444C-949A-C736AE0EC19E}')
testdf=[]
for week in weeks:
    i=0
    n=0
    # testlist=[]
    while n<5:
        while i<16:
            try:
                tmnamea=league.box_scores(week)[n].away_team.owner
                namea=league.box_scores(week)[n].away_lineup[i].name
                ya=league.box_scores(week)[n].away_lineup[i].points
                sa=league.box_scores(week)[n].away_lineup[i].slot_position
                print(namea,ya,sa,tmnamea)
                testdfa=pd.DataFrame({'Player':namea,'Score':ya,'Position':sa,'Owner':tmnamea,'Week':week,'Year':year}, index=[0])
                tmnameh=league.box_scores(week)[n].home_team.owner
                nameh=league.box_scores(week)[n].home_lineup[i].name
                yh=league.box_scores(week)[n].home_lineup[i].points
                sh=league.box_scores(week)[n].home_lineup[i].slot_position
                print(nameh,yh,sh,tmnameh)
                testdfh=pd.DataFrame({'Player':nameh,'Score':yh,'Position':sh,'Owner':tmnameh,'Week':week,'Year':year}, index=[0])
                i+=1
                testlist.append(testdfa)
                testlist.append(testdfh)
            except IndexError:
                namea='null'
                ya='null'
                sa='null'
                testdfa=pd.DataFrame({'Player':namea,'Score':ya,'Position':sa,'Owner':tmnamea,'Week':week,'Year':year}, index=[0])
                i+=1
                testlist.append(testdfa)
                continue
        i=0
        n+=1


testdf=pd.concat(testlist)
testdf.Position=pd.Categorical(testdf.Position,categories=['QB','RB','WR','TE','RB/WR/TE','D/ST','K','BE'])
testdf=testdf.sort_values('Position')
import numpy as np
testdf=testdf.replace('null',np.NaN)




#ideas
#overall winnings (assuming $20 buy in)


#testing throwing into DB
import sqlite3
conn=sqlite3.connect('\\\\ds\\home\\kevinse\\Desktop\\Python Testing\\Scripts\\test.db')
boxscores.to_sql('Boxscores',conn,if_exists='replace',index=False)
pd.read_sql('select * from Boxscores',conn)
conn.close()








testdf.loc[(testdf['Owner']=='Kevin Seymour')&(testdf['Week']==6)]


for owner in owner_list:
    print(testdf.loc[(testdf['Owner']==owner)&(testdf['Week']==6)])
    print(owner+" Scored "+testdf.loc[(testdf['Owner']==owner)&(testdf['Week']==6)&(testdf['Position']!='BE')].groupby('Week').sum().Score.apply(str))
    






