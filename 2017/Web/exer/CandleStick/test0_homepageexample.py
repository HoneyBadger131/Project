import plotly.plotly as py
import plotly.graph_objs as go

import pandas_datareader.data as web
from datetime import datetime
df = web.DataReader("TSLA",'google',datetime(2016,1,1),datetime(2017,6,1))

trace = go.Candlestick(x=df.index, open=df.Open, high=df.High, low = df.Low, close = df.Close)
data = [trace]

import plotly
plotly.offline.plot(data, filename='simple_candle')