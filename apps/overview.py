import dash
from dash import dcc
from dash import html
from dash import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as plt_io
import plotly.graph_objects as go

import pathlib
from app import app

############ DATA ################

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

learn = pd.read_csv(DATA_PATH.joinpath('learn.csv'))

skill_df = pd.read_csv(DATA_PATH.joinpath("smart_skills_knime-skills.csv"))
skill_df['gap'] = skill_df['Interest level']-skill_df['Level']
ccl_df = pd.read_csv(DATA_PATH.joinpath("smart_skills_knime-conclusion.csv"))
ccl_df['sponsored training(yes-no)'].fillna('',inplace=True) # a faire via knime
ccl_df['skills'].fillna('',inplace=True) #a faire via knime
txt_ccl_df = pd.read_csv(DATA_PATH.joinpath("ccl_with_text.csv"))
#Kpi top level group by
#top_level=df.groupby('skills')['Level'].sum().sort_values(ascending=False).head(10)
#top_level=pd.DataFrame(top_level).reset_index()


############ OPTIONS ################

# Set options for job title filter
job_options = {value:value for value in sorted(skill_df['Job_title'].unique())}
job_options.update({'All': 'All'})

# Set options for year filter
skill_year_options = {value:value for value in sorted(skill_df['year'].unique())}
skill_year_options.update({'All': 'All'})
ccl_year_options = {value:value for value in sorted(ccl_df['year'].unique())}
ccl_year_options.update({'All': 'All'})
txt_ccl_year_options = {value:value for value in sorted(txt_ccl_df['year'].unique())}
txt_ccl_year_options.update({'All': 'All'})

# Set options for sponsor filter
sponsor_options = {value:value for value in ccl_df['sponsored training(yes-no)'].unique()}
sponsor_options.update({'All': 'All'})

# Set options for field filter
field_options = {value:value for value in sorted(skill_df['sector'].unique())}
field_options.update({'All': 'All'})

# Set options for skill filter
skill_options = {value:value for value in sorted(skill_df['skills'].unique())}



############ LAYOUT ################


# Set the Plotly-wide default template
plt_io.templates.default = "simple_white"

# create our custom_dark theme from the plotly_dark template
plt_io.templates["custom_dark"] = plt_io.templates["plotly_dark"]

# set the paper_bgcolor and the plot_bgcolor to a new color
plt_io.templates["custom_dark"]['layout']['paper_bgcolor'] = '#0d2c4b'
plt_io.templates["custom_dark"]['layout']['plot_bgcolor'] = '#0d2c4b'

# Change gridline colors to make them visible on the new background
plt_io.templates['custom_dark']['layout']['yaxis']['gridcolor'] = '#4f687d'
plt_io.templates['custom_dark']['layout']['xaxis']['gridcolor'] = '#4f687d'

layout = html.Div([

    dbc.Row([

        dbc.Col([

            html.Div([

                html.Div([
                    html.H1('Overview', className='main-title'),
                    html.H2('Skill fields', className='second-title')
                ], className='title-div'),

                html.Div([

                    html.P('Select job title as filter :', className='form-text'),
                    dcc.Dropdown(
                        id='job-dpdn-p1',
                        options=[{'label': k, 'value': v} for k, v in sorted(job_options.items())],
                        value='All',
                        multi=False,
                        clearable=False,
                        className='job-title-dropdown'
                    ),

                    html.Div(
                        dcc.Link(
                                dbc.Button('Show details',
                                id='details',
                                color = 'Blue',
                                style = {'margin':"25px",'border':'2px solid #C8D4E3', 'border-radius': '12px',
                                'background' : '#f2f5fa', 'color' : 'black', 'font-size': '24px',
                                'width': '200px'}), href='/details')
                                , className='d-flex justify-content-center'),
                    
                    html.Div(
                        dcc.Link(
                                dbc.Button('Home',
                                id='home',
                                color = 'Blue',
                                style = {'margin':"25px",'border':'2px solid #C8D4E3', 'border-radius': '12px',
                                'background' : '#f2f5fa', 'color' : 'black', 'font-size': '24px',
                                'width': '200px'}), href='/home')
                                , className='d-flex justify-content-center'),



                        ], className='form-div')

            ], className='form-container')

        ], lg=2, md=12, sm=12),

        dbc.Col([

            html.Div([

                    dbc.Row([
                        html.P(),
                        html.Label("SMART SKILLS : TRAINING OVERVIEW",
                            style={'textAlign': 'center', 'font-weight': 'bold', 'color':'#1CEDB7', 'fontSize': 18}),
                        html.P(),

                        dbc.Container([
                                dcc.Graph(id='pie-level', className='graph-overview', config={'displayModeBar': False})],
                                className='box-overview', style={'margin-left': '20px', 'padding-top':'10px', 'padding-bottom':'10px', 'height' :'80vh', 'width' : '80vw'}),
                                ]),

                    dbc.Row([
                        dbc.Container([
                                dcc.Graph(id='pie-interest-level', className='graph-overview', config={'displayModeBar': False}) ],
                                className='box-overview', style={'margin-left': '20px', 'padding-top':'10px', 'padding-bottom':'10px', 'height' :'80vh', 'width' : '80vw'}),


    ]),



dbc.Row([
    dbc.Col([
        dbc.Container([
                        dcc.Graph(id='chart p1c3',className='graph-overview', config={'displayModeBar': False}),
                        html.P('Select a year', className='form-text', style={'color':'#1CEDB7', 'margin-left': '20px'}),
                        dcc.RadioItems(
                            id='year-RI-c3',
                            options=[{'label': k, 'value': v} for k, v in txt_ccl_year_options.items()],
                            value='All',
                            labelStyle={'display':'inline-block', 'color':'#1CEDB7', "padding":"10px", }),
                        ], className='box-overview', style={'padding-top':'25px', 'padding-bottom':'10px', 'height' :'80vh', 'width' : '40vw'}),
                        ]),
dbc.Col([
    dbc.Container([

                                dcc.Graph(id='chart p1c4',className='graph-overview', config={'displayModeBar': False}),
                                ],className='box-overview', style={'padding-top':'25px', 'padding-bottom':'10px','height' :'80vh', 'width' : '37vw'}
                                ),
                            ])
                        ]),




dbc.Row([
dbc.Col([
dbc.Container([
html.H1("TOP 10 OF SKILLS IN DEMAND",
    style={'textAlign': 'center', 'color':'#1CEDB7', 'fontSize': 16}),
html.P(),
html.P(),

dbc.Row([
                        dbc.Col([
                        html.P('Select a field', className='form-text',
                            style={'color':'#1CEDB7'}),

                        dcc.Dropdown(
                            id='field-dpdn-c5',
                            options=[{'label': k, 'value': v} for k, v in sorted(field_options.items())],
                            value='All'),
                        html.P(),
                        dcc.Graph(id='chart p1c5', config={'displayModeBar': False}, className='graph-overview'),

                        ], lg=5, md=12, sm=12),

                        dbc.Col([

                        html.P('Select a year', className='form-text', style={'color':'#1CEDB7'}),
                        dcc.RadioItems(
                        id='year-RI-5',
                        options=[{'label': k, 'value': v} for k, v in skill_year_options.items()],
                        value='All',
                        labelStyle={'display':'inline-block', 'color':'#1CEDB7', "padding":"10px"},
                        className='radio2'),
                        #style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                        html.P(),
                        dcc.Graph(id='chart p1c6', config={'displayModeBar': False}, className='graph-overview'),
                        ], lg=5, md=12, sm=12),




                    ], className='d-grid gap-2 d-flex justify-content-center'),

                    ],className='box-overview', style={'margin-left': '10px', 'padding-top':'25px', 'padding-bottom':'10px','height' :'100vh', 'width' : '80vw'}
                ),
],lg=10, md=12, sm=12)
]),
                    dbc.Row([

                        dbc.Container([
                        html.H1("LIST OF TRAININGS",
                            style={'textAlign': 'center', 'font-weight': 'bold', 'color':'#1CEDB7', 'fontSize': 18}),
                            html.P(),
                            html.Div([
                                html.P('Select year', className='form-text',
                                    style={'color':'#1CEDB7'}),
                                dcc.RadioItems(
                                    id='year-RI-c7',
                                    options=[{'label': k, 'value': v} for k, v in ccl_year_options.items()],
                                    value='All',
                                    labelStyle={'display':'inline-block', 'color':'#1CEDB7', "padding":"10px"}),
                                html.P()
                                ]),
                            html.Div([
                                html.P('Smart Skills Sponsoring', className='form-text',
                                    style={'color':'#1CEDB7'}),
                                dcc.Dropdown(
                                    id='sponsor-dpdn-c7',
                                    options=[{'label': k, 'value': v} for k, v in sorted(sponsor_options.items())],
                                    value='All'),
                                html.P()
                                ]),
                            dt.DataTable(
                                id='table',
                                columns=[
                                    {"name":"Year", "id":"year"},
                                    {"name":"Training", "id":"skills"},
                                    {"name":"Sponsoring", "id":"sponsored training(yes-no)"}],
                                data=ccl_df.to_dict('records'),
                                style_header={
                                    'backgroundColor': '#f6fabf',
                                    'fontWeight': 'bold',
                                    'color': '#012243',
                                    'border': '2px solid white',
                                    'textAlign': 'center'},
                                style_cell={
                                    'padding': '5px',
                                    'border': '1px solid white',
                                    'textAlign': 'center',
                                    'backgroundColor': '#2F4F4F',
                                    'color': 'white'},
                                style_cell_conditional=[
                                    {'if': {'column_id':'skills'}, 'textAlign': 'left'}],
                                style_as_list_view=False,
                                fixed_rows={'headers':True}
                                ),

                            ], className='box-overview',
                            style={'margin-left': '20px', 'padding':'25px', 'height' :'130vh', 'width' : '80vw'}),
                    ]),

                ]),
                ], lg=10, md=12, sm=12),
            ]),

    html.Div(id='page-3-content'),

])

# Callback for pie chart 1.1
@app.callback(Output('pie-level', 'figure'), Input('job-dpdn-p1', 'value'))

def update_pie_level(selected_job):

    # Define data to display according to job title dropdown selection
    if selected_job == 'All':
        skill_df1 = skill_df
    else:
        skill_df1 = skill_df[(skill_df['Job_title'] == selected_job)]

    # Define 3 dataframes with the level grouped by field (sum), 1 per year (TH, LY and L2Y)
    field_level_TY = skill_df1[skill_df1['year'] == skill_df1['year'].max()].groupby('sector')['Level'].sum().sort_values(ascending=False) # TY = This Year
    field_level_TY = pd.DataFrame(field_level_TY).reset_index()
    field_level_LY = skill_df1[skill_df1['year'] == skill_df1['year'].max()-1].groupby('sector')['Level'].sum().sort_values(ascending=False) # LY = Last Year
    field_level_LY = pd.DataFrame(field_level_LY).reset_index()
    field_level_L2Y = skill_df1[skill_df1['year'] == skill_df1['year'].max()-2].groupby('sector')['Level'].sum().sort_values(ascending=False) # L2Y = Last 2 Years
    field_level_L2Y = pd.DataFrame(field_level_L2Y).reset_index()

    # Create figure and subplots
    titleFig1s1 = str(skill_df['year'].max()-2)
    titleFig1s2 = str(skill_df['year'].max()-1)
    titleFig1s3 = str(skill_df['year'].max())
    fig1 = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]], subplot_titles=(titleFig1s1, titleFig1s2, titleFig1s3))
    fig1.add_trace(go.Pie(labels=field_level_L2Y['sector'], values=field_level_L2Y['Level']), row=1, col=1)
    fig1.add_trace(go.Pie(labels=field_level_LY['sector'], values=field_level_LY['Level']), row=1, col=2)
    fig1.add_trace(go.Pie(labels=field_level_TY['sector'], values=field_level_TY['Level']), row=1, col=3)
    fig1.update_traces(textposition = 'inside', textinfo = 'percent')

    # Set figure layout
    fig1.update_layout(
        title={'text':"EVOLUTION OF SMART SKILLS EMPLOYEES' LEVEL PER SKILL FIELD",
            'x':0.5},
        title_font_family="Arial",
        title_font_color="#1CEDB7",
        legend=dict(orientation="h", yanchor="bottom", y=-0.7),
        template="custom_dark"
        )
    for annotation in fig1['layout']['annotations']:
        annotation['yanchor']='bottom'
        annotation['y']=-0.2
        annotation['yref']='paper'

    return fig1

# Callback for pie chart 1.2
@app.callback(Output('pie-interest-level', 'figure'), Input('job-dpdn-p1', 'value'))

def update_pie_interest_level(selected_job):

    # Define data to display according to job title dropdown selection
    if selected_job == 'All':
        skill_df2 = skill_df
    else:
        skill_df2 = skill_df[(skill_df['Job_title'] == selected_job)]

    # Define 3 dataframes with the level grouped by field (sum), 1 per year (TH, LY and L2Y)
    field_interest_level_TY = skill_df2[skill_df2['year'] == skill_df2['year'].max()].groupby('sector')['Interest level'].sum().sort_values(ascending=False) # TY = This Year
    field_interest_level_TY = pd.DataFrame(field_interest_level_TY).reset_index()
    field_interest_level_LY = skill_df2[skill_df2['year'] == skill_df2['year'].max()-1].groupby('sector')['Interest level'].sum().sort_values(ascending=False) # LY = Last Year
    field_interest_level_LY = pd.DataFrame(field_interest_level_LY).reset_index()
    field_interest_level_L2Y = skill_df2[skill_df2['year'] == skill_df2['year'].max()-2].groupby('sector')['Interest level'].sum().sort_values(ascending=False) # L2Y = Last 2 Years
    field_interest_level_L2Y = pd.DataFrame(field_interest_level_L2Y).reset_index()

    # Create figure and subplots
    titleFig2s1 = str(skill_df['year'].max()-2)
    titleFig2s2 = str(skill_df['year'].max()-1)
    titleFig2s3 = str(skill_df['year'].max())
    fig2 = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]], subplot_titles=(titleFig2s1, titleFig2s2, titleFig2s3))
    fig2.add_trace(go.Pie(labels=field_interest_level_L2Y['sector'], values=field_interest_level_L2Y['Interest level']), row=1, col=1)
    fig2.add_trace(go.Pie(labels=field_interest_level_LY['sector'], values=field_interest_level_LY['Interest level']), row=1, col=2)
    fig2.add_trace(go.Pie(labels=field_interest_level_TY['sector'], values=field_interest_level_TY['Interest level']), row=1, col=3)
    fig2.update_traces(textposition = 'inside', textinfo = 'percent')

    # Set figure layout
    fig2.update_layout(
        title={'text':"EVOLUTION OF SMART SKILLS EMPLOYEES' INTEREST LEVEL PER SKILL FIELD",
            'x':0.5},
        title_font_family="Arial",
        title_font_color="#1CEDB7",
        legend=dict(orientation="h", yanchor="bottom", y=-0.7),
        template="custom_dark"
        )
    for annotation in fig2['layout']['annotations']:
        annotation['yanchor']='bottom'
        annotation['y']=-0.2
        annotation['yref']='paper'

    return fig2


# Callback for chart 1.3
@app.callback(Output('chart p1c3', 'figure'), Input('year-RI-c3', 'value'))

def update_sunburst_chart(selected_year):

    # Define data to display according to job title dropdown selection
    #if selected_job == 'All':
        #data = txt_ccl_df
    #else:
        #data = txt_ccl_df[(txt_ccl_df['Job_title'] == selected_job)]

    #Define data to display according to job title dropdown selection
    if selected_year == 'All':
        data = txt_ccl_df
    else:
        data = txt_ccl_df[(txt_ccl_df['year'] == selected_year)]




    fig3= px.sunburst(data_frame=data,
        path=["training_done(yes_no)",'sponsored_training(yes_no)'],
        color="training_done(yes_no)",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        maxdepth=-2,
        color_continuous_scale=px.colors.sequential.BuGn,
        range_color=[10,100],
        branchvalues="total",
        #hover_name='sponsored_training(yes_no)',
        #hover_data={'sponsored_training(yes_no)': False},
        template='seaborn')
    fig3.update_traces(textinfo='label+percent root')
    fig3.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig3.update_layout(
        title={'text':" TRAINING RATE EMPLOYEES ",
            'x':0.5},
        title_font_family="Arial",
        title_font_color="#1CEDB7",
        template="custom_dark",
        margin = dict(t=50, l=25, r=25, b=25),
        legend_title_text=None,


        )

    return fig3

# Callback for chart 1.4
@app.callback(
Output('chart p1c4', 'figure'),
Input('year-RI-c3','value'))



def update_bar_chart(selected_year):
        txt_ccl_df4=txt_ccl_df.groupby(["year","training_done(yes_no)",'sponsored_training(yes_no)']).count()[['ID']].sort_values(by='training_done(yes_no)',ascending=False)
        txt_ccl_df4['ID']=txt_ccl_df4['ID']/len(txt_ccl_df.ID.unique())*100
        txt_ccl_df4=txt_ccl_df4.reset_index()
        txt_ccl_df4=txt_ccl_df4[txt_ccl_df4['training_done(yes_no)']=='Training Yes']


        fig4 =px.bar(txt_ccl_df4,y='ID', x="year", color='sponsored_training(yes_no)',color_discrete_sequence=px.colors.qualitative.Pastel)
        fig4.update_yaxes(title='Percentage employees',range=[0,100])
        fig4.update_xaxes(title='training',dtick=1)
        fig4.update_layout(
            title={'text':" TRAINING RATE EMPLOYEES ",
                'x':0.5},
            title_font_family="Arial",
            title_font_color="#1CEDB7",
            template="custom_dark",
            margin = dict(t=50, l=25, r=25, b=25),
            legend_title_text=None
            )
        return fig4









# Callback for chart 1.5
@app.callback(Output('chart p1c5', 'figure'),
    [Input("year-RI-5", 'value'), Input("field-dpdn-c5", 'value'), Input("job-dpdn-p1", 'value'),])

def update_tunnel_top10_level(selected_year,selected_field,selected_job):

    # Define data to display according to job title dropdown selection
    if selected_job == 'All':
        data = skill_df
    else:
        data = skill_df[(skill_df['Job_title'] == selected_job)]

    # Define data to display according to sponsoring radio item selection
    if selected_field == 'All' and selected_year == 'All':
        data = data
    elif selected_field == 'All' and selected_year != 'All':
        data = data[(data['year'] == selected_year)]
    elif selected_field != 'All' and selected_year == 'All':
        data = data[(data['sector'] == selected_field)]
    else:
        data = data[(data['sector'] == selected_field) & (data['year'] == selected_year)]

    skill_df5 = data.groupby('skills')['Interest level'].sum().sort_values(ascending=False).head(10)
    skill_df5 = pd.DataFrame(skill_df5).reset_index()
    skill_df5['Interest level'] = skill_df5['Interest level'] / len(skill_df5)
    #skill_df5 = skill_df5.sort_values(by='Interest level')

    fig5 = px.funnel(skill_df5, x='Interest level', y='skills', #color='Interest level',
        text = "skills", color_discrete_sequence= px.colors.sequential.Agsunset_r)

    # Set figure layout
    fig5.update_traces(textinfo='label',text='skills')
    fig5.update_yaxes(visible=False)
    fig5.update_layout(
        title={'text':"TOP 10 OF SKILLS IN-DEMAND <br>(highest interest)",
            'x':0.5},
        title_font_family="Arial",
        title_font_color="#1CEDB7",
        template="custom_dark",
        margin = dict(t=50, l=25, r=25, b=25),
        showlegend=False
        )

    return fig5


# Callback for chart 1.6
@app.callback(Output('chart p1c6', 'figure'),
    [Input("year-RI-5", 'value'), Input("field-dpdn-c5", 'value'), Input("job-dpdn-p1", 'value'),])

def update_tunnel_top10_level(selected_year,selected_field,selected_job):

    # Define data to display according to job title dropdown selection
    if selected_job == 'All':
        data = skill_df
    else:
        data = skill_df[(skill_df['Job_title'] == selected_job)]

    # Define data to display according to sponsoring radio item selection
    if selected_field == 'All' and selected_year == 'All':
        data = data
    elif selected_field == 'All' and selected_year != 'All':
        data = data[(data['year'] == selected_year)]
    elif selected_field != 'All' and selected_year == 'All':
        data = data[(data['sector'] == selected_field)]
    else:
        data = data[(data['sector'] == selected_field) & (data['year'] == selected_year)]

    skill_df6 = data.groupby('skills')['gap'].sum().sort_values(ascending=False).head(10)
    skill_df6 = pd.DataFrame(skill_df6).reset_index()
    skill_df6['gap'] = skill_df6['gap'] / len(skill_df6)
    #skill_df6 = skill_df6.sort_values(by='gap')

    fig6 = px.funnel(skill_df6, x='gap', y='skills', #color='gap',
        text = "skills", color_discrete_sequence= px.colors.sequential.Agsunset_r)

    # Set figure layout
    fig6.update_traces(textinfo='label',text='skills')
    fig6.update_yaxes(visible=False)
    fig6.update_layout(
        title={'text':"TOP 10 OF SKILLS IN-DEMAND <br>(difference between level of interest and level for skills)<br>",
            'x':0.5},
        title_font_family="Arial",
        title_font_color="#1CEDB7",
        template="custom_dark",
        margin = dict(t=50, l=25, r=25, b=25),
        showlegend=False
        )

    return fig6


# Callback for table chart 1.7
@app.callback(Output('table', 'data'),
    [Input('job-dpdn-p1', 'value'),
    Input('year-RI-c7', 'value'),
    Input('sponsor-dpdn-c7', 'value')])

def update_table(selected_job, year, sponsoring):
    ccl_df7=ccl_df[(ccl_df["sponsored training(yes-no)"]=='Yes')|(ccl_df["sponsored training(yes-no)"]=='No')]
    # Define data to display according to job title dropdown selection
    if selected_job == 'All':
        data = ccl_df7
    else:
        data = ccl_df7[(ccl_df7['Job_title'] == selected_job)]

    # Define data to display according to sponsoring radio item selection
    if sponsoring == 'All' and year == 'All':
        data = data
    elif sponsoring == 'All' and year != 'All':
        data = data[(data['year'] == year)]
    elif sponsoring != 'All' and year == 'All':
        data = data[(data['sponsored training(yes-no)'] == sponsoring)]
    else:
        data = data[(data['sponsored training(yes-no)'] == sponsoring) & (data['year'] == year)]

    data = data[["year", "skills", "sponsored training(yes-no)"]]
    return data.to_dict('records')