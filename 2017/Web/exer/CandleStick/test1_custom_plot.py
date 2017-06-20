import plotly.plotly as py
import plotly.graph_objs as go
import plotly

from datetime import datetime
import pandas_datareader.data as web

df = web.DataReader("TSLA", 'google', datetime(2013, 10, 1), datetime(2016, 4, 1))

trace = go.Candlestick(x=df.index,
                       open = df.Open,
                       high = df.High,
                       low = df.Low,
                       close = df.Close,
                       increasing = dict(line=dict(color = '#17BECF')),
                       decreasing = dict(line=dict(color = '#7F7F7F'))
                       )

data = [trace]
layout = {
    'title': 'Tesla Run',
    'yaxis': {'title':'Tesla Motors Stock'},
    'shapes': [{
        'x0' : '2013-12-12', 'x1':'2013-12-12',
        'y0' : 0, 'y1':1, 'xref': 'x', 'yref':'paper',
        'line':{'color':'rgb(30,30,30)','width':1}
    }],
    'annotations': [{
        'x': '2013-12-12', 'y': 0.05, 'xref': 'x', 'yref': 'paper',
        'showarrow': False, 'xanchor': 'left',
        'text': 'Official start of the recession'
    }]
}

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig,filename='candle_annotation2.html')