import pandas as pd

from miniProject.settings import BASE_DIR

from plotly.offline import plot
import plotly.graph_objs as go

df = pd.read_csv(BASE_DIR / "app/logic/Mumbai.csv")
df = df.replace(9,0)
def getCorrelationGraph():

    z = []

    table = df.corr()

    zMin = table.describe().loc['min'].min()

    list(table.iloc[0])
    len(df.columns)
    for i in range(0, len(df.columns)-1):
        z.append(list(table.iloc[i]))

    cols = list(df.columns)
    cols.pop(2)

    trace1 = {
    "uid": "0f0d45",
    "name": "trace 0",
    "type": "heatmap",
    "x": cols,
    "y": cols,
    "zmax": 1,
    "zmin": zMin,
    "z": z,
    "colorscale": [
        [0, "rgb(0,0,255)"], [0.1, "rgb(51,153,255)"], [0.2, "rgb(102,204,255)"], [0.3, "rgb(153,204,255)"], [0.4, "rgb(204,204,255)"], [0.5, "rgb(255,255,255)"], [0.6, "rgb(255,204,255)"], [0.7, "rgb(255,153,255)"], [0.8, "rgb(255,102,204)"], [0.9, "rgb(255,102,102)"], [1, "rgb(255,0,0)"]]
    }

    data = [trace1]

    layout = {
        "font": {
            "size": 12,
            "color": "#444",
            "family": "\"Open sans\", verdana, arial, sans-serif"
        },
        "meta": False,
        "title": {
            "font": {
                "size": 12,
                "color": "#444",
                "family": "\"Open sans\", verdana, arial, sans-serif"
            },
        },
        # "width": 600,
        "autosize" : True,
        "bargap": 0.2,
        "boxgap": 0.3,
        # "height": 440,
        "legend": {
            "font": {
                "size": 10,
                "color": '#ff0000',
                "family": "\"Open sans\", verdana, arial, sans-serif"
            },
            "bgcolor": "#fff",
            "traceorder": "normal",
            "bordercolor": "#444",
            "borderwidth": 0
        },
        "margin": {
            "b": 60,
            "l": 70,
            "r": 200,
            "t": 60,
            "pad": 2,
            "autoexpand": True
        },
        "barmode": "group",
        "boxmode": "overlay",
        # "autosize": False,
        "dragmode": "zoom",
        "hovermode": "x",
        "titlefont": {
            "size": 12,
            "color": '#ff0000',
            "family": "\"Open sans\", verdana, arial, sans-serif"
        },
        "separators": ".,",
        "bargroupgap": 0,
        "boxgroupgap": 0.3,
        "hidesources": False,
        "plot_bgcolor": "#fff",
        "paper_bgcolor": "#fff"
    }
    fig = go.Figure(data=data, layout=layout)

    return plot(fig, output_type='div', include_plotlyjs=False)

def getPriceArea():
    trace1  = {
        'x' : list(df['Area']),
        'y' : list(df['Price']),
    }

    data = go.Scatter(trace1,mode="markers")
    fig = go.Figure(data=data)
    fig.update_xaxes(title_text='Area')
    fig.update_yaxes(title_text='Price')

    return plot(fig, output_type='div', include_plotlyjs=False)

def getPriceRooms():

    temp = df[['No. of Bedrooms', 'Price']]
    t = temp.groupby(['No. of Bedrooms']).mean()
    x = []
    y = []
    for i in range(len(t)):
        x.append(t.iloc[i].name)
        y.append(t.iloc[i]['Price'])

    trace1  = {
        'x' : x,
        'y' : y,
    }

    data = go.Scatter(trace1)
    fig = go.Figure(data=data)
    fig.update_xaxes(title_text='No. of rooms')
    fig.update_yaxes(title_text='Price')

    return plot(fig, output_type='div', include_plotlyjs=False)