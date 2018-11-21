# -*- coding:UTF-8 -*-
import math

from pymongo import MongoClient

import plotly.offline as py
from plotly.graph_objs import Scatter, Layout, Pie, Figure
import plotly.graph_objs as go

# 数据库的连接
client = MongoClient('localhost', 27017)
db = client.bilibili
bilibili_video = db.video  # collection

data_vid = []
data_view = []
data_like = []
data_size = []
for video in bilibili_video.find():
    view = video['view']
    vid = video['aid']
    like = video['like']
    if view != '--':
        data_vid.append(vid)
        data_view.append(view)
        data_like.append(like)
        data_size.append(1 if like == 0 else int(math.log(like, 2)))

py.init_notebook_mode(connected=True)

less_than_500 = []
less_than_1000 = []
less_than_10000 = []
ten_k_plus = []
for v in data_view:
    if v < 500:
        less_than_500.append(v)
    elif v < 1000:
        less_than_1000.append(v)
    elif v < 10000:
        less_than_10000.append(v)
    else:
        ten_k_plus.append(v)

dataset = {
    'labels': ['<500', '501~1000', '1001~10000', '10000+'],
    'values': [len(less_than_500), len(less_than_1000), len(less_than_10000), len(ten_k_plus)]
}

data_g = []
p = Pie(
    labels=dataset['labels'],
    values=dataset['values']
)

data_g.append(p)
layout = Layout(title='pie charts')
fig = Figure(data=data_g, layout=layout)
py.plot(fig, filename='hasaki')

# trace1 = go.Scatter(
#     x=data_vid,
#     y=data_view,
#     marker=dict(
#         size=data_size
#     ),
#     mode='markers'
# )
#
# py.plot([trace1])
