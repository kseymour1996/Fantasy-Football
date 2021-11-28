# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 09:08:07 2021

@author: kevinse
"""

import pandas as pd
import warnings
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
#League ID will stay the same, change to the year you want

testdf=pd.read_excel(r'\\ds\home\kevinse\Desktop\Python Testing\Scripts\FF\FFData2021.xlsx')
testdf=testdf.iloc[: , 1:]
testdf.loc[testdf.Position =='RB/WR/TE', 'Position']='FLEX'
testdf.Position=pd.Categorical(testdf.Position,categories=['QB','RB','WR','TE','FLEX','D/ST','K','BE'])
testdfactual=testdf.sort_values('Position')
playerdata=pd.read_csv(r'\\ds\home\kevinse\Desktop\Python Testing\Scripts\FF\FantasyPros_Data.csv')

accuracydf=[]
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
        t=[]
        for i in t2:
            if i in t1:
                # print(i)
                t.append(i)
        
        accuracy=round(((len(t)/9)*100),2)
        accuracy=str(accuracy)
        print('Your Start/Sit Accuracy is '+accuracy+' %.')
        # accuracy = len([t1[i] for i in range(0, len(t1)) if t1[i] == t2[i]]) / len(t1)
        # accuracy=round((accuracy*100),2)
        # accuracy=str(accuracy)
        # print('Your Start/Sit Accuracy is '+accuracy+' %.')
        allaccuracy.append(float(accuracy))
        q+=1
    
    print(sum(allaccuracy)/11)
    df=pd.DataFrame({'Owner':owner,'Percentage':(sum(allaccuracy)/11)}, index=[[0]])
    accuracydf.append(df)

accuracydf=pd.concat(accuracydf)