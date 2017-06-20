import plotly

from plotly.graph_objs import Scatter, Layout

print(plotly.__version__)

plotly.offline.plot({
    "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": Layout(title="hello world")
})




#출처: http://hamait.tistory.com/800 [HAMA 블로그]