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
#skill_options = {value:value for value in sorted(skill_df['skills'].unique())}
#skill_options.update({'All': 'All'})
skill_options = {key:[] for key in skill_df['sector'].unique().tolist()}
for i in skill_options.keys():
    skill_options[i]=skill_df[skill_df.sector==i]["skills"].unique().tolist()
# Set options for skill filter
ID_options = {value:value for value in sorted(skill_df['ID'].unique())}
#ID_options.update({'All': 'All','None':'None'})


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



########### APP ###############
layout = html.Div(

    dbc.Row([

    ###TITRE###
    dbc.Row([
    dbc.Col([
    html.Div([
    html.Img(src="https://yt3.ggpht.com/C4VnK2-PRneKt6fUVAKJL8CIDUJtvjRwQV-rsYa7iPsv3UVJ2qwXJMWQyhS7H6ZDq8QefqLZQ2E=s900-c-k-c0x00ffffff-no-rj",className="logo2"),
    html.Div(
        dcc.Link(
                dbc.Button('Show Overview',
                id='details',
                color = 'Blue',
                style = {'margin':"25px",'border':'2px solid #C8D4E3', 'border-radius': '12px',
                'background' : '#f2f5fa', 'color' : 'black', 'font-size': '24px',
                'width': '200px'}), href='/overview')
                , className='d-flex justify-content-center')
    ])
    ],lg=2,md=12, sm=12),

    dbc.Col([
    html.Div([
    #html.Img(src="https://static.wixstatic.com/media/c36c76_4d26ae83942b46c79e0e3919b818760e~mv2.png/v1/fill/w_1000,h_685,al_c,usm_0.66_1.00_0.01/c36c76_4d26ae83942b46c79e0e3919b818760e~mv2.png",className="logo"),
        html.H1('EMPLOYEES DETAILS', className='main-title'),
        #html.P('version : 0.1.0', className='text-version')
    ], className='title-div'),
    ],lg=10,md=12, sm=12),

    ]),



    ###ENCART JOB TITLE###
        dbc.Row([
            dbc.Col([
                html.Div([


                html.Img(src="https://th.bing.com/th/id/OIP.xA-dGZm-vu9fZz-wvMU-VgHaEK?pid=ImgDet&w=1200&h=675&rs=1",className="logo1"),
                html.H1("JOB TITLE", className="main-title"),


                html.Div([

                html.P('Select a year', className='form-text', style={'color':'#1CEDB7'}),
                dcc.RadioItems(
                    id='year-RI-p3c1',
                    options=[{'label': k, 'value': v} for k, v in skill_year_options.items()],
                    value=2021,
                    className='candidates-dropdown',style={'color':'#1CEDB7'}
                ),
                html.P('Select a field', className='form-text',style={'color':'#1CEDB7'}),
                dcc.Dropdown(
                    id='field-dpdn-p3c1',
                    options=[{'label': k, 'value': k} for k in skill_options.keys()],
                    value='Data Science et data analyse',
                    className='candidates-dropdown',

                ),
                html.P('Select a job title :', className='form-text', style={'color':'#1CEDB7'}),
                dcc.Dropdown(
                    id='job-dpdn-p3c1',
                    options=[{'label': k, 'value': v} for k, v in sorted(job_options.items())],
                    value='Data Analyst',
                    multi=False,
                    clearable=False,
                    className='candidates-dropdown',

                ),
                html.P('Select a skill  :', className='form-text', style={'color':'#1CEDB7'}),
                dcc.Dropdown(id='skills-dpdn-p3c1',
                #disabled=False,
                #placeholder='select skills',
                #searchable=True,
                style={'backgroundColor': '#1CEDB7','color': 'blue'}
                ),


    ])#div
    ],className='form-container')#div
    ], lg=2,md=12, sm=12 ),#col




        dbc.Col([
            html.Div([
                dbc.Container(
        dcc.Graph(id='chart p3c1',figure={},className='graph-details', config={'displayModeBar': False}),
                 className='box-overview', style={'margin-left': '20px', 'padding-top':'10px', 'padding-bottom':'10px', 'height' :'80vh', 'width' : '40vw'}),
    ]),
    ],lg=5, md=12, sm=12),

        dbc.Col([
            html.Div([
                dbc.Container(
                dcc.Graph(id='chart p3c2',figure={},className='graph-details', config={'displayModeBar': False}),
                className='box-overview', style={'margin-left': '20px', 'padding-top':'10px', 'padding-bottom':'10px', 'height' :'80vh', 'width' : '37vw'}),
    ]),
    ],lg=5, md=12, sm=12),
    ]),

    ###ENCART employees###
    dbc.Row([
        dbc.Col([
            html.Div([


            html.Img(src="https://fotomelia.com/wp-content/uploads/2016/04/images-gratuites-creative-commons-cco-7-1560x1560.jpg",className="logo1"),
            html.H1("EMPLOYEES", className="main-title"),


            html.Div([


            html.P('Select a field', className='form-text',style={'color':'#1CEDB7'}),
            dcc.Dropdown(
                id='field-dpdn-p3c3',
                options=[{'label': k, 'value': k} for k in skill_options.keys()],
                value='Data Science et data analyse',
                className='candidates-dropdown',


            ),
            html.P('Select skill as filter :', className='form-text', style={'color':'#1CEDB7'}),
            dcc.Dropdown(id='skills-dpdn-p3c3',
            ),


            html.P("ID:", style={'color':'#1CEDB7'}),
            dcc.Dropdown(id='ID-dpdn-p3c3',
                options=[{'label': k, 'value': v} for k,v in sorted(ID_options.items())],
                value='#1',
                clearable=False,
                multi=False,

    ),
    ])#div
    ],className='form-container')#div
    ], lg=2,md=12, sm=12 ),#col




    dbc.Col([
        html.Div([
            dbc.Container(
    dcc.Graph(id='chart p3c3',figure={},className='graph-details', config={'displayModeBar': False}),
                className='box-overview', style={'margin-left': '20px', 'padding-top':'10px', 'padding-bottom':'10px', 'height' :'80vh', 'width' : '40vw'}),
    ]),
    ],lg=5, md=12, sm=12),

    dbc.Col([

        html.Div([
            dbc.Container(
            dcc.Graph(id='chart p3c4',figure={},className='graph-details', config={'displayModeBar': False}),
            className='box-overview', style={'margin-left': '20px', 'padding-top':'10px', 'padding-bottom':'10px', 'height' :'80vh', 'width' : '37vw'}),
    ]),
    ],lg=5, md=12, sm=12),
    ]),

    ###ENCART Global view###
    dbc.Row([
        dbc.Col([
            html.Div([


            html.Img(src="https://www.imprim-deco.fr/6620-full_default/sticker-autocollant-longue-vue.jpg",className="logo1"),
            html.H1("GLOBAL VIEW EMPLOYEES", className="main-title"),


            html.Div([

            html.P('Select a year', className='form-text', style={'color':'#1CEDB7'}),
            dcc.RadioItems(
                id='year-RI-p3c5',
                options=[{'label': k, 'value': v} for k, v in skill_year_options.items()],
                value='All',
                className='candidates-dropdown',style={'color':'#1CEDB7'},

            ),


            html.P("select Level/Interest level or Gap:", style={'color':'#1CEDB7'}),
            dcc.Dropdown(id='color-dpdn-p3c5',
                options=[
                        {'label': 'Level', 'value': 'Level'},
                        {'label': 'Interest level', 'value': 'Interest level'},
                        {'label': 'gap', 'value': 'gap', },],
                        value='Level',

            ),

            html.P('Select job title as filter :', className='form-text', style={'color':'#1CEDB7'}),
            dcc.Dropdown(
                id='job-dpdn-p3c7',
                options=[{'label': k, 'value': v} for k, v in sorted(job_options.items())],
                value='All',
                multi=False,
                clearable=False,
                className='candidates-dropdown',
                        ),
    ])#div
    ],className='form-container')#div
    ], lg=2,md=12, sm=12 ),#col




    dbc.Col([
        html.Div([

            dbc.Container(
    dcc.Graph(id='chart p3c5',figure={},className='graph-details', config={'displayModeBar': False}),
            className='box-overview', style={'margin-left': '20px', 'padding-top':'10px', 'padding-bottom':'10px', 'height' :'100vh', 'width' : '80vw'}),

    ]),
    ],lg=10, md=12, sm=12),

    ]),

    ###ENCART Global view###BIS
    dbc.Row([
        dbc.Col([
            html.Div([


            html.Img(src="https://www.imprim-deco.fr/6620-full_default/sticker-autocollant-longue-vue.jpg",className="logo1"),
            html.H1("GLOBAL VIEW SKILLS", className="main-title"),


            html.Div([

            html.P('Select a year', className='form-text', style={'color':'#1CEDB7'}),
            dcc.RadioItems(
                id='year-RI-p3c6',
                options=[{'label': k, 'value': v} for k, v in skill_year_options.items()],
                value='All',
                className='candidates-dropdown',style={'color':'#1CEDB7'},

            ),
            html.P('Select a field', className='form-text',style={'color':'#1CEDB7'}),
            dcc.Dropdown(
                id='field-dpdn-p3c6',
                options=[{'label': k, 'value': v} for k, v in sorted(field_options.items())],
                value='All',
                className='candidates-dropdown',

            ),
            html.P('Select job title as filter :', className='form-text', style={'color':'#1CEDB7'}),
            dcc.Dropdown(
                id='job-dpdn-p3c6',
                options=[{'label': k, 'value': v} for k, v in sorted(job_options.items())],
                value='All',
                multi=False,
                clearable=False,
                className='candidates-dropdown',

            ),

            html.P("select Level/Interest level or Gap:", style={'color':'#1CEDB7'}),
            dcc.Dropdown(id='color-dpdn-p3c6',
                options=[
                        {'label': 'Level', 'value': 'Level'},
                        {'label': 'Interest level', 'value': 'Interest level'},
                        {'label': 'gap', 'value': 'gap', },],
                        value='Level',

            ),

    ])#div
    ],className='form-container')#div
    ], lg=2,md=12, sm=12 ),#col




    dbc.Col([
        html.Div([

        dbc.Container(
    dcc.Graph(id='chart p3c6',figure={},className='graph-details', config={'displayModeBar': False}),
                className='box-overview', style={'margin-left': '20px', 'padding-top':'10px', 'padding-bottom':'10px', 'height' :'100vh', 'width' : '80vw'}),
    ]),
    ],lg=10, md=12, sm=12),

    ]),


    ###ENCART TRAINING###
    dbc.Row([
        dbc.Col([
            html.Div([


            html.Img(src="https://webstockreview.net/images/clipart-telephone-telephone-skill-6.png",className="logo1"),
            html.H1("TRAININGS", className="main-title"),


            html.Div([

            html.P('Select a year', className='form-text', style={'color':'#1CEDB7'}),
            dcc.RadioItems(
                id='year-RI-p3c7',
                options=[{'label': k, 'value': v} for k, v in skill_year_options.items()],
                value='All',
                className='candidates-dropdown',style={'color':'#1CEDB7'},

            ),


            html.P("ID:", style={'color':'#1CEDB7'}),
            dcc.Dropdown(id='ID-dpdn-p3c7',
                options=[{'label': k, 'value': v} for k,v in sorted(ID_options.items())],
                value='Deep learning',
                clearable=False,
                multi=False,

    ),
            html.P('Smart Skills Sponsoring', className='form-text',
                style={'color':'#1CEDB7'}),
            dcc.Dropdown(
                id='sponsor-dpdn-p3c7',
                options=[{'label': k, 'value': v} for k, v in sorted(sponsor_options.items())],
                value='All'),

    ])#div
    ],className='form-container')#div
    ], lg=2,md=12, sm=12 ),#col




    dbc.Col([
        html.Div([
            dbc.Container(
    dt.DataTable(
        id='table-p3c7',
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
        ),className='box-overview', style={'margin-left': '100px', 'padding-top':'25px', 'padding-bottom':'10px', 'height' :'60vh', 'width' : '60vw'}),

    ]),
    ],lg=10, md=12, sm=12),

    ]),
    ])#row tt en haut
    )#1er div

###CALLBACK###



## CHART 1 ###
@app.callback(
    Output('skills-dpdn-p3c1', 'options'),
    Input('field-dpdn-p3c1', 'value'),
            )

def set_skills_options(selected_field):
    return [{'label': i, 'value': i} for i in skill_options[selected_field]]

@app.callback(

    Output("skills-dpdn-p3c1", "value"),
    Input('skills-dpdn-p3c1', 'options'),
    )

def set_skills_value(selected_skills):
    return selected_skills[0]['value']

@app.callback(

    [Output('chart p3c1', 'figure'),
    Output('chart p3c2', 'figure')],
    Input('year-RI-p3c1', 'value'),
    Input("field-dpdn-p3c1", "value"),
    Input("job-dpdn-p3c1", "value"),
    Input('skills-dpdn-p3c1', 'value'),
    )

def update_bar_chart(selected_year, selected_field,selected_job,selected_skills):
        #if type(selected_skills)!=str:
        dff = skill_df[(skill_df.year==selected_year) & (skill_df.sector==selected_field)&(skill_df.Job_title==selected_job)&(skill_df.skills == selected_skills)]
        #else:
        #dff = skill_df[(skill_df.year==selected_year) & (skill_df.sector==selected_field)&(skill_df.Job_title==selected_job)&(skill_df.skills==selected_skills)]
        fig1=px.bar(dff, y='Level', x='ID',color='ID')


        fig1.update_yaxes(dtick=1, range=[0,4.5])
        fig1.update_xaxes(title='Employees')
        fig1.update_layout(
                title={'text':f"LEVEL OF {selected_job.upper()} EMPLOYEES <Br> IN {selected_skills.upper()}" ,
                    'x':0.5},
                title_font_family="Arial",
                title_font_color="#1CEDB7",
                template="custom_dark",
                margin = dict(t=50, l=25, r=25, b=25),

                )




## CHART 2 ##



        fig2=px.bar(dff, y='gap', x='ID', color='skills', text='gap')
        fig2.update_xaxes(title='Employees')
        fig2.update_yaxes(dtick=1, range=[-4.5,4.5],title='Gap')
        fig2.update_traces(textposition = 'outside')
        fig2.update_layout(
            title={'text':f"DIFFERENCE BETWEEN LEVEL AND INTEREST <Br> FOR {selected_job.upper()} IN {selected_skills.upper()}",
                    'x':0.5},
            title_font_family="Arial",
            title_font_color="#1CEDB7",
            showlegend = False,
                #title_font_color="#FEFEFE",
            template="custom_dark",
            margin = dict(t=50, l=25, r=25, b=25),

                )

        return fig1,fig2


###chart 3.3  ###

@app.callback(
    Output('skills-dpdn-p3c3', 'options'),
    Input('field-dpdn-p3c3', 'value'),
            )

def set_skills_options(selected_field):
    return [{'label': i, 'value': i} for i in skill_options[selected_field]]

@app.callback(

    Output("skills-dpdn-p3c3", "value"),
    Input('skills-dpdn-p3c3', 'options'),
    )

def set_skills_value(selected_skills):
    return selected_skills[0]['value']

@app.callback(

    [Output('chart p3c3', 'figure'),
    Output('chart p3c4', 'figure')],
    Input("skills-dpdn-p3c3", "value"),
    Input("field-dpdn-p3c3", "value"),
    Input('ID-dpdn-p3c3', 'value'),
    )

def update_graph(selected_skills,selected_field,selected_ID):

            dff = skill_df[(skill_df.sector==selected_field) & (skill_df.skills == selected_skills)&(skill_df.ID==selected_ID) ]
            data0 = go.Bar(y=dff.Level, x=dff.year,name='Level')# color='ID',animation_frame="ID")

            data1=go.Scatter( y=dff['Interest level'], x=dff.year,name='Interest Level')# color='ID',animation_frame="ID")
            data =[data0,data1]


            fig3=go.Figure(data=data)
            fig3.update_yaxes(dtick=1,range=[-4,4.5], title = 'Gap')
            fig3.update_xaxes(dtick=1)
            fig3.update_layout(
                title={'text':f"EVOLUTION OF EMPLOYEE ID {selected_ID} 'S LEVEL <Br> IN {selected_skills.upper()}",
                    'x':0.5},
                title_font_family="Arial",
                title_font_color="#1CEDB7",
                template="custom_dark",
                margin = dict(t=50, l=25, r=25, b=25),

                )



###chart4###




            fig4=px.bar(dff, y='gap', x='year', color='skills',barmode='group',text = 'gap')
            fig4.update_yaxes(dtick=1, range=[-4.5,4.5],title='Gap')
            fig4.update_xaxes(dtick=1, )
            fig4.update_traces(textposition = 'outside')
            fig4.update_layout(
                title={'text':f"EVOLUTION OF THE GAP BETWEEN LEVEL AND INTEREST <Br> FOR EMPLOYEE ID {selected_ID} IN {selected_skills.upper()}",
                    'x':0.5},
                title_font_family="Arial",
                title_font_color="#1CEDB7",
                xaxis_title = None,
                showlegend = False,
                template="custom_dark",
                margin = dict(t=50, l=25, r=25, b=25),

                )


            return fig3,fig4



###chart 3.5 Treemap ###
@app.callback(
Output('chart p3c5', 'figure'),
[Input('year-RI-p3c5', 'value'),
Input("color-dpdn-p3c5", 'value'),
Input('job-dpdn-p3c7', 'value')]
)

def update_global_treemap_ID (selected_year,selected_color,selected_job):
    #if selected_year == 'All':
        #skill_df5 = skill_df
    #else:
        #skill_df5 = skill_df[(skill_df['year'] == selected_year)]

    if selected_job == 'All' and selected_year == 'All':
        skill_df6 = skill_df
    elif selected_job == 'All' and selected_year != 'All':
        skill_df6 = skill_df[(skill_df['year'] == selected_year)]
    elif selected_job != 'All' and selected_year == 'All':
        skill_df6 = skill_df[(skill_df['Job_title'] == selected_job)]
    else:
        skill_df6 = skill_df[(skill_df['Job_title'] == selected_job) & (skill_df['year'] == selected_year)]

    fig5 = px.treemap(skill_df6, path=['ID','skills',selected_color,'year'],color=(selected_color),height=600,
    color_discrete_sequence= px.colors.sequential.Agsunset_r)


    fig5.update_layout(
    title={'text':f"GLOBAL VIEW OF {selected_color.upper()} FOR EMPLOYEES ",
        'x':0.5},
    title_font_family="Arial",
    title_font_color="#1CEDB7",
    template="custom_dark",
    margin = dict(t=50, l=25, r=25, b=25),
    showlegend=False
    )

    return fig5

###chart 3.6 Treemap ###


@app.callback(
Output('chart p3c6', 'figure'),
[Input('year-RI-p3c6', 'value'),
Input('job-dpdn-p3c6', 'value'),
Input('field-dpdn-p3c6', 'value'),
Input("color-dpdn-p3c6", 'value')]
)

def update_global_treemap_skills(selected_year,selected_job,selected_field,selected_color):
# Define data to display according to job title dropdown selection


# Define data to display according to sponsoring radio item selection
    if selected_field == 'All':
        skill_df6 = skill_df
    else:
        skill_df6 = skill_df[(skill_df['sector'] == selected_field)]


    if selected_job == 'All' and selected_year == 'All':
        skill_df6 = skill_df6
    elif selected_job == 'All' and selected_year != 'All':
        skill_df6 = skill_df6[(skill_df6['year'] == selected_year)]
    elif selected_job != 'All' and selected_year == 'All':
        skill_df6 = skill_df6[(skill_df6['Job_title'] == selected_job)]
    else:
        skill_df6 = skill_df6[(skill_df6['Job_title'] == selected_job) & (skill_df6['year'] == selected_year)]

    fig6 = px.treemap(skill_df6, path=['skills',selected_color,'ID'],color=(selected_color),height=600,color_discrete_sequence= px.colors.sequential.Agsunset)
    fig6.update_layout(
          title={'text':f"GLOBAL VIEW OF {selected_color.upper()} FOR SKILLS",
              'x':0.5},
          title_font_family="Arial",
          title_font_color="#1CEDB7",
          template="custom_dark",
          margin = dict(t=50, l=25, r=25, b=25),
          showlegend=False
          )



    return fig6

###Chart table###
@app.callback(Output('table-p3c7', 'data'),
    [Input('ID-dpdn-p3c7', 'value'),
    Input('year-RI-p3c7', 'value'),
    Input('sponsor-dpdn-p3c7', 'value')])

def update_table(selected_ID, year, sponsoring,):
    ccl_df7=ccl_df[(ccl_df["sponsored training(yes-no)"]=='Yes')|(ccl_df["sponsored training(yes-no)"]=='No')]
    # Define data to display according to job title dropdown selection
    if selected_ID == 'All':
        data = ccl_df7
    else:
        data = ccl_df7[(ccl_df7['ID'] == selected_ID)]

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
