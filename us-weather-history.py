## streamlite template
## use line below to install streamlit
## pip install streamlt
## Documentation is below
## https://www.streamlit.io/
## run app in command line: 
## streamlit run your_script.py

## basic libraries for processing data and plotting graphs
import pandas as pd
import numpy as np
import streamlit as st
import datetime
import random
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import time

import warnings
warnings.filterwarnings("ignore")

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

matplotlib.rc('font', **font)

cities = {"KCLT": 'Charlotte, NC', "KCQT": "Los Angeles, CA", "KHOU": "Houston, TX", "KIND":"Indianapolis, IN", "KJAX": "Jacksonville, FL", "KMDW":"Chicago, IL", "KNYC":"New York, NY", "KPHL": "Philadelphia, PA","KPHX":"Phoenix, AZ", "KSEA":"Seattle, WA"}

##  helper functions with cache
@st.cache(persist=True)
def explore_csv():
    df = pd.read_csv('df.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['GroupName','date'], inplace=True, ascending=True)
    return df


# plot data
@st.cache(persist=True, allow_output_mutation=True)

def fig1(df, cols, y, GroupName):
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

    df_1 = df.copy(deep=True)
    df_1[y] = df_1[y].apply(lambda x:x.month)

    pal1 = sns.cubehelix_palette(10, rot=0.6,dark=0.3, light=.7)
    pal2 = sns.cubehelix_palette(10, rot=-0.2,dark=0.3, light=.7)

    g = sns.FacetGrid(df_1[df_1['GroupName']==GroupName], row=y, hue=y, aspect=15, height=.5, palette=pal1, legend_out=True)
    
    for col in cols:
        g.map(sns.kdeplot, col, bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=1.5, legend=True)
        g.map(sns.kdeplot, col, clip_on=False, color="w", lw=2, bw_adjust=.5, legend=True)
        
    g.map(plt.axhline, y=0, lw=2, clip_on=False)

    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .15, label, fontweight="bold", color=color, ha="left", va="center", transform=ax.transAxes, fontsize=20)
    
    
    g.map(label, 'actual_max_temp')

    g.fig.subplots_adjust(hspace=-.25)
    title = cols[0].split('_')

    g.axes[0,0].set_title(title[0].capitalize()+' '+title[2].capitalize()+' Maximum and Minimum Distributions for Months between Jul. 2014 to Jun. 2015')
    for i in range(1,12):
        g.axes[i,0].set_title("")
    g.axes[11,0].set_xlabel("Temperature")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)
    g.fig.set_size_inches(15,15)

    return g

@st.cache(persist=True, allow_output_mutation=True)
def fig2(df, g_name):
    df_g = df.copy(deep=True)
    df_g = df_g[df_g['GroupName']==g_name]

    actual=go.Candlestick(x=df_g['date'], open=df_g['actual_max_temp'], high=df_g['actual_max_temp'], low=df_g['actual_min_temp'], close=df_g['actual_min_temp'], increasing_line_color= 'cyan', decreasing_line_color= 'cyan', hoverinfo = 'skip', showlegend=True, legendgroup='Actual', name= 'Actual')

    average = go.Candlestick(x=df_g['date'], open=df_g['average_max_temp'], high=df_g['average_max_temp'], low=df_g['average_min_temp'], close=df_g['average_min_temp'], increasing_line_color= 'lightcoral', decreasing_line_color= 'lightcoral', hoverinfo = 'skip', showlegend=True, legendgroup='Average', name= 'Average')

    recorded=go.Candlestick(x=df_g['date'], open=df_g['record_max_temp'], high=df_g['record_max_temp'], low=df_g['record_min_temp'], close=df_g['record_min_temp'], hoverinfo = 'skip', increasing_line_color= 'gray', decreasing_line_color= 'gray', showlegend=True, legendgroup='Recorded', name= 'Recorded')
    
    figSignal = go.Figure(data=[recorded, average, actual])
    
    figSignal.update_layout( margin=dict(l=20, r=20, t=20, b=20), width=1200, height=600, 
                        xaxis=go.layout.XAxis(linecolor = 'black', linewidth = 1, mirror = True,fixedrange = False, rangeslider={'visible':False},
                                              showticklabels=True, tickvals=pd.date_range('2014-07', '2015-06', freq='MS'),
                        title_text='Recorded vs Actual Temperature at '+cities[g_name]))
    return figSignal

@st.cache(persist=True, allow_output_mutation=True)
def fig3(df, g_name):
    df_p = df.copy(deep=True)
    df_p = df_p[['date', 'actual_precipitation','average_precipitation','record_precipitation']]
    df_p = df_p[df['GroupName']==g_name]
    fig, ax = plt.subplots(1,1,figsize=(15,12))
    sns.lineplot(data=df_p, linewidth=2.5, ax=ax)
    ax.set_title("Recorded, Actual and Average Percipitation from Jul. 2014 to Jun. 2015 in "+cities[g_name])
    ax.legend(frameon=False)
    ax.set_ylabel("Percipitation (inches)")
    ax.set_xlabel("Date")
    plt.show()
    return fig

#loading datarames
df  = explore_csv()

## Header image
st.title('US Weather')

st.write("""
The data is a collection of weather data for the US cities of Charlotte (NC), Los Angeles (CA), Houston (TX), Indianapolis (IN), Jacksonville (FL), Chicago (IL), New York (NY), Philadelphia (PA), Phoenix(AZ) and Seattle (WA) for the dates between July 2014 to June 2015. The data shows:
- The maximum, minimum and average temperatures measured each day.
- The maximum, minimum and average temperatures recorded historically.
- The measured, historically recorded and average rain fall for each day.

""")

st.header('Choose City')
feats1 = ['KCLT', 'KCQT', 'KHOU', 'KIND', 'KJAX', 'KMDW', 'KNYC', 'KPHL', 'KPHX', 'KSEA']
box1 = st.selectbox("Select Location of Crime", options = feats1)
st.write('You selected:', box1)


# plotting matplotlib/sns graphs
st.write('The plot below explores the distribution of the minimum and maximum measured temperature for each month. It shows a greater dispersion of in the colder months when compared with the months closer in the summer season.')
st.pyplot(fig1(df, ['actual_min_temp', 'actual_max_temp'], 'date', box1))


st.markdown('\n')

st.write("The plot below shows a candle chart with maximum and minimum temperature represented in each stick. The grey graph is the historical minimum and maximum values, these are compared with the overall minimum and maximum average and measured on-the-day temperatures represented by the red and cyan graphs respectively. When the cyan graphs breaks through the grey boarder it means the a new record minimum or maximum temperature was measured on that day.")
st.plotly_chart(fig2(df, box1))

st.write("The plot below shows the average, historical record and measured on-the-day rainfall in the selected city")
st.pyplot(fig3(df, box1))

st.markdown('\n')
