import pandas as pd
from collections import Counter, OrderedDict
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import sys

# GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS--GRAPHS

# Read DF
def read(path='games.csv'):
    df = pd.read_csv(path)
    df = df.dropna(axis=0, how='any')
    df = df[df['Year_of_Release'] >= 2000]
    # add some filtrations
    return df


# First plot
def first(df):
    platform = df.Platform.unique()
    plat = {}
    res1 = {}
    for i in platform:
        plat[i] = []
        res1[i] = {}

    for index, row in df.iterrows():
        plat[row[1]].append(int(row[2]))

    for pl in platform:
        d = plat[pl]
        d = dict(OrderedDict(sorted(Counter(d).items(), key=lambda t: t[0])))
        res1[pl]['years'] = list(d.keys())
        res1[pl]['num'] = list(d.values())

    plot = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="Выпуск игр по годам и платформам"),
        xaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            gridcolor='#bdbdbd',
            gridwidth=2,
            zerolinecolor='#969696',
            zerolinewidth=2,
            linecolor='#636363',
            linewidth=2,
            title='ГОД',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
                color='lightgrey'
            )),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            gridcolor='#bdbdbd',
            gridwidth=2,
            zerolinecolor='#969696',
            zerolinewidth=2,
            linecolor='#636363',
            linewidth=2,
            title='КОЛИЧЕСТВО ИГР',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
                color='lightgrey'
            ))))

    for name in platform:
        plot.add_trace(go.Scatter(
            name=name,
            x=res1[name]['years'],
            y=res1[name]['num'],
            stackgroup='one'
        ))
    return platform, plot


# Second plot
def second(df):
    genre = df.Genre.unique()
    res2 = {}
    for g in genre:
        res2[g] = {'crit': [], 'user': []}

    for index, row in df.iterrows():
        res2[row[3]]['crit'].append(float(row[4]))
        if row[5] != 'tbd':
            res2[row[3]]['user'].append(float(row[5]))
        else:
            res2[row[3]]['user'].append(0)

    plot1 = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="Оценки жанров"),
        xaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            gridcolor='#bdbdbd',
            gridwidth=2,
            zerolinecolor='#969696',
            zerolinewidth=2,
            linecolor='#636363',
            linewidth=2,
            title='ОЦЕНКИ ИГРОКОВ',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
                color='lightgrey'
            )),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            gridcolor='#bdbdbd',
            gridwidth=2,
            zerolinecolor='#969696',
            zerolinewidth=2,
            linecolor='#636363',
            linewidth=2,
            title='ОЦЕНКИ КРИТИКОВ',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
                color='lightgrey'
            ))))
    for name in genre:
        plot1.add_trace(go.Scatter(
            name=name,
            y=res2[name]['crit'],
            x=res2[name]['user'],
            mode='markers'
        ))
    return genre, plot1


# END-OF-GRAPHS--END-OF-GRAPHS--END-OF-GRAPHS--END-OF-GRAPHS--END-OF-GRAPHS--END-OF-GRAPHS--END-OF-GRAPHS--END-OF-GRAPHS


if len(sys.argv) != 1:
    df = read(sys.argv[1])
else:
    df = read()
platform, plot = first(df)
genre, plot1 = second(df)

# APP---APP--APP---APP--APP---APP--APP---APP--APP---APP--APP---APP--APP---APP--APP---APP--APP---APP--APP---APP--APP---APP
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# Create layout
app.layout = html.Div(

    children=[
        # Title
        dbc.Row([dbc.Col(html.H3("Gamesrank+"))], className="h-10", ),

        # Thematic break
        html.Hr(),

        # Description
        dbc.Row([dbc.Col(html.Div("Данный дашборд предназначен для анализа игр по жанрам, годам и платформам. "
                                  "Чтобы изменить выборку, уберите или добавьте галочку у нужной Вам платформы или "
                                  "жанра. "
                                  "Под фильтром платформ Вы можете видеть число анализируемых игр в настоящий момент. "
                                  "Внизу страницы вы можете изменить период годов выпуска игр."
                                  ))], className="h-15", ),

        # Filters
        dbc.Row(dbc.CardGroup([
            # Filter №1
            dbc.Card(
                dbc.CardBody(
                    dbc.Col(
                        children=[
                            html.Span("Выберите платформы:"),
                            dcc.Checklist(
                                id='select1',
                                options=[{'label': i, 'value': i} for i in platform],
                                value=[i for i in platform]
                            )]),
                ),
                className="w-40"
            ),
            # Filter №2
            dbc.Card(
                dbc.CardBody(
                    dbc.Col(
                        children=[
                            html.Span("Выберите жанры:"),
                            dcc.Checklist(
                                id='select2',
                                options=[{'label': i, 'value': i} for i in genre],
                                value=[i for i in genre]
                            )
                        ]
                    )),
                className="w-40"
            )]
        )),

        # Result of a filtration
        dbc.Row(
            dbc.Col(
                dbc.Alert(
                    [
                        "Количество выбранных игр (результат фильтрации): ",
                        html.A(id='number', href="#"),
                    ]
                ))
        ),

        # Graphs
        dbc.Row(children=[
            # First column
            dbc.Col(dcc.Graph(id="qty", figure=plot)),

            # Second column
            dbc.Col(dcc.Graph(id="rate", figure=plot1))
        ], className="h-300"),

        # Filter №3
        dbc.Row(children=[

            dbc.Col(

                html.Div([
                    "С: ",
                    dcc.Input(
                        id='from',
                        type='number',
                        placeholder='From',
                        value=2000,
                        min=2000,
                        max=2021),
                    "По: ",
                    dcc.Input(
                        id='to',
                        type='number',
                        placeholder='From',
                        value=2021,
                        min=2000,
                        max=2021)
                ]

                )
            ),
        ]

        )

    ])


@app.callback(
    [Output('qty', 'figure'),
     Output('rate', 'figure'),
     Output('number', 'children'),

     ],
    [Input('select1', 'value'),
     Input('select2', 'value'),
     Input('from', 'value'),
     Input('to', 'value'),
     ]
)
def update_second(platform, genre, frm, to):
    lst = [i for i in range(frm, to + 1)]
    df1 = df[df['Year_of_Release'].isin(lst)]
    df1 = df1[df1['Genre'].isin(genre)]
    df1 = df1[df1['Platform'].isin(platform)]
    num = len(df1)
    _, plot = first(df1)
    _, plot1 = second(df1)
    # num = f"Количество выбранных игр (результат фильтрации): {num}"
    return plot, plot1, num


# Run app
if __name__ == "__main__":
    app.run_server()
