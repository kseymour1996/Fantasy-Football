# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 18:16:44 2022

@author: kevinse
"""

import nflfastpy as nfl
import re
import pandas as pd
import numpy as np


df19 = nfl.load_pbp_data(2021)

df19penalty=df19[df19['desc'].str.contains('PENALTY')]
columns=['desc','receiver_player_name','passer_player_name','rusher_player_name']

df=df19penalty[columns]


#work in progress
# for row in df['desc']:
#     z=re.findall(r"[A-Z][a-z]+,?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+", row)
#     print(z)

#cleaning up dataset, getting rid of rows we dont need
df=df[~df['desc'].str.contains('Neutral Zone Infraction')]
df=df[~df['desc'].str.contains('TWO-POINT CONVERSION')]
df=df[~df['desc'].str.contains('Field Goal')]
df=df[~df['desc'].str.contains('False Start')]
df=df[~df['desc'].str.contains('punts')]
df=df[~df['desc'].str.contains('sacked')]
df=df[~df['desc'].str.contains('kicks')]
df=df[~df['desc'].str.contains('Delay of Game')]
df=df[~df['desc'].str.contains('extra point')]
df=df[~df['desc'].str.contains('field goal')]
df=df[~df['desc'].str.contains('Touchback')]
df=df[~df['desc'].str.contains('Too Many Men on Field')]
df=df[~df['desc'].str.contains('Illegal Substitution')]
df=df[~df['desc'].str.contains('Encroachment')]
df=df[~df['desc'].str.contains('Illegal Formation')]
df=df[~df['desc'].str.contains('Illegal Shift')]
df=df[~df['desc'].str.startswith('PENALTY on')]
df=df[~df['desc'].str.contains('Unsportsmanlike')]
df=df[~df['desc'].str.contains('spiked')]


#getting rid of declined penalties, incomplete passes
df=df[~df['desc'].str.contains('declined')]
#getting rid of defensive penalties (only want to find plays that cost OP yards)
df=df[~df['desc'].str.contains('defensive')]
df=df[~df['desc'].str.contains('Defensive')]
df=df[~df['desc'].str.contains('incomplete')]
#trying to get rid of of penalties that didnt matter in the outcome
df=df[~df['desc'].str.contains('enforced between downs')] ##check this one!!!
df=df[~df['desc'].str.contains('INTERCEPTED')]

#regex to get rid of leading whitespace, timestamps, and parenthesis
# df['desc']=re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>",(dfcopy['desc']))  
df['desc']=df['desc'].replace("([\(\[]).*?([\)\]])", "\g<1>\g<2>",regex=True)
df['desc']=df['desc'].replace("[()]",'',regex=True)
df['desc']=df['desc'].apply(lambda x: x.strip())

#getting rid of the number- before the player name
df['desc']=df['desc'].replace(r'\d+-','',regex=True)

df['Penalty Yardage']=df['desc'].str.findall(r"\d+ yards").str[0]
#converting to a number
df['Penalty Yardage']=df['Penalty Yardage'].str.replace('yards','')
df['Penalty Yardage']=df['Penalty Yardage'].fillna(0)
df['Penalty Yardage']=df['Penalty Yardage'].astype(int)

######putting a helper column for separating player names

#breaking out and assigning player names and positions

#putting a helper column for separating player names
#first fixing robby anderson and damien williams, formatting is odd
df['desc']=df['desc'].str.replace('Ro.Anderson','R.Anderson')
df['desc']=df['desc'].str.replace('Dam.Williams','D.Williams')
df['desc']=df['desc'].str.replace('Da.Williams','D.Williams')
df['desc']=df['desc'].str.replace('Dj.Moore','D.Moore')
df['desc']=df['desc'].str.replace('E.St. Brown','E.Brown')
df['desc']=df['desc'].str.replace('Aa.Rodgers','A.Rodgers')
df['desc']=df['desc'].str.replace('Mi.Carter','M.Carter')
df['desc']=df['desc'].str.replace('Ty.Taylor','T.Taylor')
df['playerhelper']=df['desc'].str.findall(r"[A-Z]\.[A-Za-z]+")


#list comprehensions to get the data we want into passer, receiver, and rusher columns

df['passer']=df.apply(lambda x: x['playerhelper'][0] if 'pass' in x['desc'] else None, axis=1)
df['receiver']=df.apply(lambda x: x['playerhelper'][1] if 'pass' in x['desc'] else None, axis=1)
df['rusher']=df.apply(lambda x: x['playerhelper'][0] if x['passer']==None else None, axis=1)
df['Skill Player']=df.apply(lambda x: x['receiver'] if x['receiver']!=None else x['rusher'],axis=1)

#we can now drop the columns we dont need:
df=df.drop(columns=['receiver_player_name','passer_player_name','rusher_player_name','playerhelper'])

#making columns for .5ppr passing FPTS, receiving FPTS, and rushing FPTS
df['PassingFPTS']=df.apply(lambda x: x['Penalty Yardage']*.04 if x['passer']!=None else 0,axis=1)
df['ReceivingFPTS']=df.apply(lambda x: x['Penalty Yardage']*.1+.5 if x['receiver']!=None else 0,axis=1)
df['RushingFPTS']=df.apply(lambda x: x['Penalty Yardage']*.1 if x['rusher']!=None else 0,axis=1)
df['Touchdown']=df.apply(lambda x: 6 if 'TOUCHDOWN' in x['desc'] else 0, axis=1)

#total points from play. 
df['PasserTotalPts']=df.apply(lambda x: x['PassingFPTS']+x['Touchdown'] if x['passer']!=None else 0, axis=1)
df['SkillPlayerTotalPts']=df.apply(lambda x: x['ReceivingFPTS']+x['RushingFPTS']+x['Touchdown'],axis=1)

# for i,row in df.iterrows():
#     if 'pass' not in row['desc']:
#         if len(row['playerhelper'])<2:
#            print(row)

df.groupby(['passer']).agg({'PasserTotalPts':'sum'})
x=df.groupby(['Skill Player']).agg({'SkillPlayerTotalPts':'sum'})


# # \d+ms
# for row in df['desc']:
#     z=re.findall(r"([A-Z].[A-Za-z]+)",row)
#     print(z)


# for row in df['desc']:
#     z=re.findall(r"[A-Z]\.[A-Za-z]+",row)
#     print(z)
