# IEE 555- Programming for Analytics
# Homework 7- Online data

# Seyed Hamed Ghodsi
# Miti Dilipbhai Patel

# ---------------------------------------------------------------------------------------

# Source(s):  
# The webpage:
# https://rapidapi.com/theapiguy/api/free-nba?endpoint=apiendpoint_0c94f219-1d0f-4fc1-8bbb-c5ee6b8327cc
# The URL: "https://free-nba.p.rapidapi.com/stats"

# ----------------------------------------------------------------------------------------

# Import needed packages
import json                                # convert the raw data to json 
import requests                            # To retrieve the data from API
import pandas as pd                        # To build the data frame from json data
import matplotlib.pyplot as plt            # To plot 

# Note that maybe packages requests and json are not installed in your python. 
# To install them you can write these commands in your windows terminal:
# pip install json
# pip install requests

# ----------------------------------------------------------------------------------------

headers = {
    'x-rapidapi-host': "free-nba.p.rapidapi.com",
    'x-rapidapi-key': "215bb899b8mshca9fc34ad929fd9p1883fdjsn411beeb306d0"
    }

url_stats   = "https://free-nba.p.rapidapi.com/stats"
# Reference : https://rapidapi.com/theapiguy/api/free-nba?endpoint=apiendpoint_0c94f219-1d0f-4fc1-8bbb-c5ee6b8327cc

# ----------------------------------------------------------------------------------------

# To find the number of total pages
querystring = {"page":"1","per_page":"100"}
stats = requests.request("GET", url_stats, headers=headers, params=querystring)
stats_json = stats.json()
#print (len(stats_json['data']))
totalPages = stats_json['meta']['total_pages']
print('There are', totalPages, 'pages of data.')
	
# ----------------------------------------------------------------------------------------

# To build a dynamic querystring for retrieving data from the original website
totalPages = 50
querystring = dict()
for j in range(1,totalPages+1):
    querystring [j] = {"page":j,"per_page":"100"}

# To build one comprehensive framework which contains all datasets we can retrieve from those 50 (total pages) pages. 
stats_df = pd.DataFrame()
for j in range(1,totalPages+1):
    
    if (j in range(0,totalPages+1,10)):    
        print('page', j , 'is uploading. Maximum page number is:', totalPages)
        
    stats = requests.request("GET", url_stats, headers=headers, params=querystring[j])
    stats_json = stats.json()

    rows1 = []
    for i in range(0,len(stats_json['data'])):
        flatDict = {}

        for key1 in stats_json['data'][i].keys():        
            if (type(stats_json['data'][i][key1]) is dict):           
                for key2 in stats_json['data'][i][key1].keys():               
                    newKey = key1 + key2                
                    flatDict[newKey] = stats_json['data'][i][key1][key2]
            else:
                flatDict[key1] = stats_json['data'][i][key1]

        rows1.append(flatDict)
    
    stats_df = stats_df.append(pd.DataFrame(rows1))

# ----------------------------------------------------------------------------------------

# To interpret the results:

# see the columns
#stats_df.columns

#find the best players in five skills. 
cols = ['playerfirst_name','playerlast_name','pts', 'ast','reb', 'stl','blk','teamfull_name', 'gameseason', 'id']

pts = stats_df [stats_df.pts == stats_df.pts.max()][cols]
pts ['Criteria'] = 'Point'

ast = stats_df [stats_df.ast == stats_df.ast.max()][cols]
ast ['Criteria'] = 'Assist'

reb = stats_df [stats_df.reb == stats_df.reb.max()][cols]
reb ['Criteria'] = 'Rebound'

stl = stats_df [stats_df.stl == stats_df.stl.max()][cols]
stl ['Criteria'] = 'Steal'

blk = stats_df [stats_df.blk == stats_df.blk.max()][cols]
blk ['Criteria'] = 'Block'

# To build the result table
table_df = pts.append(ast).append(reb).append(stl).append(blk)
table_df.set_index('Criteria')

# ----------------------------------------------------------------------------------------
# To plot the distribution of number of players 

# import matplotlib.pyplot as plt
# %matplotlib inline

df = stats_df [stats_df.pts>=0]['pts']
print('Number of players which their points are recorded:', len(df))

df2 = stats_df [stats_df.pts>0]['pts']
print('Number of players which scored at least one point in a game:', len(df2))

plt.hist(df2, bins=int(stats_df.pts.max()));

plt.gca().set(title='Points', ylabel='Number of players');
plt.savefig('hw7_histogram.jpg')
plt.show()
