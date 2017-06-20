import plotly.plotly as py
import plotly.graph_objs as go

from datetime import datetime
import pandas_datareader.data as web


df = web.DataReader("aapl",'google',datetime(2016,1,1),datetime(2017,1,1))
print(df)
#df = web.DataReader("078930.KS", 'yahoo',
#                    datetime(2015, 1, 1),
#                    datetime(2016, 7, 1))

#df2 = web.DataReader('AAPL', 'google', '2016-06-25', '2016-06-30')

data = [go.Scatter(x=df.index, y=df.High)]

py.iplot(data)
py.show()