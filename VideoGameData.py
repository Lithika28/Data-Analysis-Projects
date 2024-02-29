#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis on Video Game Dataset

# In[1]:


#Let's start off by importing our necessary Python libraries
import numpy as np # for linear algebra
import pandas as pd # for data preparation
import plotly.express as px # for data visualization
from textblob import TextBlob # for sentiment analysis
from datetime import date # for date-time-conversion

df = pd.read_csv('all_video_games(cleaned).csv') #Metacritic Video Game Dataset from Kaggle
df.shape

#Kaggle Source: https://www.kaggle.com/datasets/beridzeg45/video-games/data


# In[2]:


df.columns


# In[3]:


df.head()


# Let's clean up this table a little more. Clearing out all rows with NaN values as this would not really allow us to analyze the User Ratings of the video games by setting it to 0 instead.

# In[4]:


df = df.fillna(0)


# In[5]:


df


# ### Let's start analyzing the video game data

# In[6]:


z1 = df.groupby(['Product Rating']).size().reset_index(name='counts')
pieChart = px.pie(z1,values='counts', names='Product Rating',title='Distribution of Product Ratings', color_discrete_sequence=px.colors.qualitative.Set3)
pieChart.show()


# As shown by the Pie Chart, a majority of content released this year is rated T for Teen. What about genres? 

# In[7]:


df['Genres'] = df['Genres'].fillna('No Genre Specified') #Taking care of the NaN
filtered_genres = pd.DataFrame()
filtered_genres = df['Genres'].str.split(' ',expand=True).stack()
filtered_genres = filtered_genres.to_frame()
filtered_genres.columns=['Genres']
genres=filtered_genres.groupby(['Genres']).size().reset_index(name='Total Content')
genres=genres.sort_values(by=['Total Content'], ascending=False)
genresTop=genres.head()
genresTop=genresTop.sort_values(by=['Total Content'])
fig1=px.bar(genresTop, x='Total Content', y='Genres',  title='Top 5 Genres')
fig1.show()
genresTop20 = genres.head(20)
fig2 = px.pie(genresTop20,values='Total Content', names='Genres',title='Distribution of the Top 20 Genres', color_discrete_sequence=px.colors.qualitative.Set3)
fig2.show()


# As show above the top genres are Action and Adventure. With Action leading with a total of 2595 games falling the category. Adventure following with 1686 games, RPG in third with 1055 games, Sim in fourth with 1023 games and 2D games in fifth with 1013 games.

# As shown by the following pie chart though the action genre had the most games we can see that it only accounts for 16.6% of the top 20 genres.

# ### Let's look at the Developers

# What about the developers? Which companies were the most prolific? 

# In[8]:


df['Developer'] = df['Developer'].fillna('No Dev. Specified') #Taking care of the NaN
DfDevs = pd.DataFrame()
DfDevs = df['Developer']
DfDevs = DfDevs.to_frame()
DfDevs.columns=['Developer']
Devs=DfDevs.groupby(['Developer']).size().reset_index(name='Total Content')
Devs=Devs.sort_values(by=['Total Content'], ascending=False)
DevsTop=Devs.head(10)
DevsTop=DevsTop.sort_values(by=['Total Content'])
fig3=px.bar(DevsTop, x='Total Content', y='Developer',  title='Top 10 Developers')
fig3.show()


# As shown Nintendo is the most prolific game developer. 

# ### Let's take a look at User Ratings

# Let's look into the most popular game and the highest rated game for the year (2023) in recent gaming history. The most popular game takes into account both the user score and the user ratings count. Whereas the highest rated games just looks at the user score. 

# In[41]:


#Let's convert these Release Date strings into Datetime objects first
df['Release Date'] = pd.to_datetime(df['Release Date'])
recent_games = df.copy()
recent_games = recent_games[df['Release Date'].dt.year == 2023]

recent_games['Total Ratings'] = recent_games['User Score']*recent_games['User Ratings Count']
recent_games = recent_games.dropna()
fig4 = px.scatter(recent_games, x='User Score', y='User Ratings Count',size="Total Ratings", color='Title', log_x=True, size_max=60,title='Most Popular Games of the Year')
fig4.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=-1,
    xanchor="right",
    x=1
))

fig4.show(render='iframe')


# Based on the graph we can see that when looking at Total Ratings, User Score, and User Ratings Count. For the year 2023, the game Baldur's Gate 3, out did all other games. Most interesting parts of this graph include Starfield which had a lower User Score but a large amount of ratings. Indicating that a lot of people played the game but did not feel as good about it compared to other games. IT should also be noted that while Marvel's Spider-Man 2 had a higher rating than Baldur's Gate 3 did not have nearly as much reviews.

# It should also be noted that Baldur's Gate 3 won Game of the Year! A few of the nominees are also visible in this particular data set (Alan Wake 2, Resident Evil 4, and Marvel's Spider-man 2). As seen by the following table a little more clearly. 
# 
# Sources: 
# https://thegameawards.com/nominees/game-of-the-year

# In[10]:


recent_games=recent_games.sort_values(by=['Total Ratings', 'User Score', 'User Ratings Count'], ascending=False)
recent_games.head(10)

