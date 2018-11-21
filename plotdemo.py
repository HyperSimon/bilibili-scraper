import plotly.offline as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go

py.init_notebook_mode(connected=True)

trace1 = go.Scatter(
    x=[101, 2],
    y=[1, 2],
    mode='markers'
)

py.plot([trace1])
