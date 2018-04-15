import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

def get_list_of_university_towns():
    
    l=[]
    an=[]
    with open("university_towns.txt",'r') as f:
        for q in f:
            l.append(q)
    st=''
    #print(l)
    for va in l:
        #print(va)
        i=va.find("[edit]")
        if i>-1:
            st=va[:i]
        else:
            j=va.find("(")
            if j>-1:
                an.append([st,va[:j-1]])
    #print(an)
    labels=['State','RegionName']
    df1=pd.DataFrame.from_records(an,columns=labels)
    return df1

def get_recession_start():
    df=pd.read_excel("gdplev.xls",skiprows=219)
    df=df[['1999q4',12323.3]]
    df.columns=['Year','GDP']
    ans=''
    #print(df)
    for i in range(1,len(df)-2):
        #plt.plot(df.iloc[i-1]['Year'][:4],df.iloc[i-1]['GDP'],'bo');
        if df.iloc[i-1]['GDP']>df.iloc[i]['GDP'] and df.iloc[i+1]['GDP']>df.iloc[i+2]['GDP']:
            ans=df.iloc[i-1]['Year']
    
    #plt.show()
    return ans
tt=get_recession_start()

def get_recession_end():
    df=pd.read_excel("gdplev.xls",skiprows=219)
    df=df[['1999q4',12323.3]]
    df.columns=['Year','GDP']
    ans=''
    #print(df)
    begin=get_recession_start()
    for i in range(int(df[df['Year']==begin].index.values),len(df)-2):
        if df.iloc[i]['GDP']<df.iloc[i+1]['GDP'] and df.iloc[i+1]['GDP']<df.iloc[i+2]['GDP']:
            ans=df.iloc[i+2]['Year']
            break
    return ans

def get_recession_bottom():
    df=pd.read_excel("gdplev.xls",skiprows=219)
    df=df[['1999q4',12323.3]]
    df.columns=['Year','GDP']
    ans=''
    begin=get_recession_start()
    end=get_recession_end()
    mini=1000000000
    for i in range(int(df[df['Year']==begin].index.values),int(df[df['Year']==end].index.values)):
        if mini>df.iloc[i]['GDP']:
            mini=df.iloc[i]['GDP']
            ans=df.iloc[i]['Year']
    return ans

def convert_housing_data_to_quarters():
   
    col=1
    da=pd.read_csv("City_Zhvi_AllHomes.csv")
    
    da.replace({'State':states},inplace=True)
    for year in range(2000,2016):
        da[str(year)+'q1']=da[[str(year)+'-01',str(year)+'-02',str(year)+'-03']].mean(axis=col)
        da[str(year)+'q2']=da[[str(year)+'-04',str(year)+'-05',str(year)+'-06']].mean(axis=col)
        da[str(year)+'q3']=da[[str(year)+'-07',str(year)+'-08',str(year)+'-09']].mean(axis=col)
        da[str(year)+'q4']=da[[str(year)+'-10',str(year)+'-11',str(year)+'-12']].mean(axis=col)
    da['2016'+'q1']=da[[str(year)+'-01',str(year)+'-02',str(year)+'-03']].mean(axis=col)
    da['2016'+'q2']=da[[str(year)+'-04',str(year)+'-05',str(year)+'-06']].mean(axis=col)
    da['2016'+'q3']=da[[str(year)+'-07',str(year)+'-08',str(year)+'-09']].mean(axis=col)
    da.set_index(['State','RegionName'],inplace=True)
    da.drop(da.columns[list(range(0,249,1))],axis=1,inplace=True)
    
    return da
