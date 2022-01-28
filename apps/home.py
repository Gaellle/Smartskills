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

from apps import survey, overview, details, home

############" HOME PAGE LAYOUT################

layout = html.Div(
    
    dbc.Row([
        
        dbc.Col([
            
            html.Div([   
                html.Img(src="https://static.wixstatic.com/media/c36c76_4d26ae83942b46c79e0e3919b818760e~mv2.png/v1/fill/w_1000,h_685,al_c,usm_0.66_1.00_0.01/c36c76_4d26ae83942b46c79e0e3919b818760e~mv2.png", className="logo"),
            ])
                           
        ], lg=3, md=12, sm=12 ),      
                
               
        dbc.Col([
            html.Div([
                    html.Br(),
                    html.H1("Projet SMART SKILLS", className="main-title"),
                    ], className="title-div"),

            dbc.Row([
                        html.Div([  html.Br(),
                                    html.P(),
                                    dcc.Link(
                                        dbc.Button('Employees overview',
                                        id='overview', 
                                        color = 'Blue',
                                        style = {'margin':"25px",'border':'2px solid rgb(104, 96, 165)', 'border-radius': '12px',
                                        'background' : '#ebf875', 'color' : 'black', 'font-size': '28px',
                                        'width': '350px', 'height' : '220px'}
                                                            ),
                                                            href='/overview'),

                                    dcc.Link(
                                        dbc.Button('Detailed datas',
                                        id='insight', 
                                        color = 'Blue',
                                        style = {'margin':"25px",'border':'2px solid rgb(104, 96, 165)', 'border-radius': '12px',
                                        'background' : '#ebf875', 'color' : 'black', 'font-size': '28px',
                                        'width': '350px', 'height' : '220px'}
                                                            ),
                                                            href='/details')
                                    
                                ], className='d-grid gap-2 d-flex justify-content-center'),
                        ]),
            
            dbc.Row([
                        html.Div([  html.Br(),
                                    html.P(),
                                    dcc.Link(
                                        dbc.Button('Worldwide Developer Survey',
                                        id='survey', 
                                        color = 'Blue',
                                        style = {'margin':"25px",'border':'2px solid rgb(104, 96, 165)', 'border-radius': '12px',
                                        'background' : '#f8d575', 'color' : 'black', 'font-size': '28px',
                                        'width': '350px', 'height' : '220px'}
                                                            ),
                                                            href='/survey'),

                                    
                                ], className='d-grid gap-2 d-flex justify-content-center'),
                        ]),
            
            html.Div([
                    html.Br(),
                    html.H1("DREAM TEAM", className="main-title"),
                    ], className="title-div"),

            
            dbc.Row([
                dbc.Col([
                    dbc.Container( [
                                    html.H2('Charlotte'),
                                    html.Br(),
                                    ],
                                    className='box', style={'padding':'20px','width' : '200px','height' :'150 px'})
                                    ], lg = 3),

                dbc.Col([
                    dbc.Container( [
                                    html.H2('Ghizlaine'),
                                    html.Br(),
                                    ],
                                    className='box', style={'padding':'20px','width' : '200px','height' :'150 px'})
                                    ], lg = 3),


                dbc.Col([
                    dbc.Container( [
                                    html.H2('Lucile'),
                                    html.Br(),
                                    ],
                                    className='box', style={'padding':'20px','width' : '200px','height' :'150 px'})
                                    ], lg = 3)                    
                    ], className='d-grid gap-2 d-flex justify-content-center'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Container( [
                                    html.H2('Maxime'),
                                    html.Br(),
                                    ],
                                    className='box', style={'padding':'20px','width' : '200px','height' :'150 px'})
                                    ], lg = 3),

                dbc.Col([
                    dbc.Container( [
                                    html.H2('Gaelle'),
                                    html.Br(),
                                    html.Div([   
                                        html.Img(src="https://storage.googleapis.com/quest_editor_uploads/SoDu36bRthc7V4Owh1mZ1433khzti00R.jpeg", className="photo_id")],className='d-grid gap-2 d-flex justify-content-center')
                                    ],
                                    className='box', style={'padding':'20px','width' : '200px','height' :'150 px'})
                                    ], lg = 3),
            
                    ],className='d-grid gap-2 d-flex justify-content-center'),
                        
            ], lg=9, md=12, sm=12)    
            
        ])
      
)
