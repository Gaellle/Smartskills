import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State

import pathlib
from app import app


############  DATAS ################

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

learn = pd.read_csv(DATA_PATH.joinpath('learn.csv'))
code = pd.read_csv(DATA_PATH.joinpath('code.csv'))
salary = pd.read_csv(DATA_PATH.joinpath('salary.csv'))
age = pd.read_csv(DATA_PATH.joinpath('age.csv'))


##############" PAGE SURVEY LAYOUT ##################

layout = html.Div([
                            html.Div(
                                    
                                dbc.Col([
                                    html.H1('Developer Experience Survey'),
                                    html.Br(),

                                    dbc.Row([

                                        dcc.Dropdown(
                                                                options=[{'label': c, 'value': c}
                                                                for c in list(salary.DevType.unique())],
                                                                value= 'Data Analyst',
                                                                id='dropdown-component',
                                                                style = {'width' : '350px'}

                                                                ),
                                    ], className='d-grid gap-2 d-flex justify-content-center'),                   

                                    html.Br(),
                                    dbc.Row([
                                        
                                        dbc.Container(
                                                        [
                                                        dcc.RadioItems(
                                                        options=[
                                                            {'label': ' Databases', 'value': 'data_df'},
                                                            {'label': ' Languages', 'value' : 'lang_df'},
                                                            {'label': ' Platforms', 'value' : 'plat_df'},
                                                            {'label': ' Webframes', 'value' : 'web_df'},
                                                            {'label': ' Tools', 'value' : 'tool_df'},
                                                            {'label': ' Others', 'value' : 'other_df'}],

                                                        id="radio-component",
                                                        className="date-group-items",
                                                        labelStyle={'display': 'inline-block', 'margin-right': '20px', 'color':'rgb(95, 70, 144)' },
                                                        value = 'lang_df',
                                                        style = {"padding": "10px", 'text-align': 'center'}    
                                                            ),
                                                        
                                                        html.P(id="output"),
                                                        ],
                                                        className='box', style={'padding-top':'25px', 'padding-bottom':'10px','width' : '80vw'}
                                                    ),

                                        dbc.Container(                                      
                                                    dcc.Graph(id='barplot', className='top-graph', config={'displayModeBar': False}) ,
                                                    className='box', style={'padding-top':'25px', 'padding-bottom':'10px','width' : '80vw','height' :'80vh'}
                                                    )
                                        
                                        ], className='d-grid gap-2 d-flex justify-content-center'),

                                    dbc.Row([    
                                        
                                        dbc.Col([
                                            
                                            # emplacement du graph sur ma page
                                            dbc.Container(
                                            dcc.Graph(id='pieplot',className='graph', config={'displayModeBar': False}),
                                                    className='box', style={'margin-left': '60px','margin-right': '60px','padding-top':'25px', 'padding-bottom':'10px','width' : '30 vw', 'height' :'80 vh'}
                                                    ),

                                            dbc.Container(
                                            dcc.Graph(id='boxplot', config={'displayModeBar': False}, className='graph'),
                                                    className='box', style={'margin-left': '60px','margin-right': '60px', 'padding-top':'25px', 'padding-bottom':'10px','width' : '30 vw','height' :'80 vh'}
                                                    ),
                                            
                                        ], lg=6, md=12, sm=12),

                                        dbc.Col([
                                            dbc.Container(
                                                dcc.Graph(id='histplot', className='graph', config={'displayModeBar': False}),
                                                className='box', style={'margin-right': '120px','margin-left': '60px', 'padding-top':'25px', 'padding-bottom':'10px','width' : '30 vw', 'height' :'80 vh'} ),
                                            

                                            dbc.Container(
                                                    dcc.Graph(id='ageplot', className='graph', config={'displayModeBar': False}),
                                                    className='box', style={'margin-right': '120px','margin-left': '60px', 'padding-top':'25px', 'padding-bottom':'10px','width' : '30 vw', 'height' :'80 vh'}
                                                    ),


                                        ], lg=6, md=12, sm=12)
                                        
                                        ]),
                                    
                                    dbc.Row([
                                        dbc.Container( [
                                            html.Label('Source : Stack Overflow Annual Developer Survey 2021 : https://insights.stackoverflow.com/survey'),
                                            html.Br(),
                                            html.P('With nearly 80,000 responses fielded from over 180 countries and dependent territories, our Annual Developer Survey examines all aspects of the developer experience from career satisfaction and job search to education and opinions on open source software.') ],
                                            className='box', style={'padding':'20px','width' : '1100px','height' :'150 px'})
                                    ]),


                                ], lg=12, md=12, sm=12, align="center")         

                                ),

                        html.Div(id='page-1-content'),

                        html.Div(
                            dcc.Link(
                                    dbc.Button('Home',
                                    id='home',
                                    color = 'Blue',
                                    style = {'margin':"25px",'border':'2px solid #C8D4E3', 'border-radius': '12px',
                                    'background' : '#f2f5fa', 'color' : 'black', 'font-size': '24px',
                                    'width': '200px'}), href='/home')
                                    , className='d-flex justify-content-center')
])


#################### CALLBACKS #############################################""


## pour le pie plot LEARN


@app.callback(
    Output(component_id='pieplot', component_property='figure'),
    Input(component_id='dropdown-component', component_property='value'),
)
# Fonction callback
def update_pieplot(devtype): # -> autant de paramètre(s) que d'input(s)
    
    
    # Création et alimentation du en données du graph
    fig = go.Figure()
    
    colors = px.colors.qualitative.Prism
    learn2 = learn[learn['DevType'] == devtype]
    data = pd.DataFrame(learn2['LearnCode'].value_counts())
    labels = data.index
    values = data['LearnCode']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    fig.update_layout(title_text="Learning how to code",title_x=0.5, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',font_color='white' ,
                    legend=dict(
                    yanchor="bottom",
                    y=-0.4,
                    xanchor="center",
                    x = 0.5)
                    )
            
    fig.update_yaxes(visible=False, fixedrange=False)

    fig.update_traces(hoverinfo='label+percent', textfont_size=12,
                  marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    
    # Renvoi du graph mis à jour dans le layout
    return fig

 ### pour le histplot YEARS   
@app.callback(
    Output(component_id='histplot',component_property='figure'),
    Input(component_id='dropdown-component', component_property='value')
)
def update_histplot(devtype):

    fig = go.Figure()

    data = code[code['DevType'] == devtype]

    fig = px.histogram(data, x="YearsCode",
                   title='Experience in code',
                   labels={'YearsCode':'Years since first code'},
                   nbins = 12, 
                   color_discrete_sequence=['rgb(29, 105, 150)'],
                   opacity = 0.9
                   )
   
    fig.update_layout(title_x=0.5,
                    yaxis_title= None,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False )

    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(tickvals=[5,10,15,20,25,30,35,40,45,50])

 
    return fig


### pour le box plot salary
@app.callback(
    Output(component_id='boxplot', component_property = 'figure'),
    Input(component_id = 'dropdown-component', component_property='value')
)

def update_boxplot(devtype) :

    df = salary[salary['DevType'] == devtype]

    #fig = go.Figure(data=[go.Box(y=df[(df['ConvertedCompYearly']<=100000) & (df['ConvertedCompYearly']>=10000)]['ConvertedCompYearly'], marker_color = 'rgb(95, 70, 144)')])
    #fig = px.box(data[(data['ConvertedCompYearly']<=100000) & (data['ConvertedCompYearly']>=10000)], y='ConvertedCompYearly')

    fig = px.box(df[(df['ConvertedCompYearly']<=100000) & (df['ConvertedCompYearly']>=10000)], x='ConvertedCompYearly',
                       color = 'Employment', facet_col="Employment", facet_col_wrap=1)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))


    fig.update_layout(title_text="Salary and employment status",
                    title_x=0.5,
                    xaxis_title = 'Yearly salary in $',
                    yaxis_title= None,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False )


    return fig

### pour le ageplot
@app.callback(
    Output(component_id='ageplot', component_property = 'figure'),
    Input(component_id = 'dropdown-component', component_property='value')
)

def update_ageplot(devtype) :

    data = age[age['DevType'] == devtype]

    fig = px.histogram(data, x="Age",
                   color = 'Gender',
                   title='Age and gender',
                   category_orders={"Age": ["Under 18 years old",
                                            "18-24 years old",
                                            "25-34 years old",
                                            "35-44 years old",
                                            "45-54 years old",
                                            "55-64 years old",
                                            "65 years or older"],
                                   "Gender" : ["Man","Woman","Non binary","Prefer not to say"]},
                    
                   color_discrete_sequence=px.colors.qualitative.Prism
                   
                   )
    fig.update_layout(title_x=0.5,
                    yaxis_title= None,
                    xaxis_title = 'years old',
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    legend_title=None,
                    legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1,
                              xanchor="center",
                              x=0.5
                               ))
    
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(   ticktext= ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or older"],
                        tickvals= ["Under 18 years old",
                                            "18-24 years old",
                                            "25-34 years old",
                                            "35-44 years old",
                                            "45-54 years old",
                                            "55-64 years old",
                                            "65 years or older"])
    
    return fig

### pour le funnel techno
@app.callback(
    Output(component_id='barplot', component_property = 'figure'),
    [ Input(component_id = 'dropdown-component', component_property='value'),
      Input(component_id = 'radio-component', component_property='value')]
)

def update_barplot(devtype, techno) :

    data= pd.read_csv(DATA_PATH.joinpath(techno+'.csv'))
    data =data[['WorkedWith', devtype]].sort_values(by= devtype, ascending = False).head(5)
    data= data.sort_values(by= devtype)
       
    fig = px.funnel(data, y='WorkedWith', x= devtype ,color = "WorkedWith", color_discrete_sequence=px.colors.qualitative.Prism)

    #fig = px.bar(data, y="WorkedWith", x= devtype ,color = "WorkedWith", color_discrete_sequence=px.colors.qualitative.Prism)

    fig.update_traces(textinfo='label',text="WorkedWith")
    fig.update_yaxes(visible=False)

    fig.update_layout(title_text=f"Technologies most used by {devtype}",
                    title_x=0.5,
                    yaxis_title= None,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False )
    
    return fig