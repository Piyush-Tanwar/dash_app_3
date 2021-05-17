# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:18:15 2021

@author: Adm one
"""

import pandas as pd
import os
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import dash 
from dash.dependencies import Input,Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

os.chdir(r'C:\Users\Adm one\Desktop\AP\Piyush\whole_state_scheme_analysis')
######----------overview data-------------####
overview_dbt = pd.read_csv('overview_dbt.csv')
overview_dbt = overview_dbt.fillna('')
overview_dbt['SCHEME NAME'] = overview_dbt['SCHEME NAME'].str.upper()
overview_dbt = overview_dbt.rename(columns={'SI NO':'S.No.','HH Count':'HOUSEHOLD COUNT','Total Beneficiaries':'BENEFICIARIES COUNT','Total Amount( In Cr.)':'AMOUNT(crores)'})

overview_non_dbt = pd.read_csv('overview_non_dbt.csv')
overview_non_dbt = overview_non_dbt.fillna('')
overview_non_dbt['SCHEME NAME'] = overview_non_dbt['SCHEME NAME'].str.upper()
overview_non_dbt = overview_non_dbt.rename(columns={'SI NO':'S.No.','HH Count':'HOUSEHOLD COUNT','Total Beneficiaries':'BENEFICIARIES COUNT','Total Amount( In Cr.)':'AMOUNT(crores)'})

total_hh_benefits = overview_dbt.loc[22,'HOUSEHOLD COUNT'] + overview_non_dbt.loc[2,'HOUSEHOLD COUNT']
total_ind_benefits = overview_dbt.loc[22,'BENEFICIARIES COUNT'] + overview_non_dbt.loc[2,'BENEFICIARIES COUNT']
total_amt_benefits = overview_dbt.loc[22,'AMOUNT(crores)'] + overview_non_dbt.loc[2,'AMOUNT(crores)']
total_amt_benefits_round_fig = round(total_amt_benefits/100000,1)
total_hh_benefits_round_fig = round(total_hh_benefits/10000000,2)
total_ind_benefits_round_fig = round(total_ind_benefits/10000000,2)

statewise_dbt = pd.read_csv('statewise_dbt.csv')
statewise_dbt = statewise_dbt.fillna('')

statewise_non_dbt = pd.read_csv('statewise_non_dbt.csv')
statewise_non_dbt = statewise_non_dbt.fillna('')

statewise_dbt_non_dbt = pd.read_csv('statewise_dbt_non_dbt.csv')
statewise_dbt_non_dbt = statewise_dbt_non_dbt.fillna('')
total_pop = round(statewise_dbt_non_dbt.loc[13,'Total Citizens']/10000000,2)
total_unique_ben = round(statewise_dbt_non_dbt.loc[13,'Unique Beneficiaries']/10000000,2)
total_household = round(statewise_dbt_non_dbt.loc[13,'Total Households']/10000000,2)
total_unique_hh = round(statewise_dbt_non_dbt.loc[13,'Unique Household Beneficiaries']/10000000,2)

card_data_1 = {'benefits':['total_hh_benefits',
               'total_ind_benefits',
               'total_amt_benefits',
               'total_amt_benefits_round_fig',
               'total_hh_benefits_round_fig',
               'total_ind_benefits_round_fig'],
               'Values':[total_hh_benefits,
               total_ind_benefits,
               total_amt_benefits,
               total_amt_benefits_round_fig,
               total_hh_benefits_round_fig,
               total_ind_benefits_round_fig]}


card_data_1 = pd.DataFrame(card_data_1)

card_data_2 = {'benefits':['total_pop',
               'total_unique_ben',
               'total_household',
               'total_unique_hh',],
               'Values':[total_pop,
               total_unique_ben,
               total_household,
               total_unique_hh]}


card_data_2 = pd.DataFrame(card_data_2)

def dist_filter(d,dist):
    if d=='DBT':
        dbt_dist_uni = pd.read_csv('dbt_dist_uni.csv')
        dbt_dist_uni = dbt_dist_uni.fillna('')
        dbt_dist_uni['District'] = dbt_dist_uni['District'].replace('ANDHRA PRADESH','ALL')
        dbt_dist_uni_dd = dbt_dist_uni[dbt_dist_uni['District']==dist]
        dbt_dist_uni_dd.reset_index(inplace = True)

        dbt_dist_hh = pd.read_csv('dbt_dist_hh.csv')
        dbt_dist_hh = dbt_dist_hh.fillna('')
        dbt_dist_hh['District'] = dbt_dist_hh['District'].replace('ANDHRA PRADESH','ALL')
        dbt_dist_hh_dd = dbt_dist_hh[dbt_dist_hh['District']==dist]
        dbt_dist_hh_dd.reset_index(inplace = True)
    if d=='NON-DBT':
        dbt_dist_uni = pd.read_csv('non_dbt_dist_uni.csv')
        dbt_dist_uni = dbt_dist_uni.fillna('')
        dbt_dist_uni['District'] = dbt_dist_uni['District'].replace('ANDHRA PRADESH','ALL')
        dbt_dist_uni_dd = dbt_dist_uni[dbt_dist_uni['District']==dist]
        dbt_dist_uni_dd.reset_index(inplace = True)

        dbt_dist_hh = pd.read_csv('non_dbt_dist_hh.csv')
        dbt_dist_hh = dbt_dist_hh.fillna('')
        dbt_dist_hh['District'] = dbt_dist_hh['District'].replace('ANDHRA PRADESH','ALL')
        dbt_dist_hh_dd = dbt_dist_hh[dbt_dist_hh['District']==dist]
        dbt_dist_hh_dd.reset_index(inplace = True)
    if d=='DBT + NON-DBT':
        dbt_dist_uni = pd.read_csv('dbt_non_dbt_dist_uni.csv')
        dbt_dist_uni = dbt_dist_uni.fillna('')
        dbt_dist_uni['District'] = dbt_dist_uni['District'].replace('ANDHRA PRADESH','ALL')
        dbt_dist_uni_dd = dbt_dist_uni[dbt_dist_uni['District']==dist]
        dbt_dist_uni_dd.reset_index(inplace = True)

        dbt_dist_hh = pd.read_csv('dbt_non_dbt_dist_hh.csv')
        dbt_dist_hh = dbt_dist_hh.fillna('')
        dbt_dist_hh['District'] = dbt_dist_hh['District'].replace('ANDHRA PRADESH','ALL')
        dbt_dist_hh_dd = dbt_dist_hh[dbt_dist_hh['District']==dist]
        dbt_dist_hh_dd.reset_index(inplace = True)
        
    dbt_dist_uni_dd_data = {'labels':['District',
                        'Population',
                        'Unique Beneficiaries',
                        'Beneficiaries(1 scheme)',
                        'Beneficiaries(2 schemes)',
                        'Beneficiaries(more than 2 schemes)',
                        'Total Households',
                        'Household Benefitted',
                        'Household benefitted(1 scheme)',
                        'Household benefitted(2 schemes)',
                        'Household benefitted(more than 2 schemes)'],
                        'Values':[dbt_dist_uni_dd.loc[0,'District'],
                        dbt_dist_uni_dd.loc[0,'Total Citizens'],
                        dbt_dist_uni_dd.loc[0,'Unique Beneficiaries'],
                        dbt_dist_uni_dd.loc[0,'Beneficiaries with 1 Scheme'],
                        dbt_dist_uni_dd.loc[0,'Beneficiaries with 2 Scheme'],
                        dbt_dist_uni_dd.loc[0,'Beneficiaries with more than 2 Scheme'],
                        dbt_dist_hh_dd.loc[0,'Total Households'],
                        dbt_dist_hh_dd.loc[0,'Households Benefitted'],
                        dbt_dist_hh_dd.loc[0,'Households Benefitted with 1 Scheme'],
                        dbt_dist_hh_dd.loc[0,'Households Benefitted with 2 Scheme'],
                        dbt_dist_hh_dd.loc[0,'Households Benefitted with more than 2 Scheme']]
                        }
    card_data_3 = pd.DataFrame(dbt_dist_uni_dd_data)
    return card_data_3

def flag_filter(d,flag):
    if d=='DBT':
        dbt_flag_hh = pd.read_csv('dbt_flag_hh.csv')
        dbt_flag_hh_dd = dbt_flag_hh[dbt_flag_hh['CATEGORY']==flag]
        dbt_flag_hh_dd.reset_index(inplace = True)
    if d=='NON-DBT':
       

        dbt_flag_hh = pd.read_csv('non_dbt_flag_hh.csv')
        dbt_flag_hh_dd = dbt_flag_hh[dbt_flag_hh['CATEGORY']==flag]
        dbt_flag_hh_dd.reset_index(inplace = True)
    if d=='DBT + NON-DBT':
        dbt_flag_hh = pd.read_csv('dbt_non_dbt_flag_hh.csv')
        dbt_flag_hh_dd = dbt_flag_hh[dbt_flag_hh['CATEGORY']==flag]
        dbt_flag_hh_dd.reset_index(inplace = True)
        
    dbt_flag_hh_dd_data = {'labels':['CATEGORY',
                        'Total Households',
                        'Household Benefitted',
                        'Household benefitted(1 scheme)',
                        'Household benefitted(2 schemes)',
                        'Household benefitted(more than 2 schemes)'],
                        'Values':[dbt_flag_hh_dd.loc[0,'CATEGORY'],
                        dbt_flag_hh_dd.loc[0,'Total Households'],
                        dbt_flag_hh_dd.loc[0,'Households Benefitted'],
                        dbt_flag_hh_dd.loc[0,'Households Benefitted with 1 Scheme'],
                        dbt_flag_hh_dd.loc[0,'Households Benefitted with 2 Scheme'],
                        dbt_flag_hh_dd.loc[0,'Households Benefitted with more than 2 Scheme']]
                        }
    card_data_4 = pd.DataFrame(dbt_flag_hh_dd_data)
    return card_data_4

def transfer_mode_filter_for_amt_range(d):
    if d=='DBT':
        amt_range_hh = pd.read_csv('amt_range_dbt_hh.csv')
        amt_range_hh_amount = pd.read_csv('amt_range_dbt_hh_amount.csv')
    if d=='NON-DBT':
        amt_range_hh = pd.read_csv('amt_range_non_dbt_hh.csv')
        amt_range_hh_amount = pd.read_csv('amt_range_non_dbt_hh_amount.csv')
    if d=='DBT + NON-DBT':
         amt_range_hh = pd.read_csv('amt_range_dbt_non_dbt_hh.csv')
         amt_range_hh_amount = pd.read_csv('amt_range_dbt_non_dbt_hh_amount.csv')
    
    if d=='DBT':
        amt_range_ben = pd.read_csv('amt_range_dbt_ben.csv')
        amt_range_ben_amount = pd.read_csv('amt_range_dbt_ben_amount.csv')
    if d=='NON-DBT':
        amt_range_ben = pd.read_csv('amt_range_non_dbt_ben.csv')
        amt_range_ben_amount = pd.read_csv('amt_range_non_dbt_ben_amount.csv')
    if d=='DBT + NON-DBT':
         amt_range_ben = pd.read_csv('amt_range_dbt_non_dbt_ben.csv')
         amt_range_ben_amount = pd.read_csv('amt_range_dbt_non_dbt_ben_amount.csv')
    

    return amt_range_hh,amt_range_ben,amt_range_hh_amount,amt_range_ben_amount


one_scheme_top_5 = pd.read_csv('one_Scheme_top_5.csv')
one_scheme_top_5.sort_values('Scheme Name',inplace = True)

two_scheme_top_5 = pd.read_csv('two_Scheme_top_5.csv')
two_scheme_top_5.sort_values('Scheme Name',inplace = True)

three_scheme_top_5 = pd.read_csv('three_Scheme_top_5.csv')
three_scheme_top_5.sort_values('Scheme Name',inplace = True)

one_scheme_top_5_ben = pd.read_csv('one_scheme_top_5_ben.csv')
one_scheme_top_5_ben.sort_values('Scheme Name',inplace = True)

two_scheme_top_5_ben = pd.read_csv('two_scheme_top_5_ben.csv')
two_scheme_top_5_ben.sort_values('Scheme Name',inplace = True)

three_scheme_top_5_ben = pd.read_csv('three_scheme_top_5_ben.csv')
three_scheme_top_5_ben.sort_values('Scheme Name',inplace = True)

scheme_avg_amt_hh = pd.read_csv('scheme_avg_amt_hh.csv')
scheme_avg_amt_ben = pd.read_csv('scheme_avg_amt_ben.csv')

bg_image = 'url(https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/jagan_sir_background_image.JPG?raw=true)'

colors = {
    'background': 'rgba(0, 179, 60, 0.4)',
    'bodyColor':'#F2DFCE',
    'textcolor': 'white'
}

###-------------page header--------------#########
def get_page_heading_style():
    return {'backgroundColor': colors['background'],#'width':'100%',
                                    'height':'100px','margin-top':'20px'}


def get_page_heading_title():
    return html.H1(children="STATE's WELFARE SCHEMES BENEFICIARIES ANALYSIS",
                                        style={
                                        'textAlign': 'center',
                                        'color': colors['textcolor'],
                                    'fontWeight':'bold',
                                    'font-family': "'sans-serif'",
                                    'padding-top':'25px',
                                    'textAlign':'center'})
                                    


def generate_page_header():
    main_header =  dbc.Row(
                            [
                                dbc.Col(get_page_heading_title(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
   
    header = main_header
    return header


############----------------end page header--------------#########


def generate_card_content(string,card_value,string2,exact_card_value,img_address,inp):
    card_image = dbc.CardImg(src=img_address, top=True,style = {'backgroundColor':'blue'})
    card_head_style = {'textAlign':'center','fontSize':'100%'}
    card_title_style = {'textAlign':'center','fontSize':'200%'}
    card_subtitle_style = {'textAlign':'center','fontSize':'100%'}
    
    card_header = dbc.CardHeader(string,style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H5(children = [f"{(card_value):,}",html.Span(children = string2,style = {'fontSize':'50%'})],className="card-title",style=card_title_style),
            html.H6(children = [html.Span(inp,style = {'fontSize':'75%'}),f"{(exact_card_value):,}"], className="sub-title",style=card_subtitle_style)
            
        ]
    )
    card = [card_image,card_header,card_body]
    return card

def generate_card_content1(d,string,card_value,string2,exact_card_value,img_address,inp,dist):
    card_image = dbc.CardImg(src=img_address, top=True,style = {'backgroundColor':'blue'})
    card_head_style = {'textAlign':'center','fontSize':'100%'}
    card_title_style = {'textAlign':'center','fontSize':'150%'}
    card_subtitle_style = {'textAlign':'center','fontSize':'100%'}
    card_subtitle2_style = {'textAlign':'center','fontSize':'100%'}    
    card_header = dbc.CardHeader(string+'('+dist+')',style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H6(children = [d], className="sub-title2",style=card_subtitle2_style),
            html.H5(children = [f"{(card_value):,}",html.Span(children = string2,style = {'fontSize':'50%'})],className="card-title",style=card_title_style),
            html.H6(children = [f"{(exact_card_value):,}",html.Span('('+inp+')',style = {'fontSize':'75%'})], className="sub-title",style=card_subtitle_style)
            
        ]
    )
    card = [card_image,card_header,card_body]
    return card

def generate_card_content2(d,string,card_value,string2,exact_card_value,img_address,inp,flag):
    card_image = dbc.CardImg(src=img_address, top=True,style = {'backgroundColor':'blue'})
    card_head_style = {'textAlign':'center','fontSize':'100%'}
    card_title_style = {'textAlign':'center','fontSize':'150%'}
    card_subtitle_style = {'textAlign':'center','fontSize':'100%'}
    card_subtitle2_style = {'textAlign':'center','fontSize':'100%'}    
    card_header = dbc.CardHeader(string+'('+flag+')',style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H6(children = [d], className="sub-title2",style=card_subtitle2_style),
            html.H5(children = [f"{(card_value):,}",html.Span(children = string2,style = {'fontSize':'50%'})],className="card-title",style=card_title_style),
            html.H6(children = [f"{(exact_card_value):,}",html.Span('('+inp+')',style = {'fontSize':'75%'})], className="sub-title",style=card_subtitle_style)
            
        ]
    )
    card = [card_image,card_header,card_body]
    return card


def generate_cards1():
    total_ind_benefits = card_data_1.loc[1,'Values']
    total_hh_benefits = card_data_1.loc[0,'Values']
    total_amt_benefits = card_data_1.loc[2,'Values']
    total_amt_benefits_round_fig = card_data_1.loc[3,'Values']
    total_ind_benefits_round_fig = card_data_1.loc[5,'Values']
    total_hh_benefits_round_fig = card_data_1.loc[4,'Values']
    img_ind = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/people_image.jpg?raw=true'
    #img_hh = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/house.jpg?raw=true'
    img_money = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/money_bag.jpg?raw=true'
    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(generate_card_content("TOTAL BENEFITS",total_ind_benefits_round_fig,' Crores',total_ind_benefits,img_ind,'Exact Value-:'), color="success", inverse=True,style={'width':'13rem','height':'21rem','margin':'20px 20px 20px 20px'}),md=dict(size=2)),
                   #dbc.Col(dbc.Card(generate_card_content("TOTAL BENEFITS AVAILED BY HOUSEHOLDS",total_hh_benefits_round_fig,' Crores',total_hh_benefits,img_hh,'Exact Value'), color="success", inverse=True,style={'width':'13rem','height':'21rem','margin':'20px 20px 20px 20px'}),md=dict(size=2)),
                   dbc.Col(dbc.Card(generate_card_content("TOTAL BENEFITS IN MONETARY TERMS",total_amt_benefits_round_fig,' Lacs Crores',total_amt_benefits,img_money,'Exact Value-:'), color="success", inverse=True,style={'width':'13rem','height':'21rem','margin':'20px 20px 20px 20px'}),md=dict(size=2))
                ],
                className="mb-4",
            ),
        ],id='card1'
    )
    return cards

def generate_cards2():
    total_pop = card_data_2.loc[0,'Values']
    total_unique_ben = card_data_2.loc[1,'Values']
    total_household = card_data_2.loc[2,'Values']
    total_unique_hh = card_data_2.loc[3,'Values']

    img_ind = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/family.jpg?raw=true'
    img_hh = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/house.png?raw=true'
    #img_money = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/money_bag.jpg?raw=true'
    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(generate_card_content("TOTAL UNIQUE BENEFICIARIES",total_unique_ben,' Crores',total_pop,img_ind,'Population(crores)-: '), color="blue", inverse=True,style={'width':'13rem','height':'21rem','margin':'20px 20px 20px 20px'}),md=dict(size=2)),
                   dbc.Col(dbc.Card(generate_card_content("TOTAL HOUSEHOLD BENEFITED",total_unique_hh,' Crores',total_household,img_hh,'Total Household(crores)-: '), color="blue", inverse=True,style={'width':'13rem','height':'21rem','margin':'20px 20px 20px 20px'}),md=dict(size=2)),
                   #dbc.Col(dbc.Card(generate_card_content("TOTAL BENEFITS AVAILED IN MONETARY TERMS",total_amt_benefits_round_fig,' Lacs Crores',total_amt_benefits,img_money), color="success", inverse=True,style={'width':'13rem','height':'21rem','margin':'20px 20px 20px 20px'}),md=dict(size=2))
                ],
                className="mb-4",
            ),
        ],id='card2'
    )
    return cards

def generate_cards3(d,dist):
    card_data_3 = dist_filter(d,dist)
    district_name = card_data_3.loc[0,'Values']
    total_pop = card_data_3.loc[1,'Values']
    total_unique_ben = card_data_3.loc[2,'Values']
    total_household = card_data_3.loc[6,'Values']
    total_unique_hh = card_data_3.loc[7,'Values']

    img_ind = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/family.jpg?raw=true'
    img_hh = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/house.png?raw=true'
    #img_money = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/money_bag.jpg?raw=true'
    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(generate_card_content1(d,"TOTAL UNIQUE BENEFICIARIES",total_unique_ben,'',total_pop,img_ind,'Population',district_name), color="#800015", inverse=True,style={'width':'18rem','height':'24rem','margin':'20px 20px 20px 20px'}),md=dict(size=2,offset = 3)),
                    dbc.Col(dbc.Card(generate_card_content1(d,"TOTAL HOUSEHOLD BENEFITED",total_unique_hh,' ',total_household,img_hh,'Total Household',district_name), color="#800015", inverse=True,style={'width':'18rem','height':'24rem','margin':'20px 20px 20px 20px'}),md=dict(size=2,offset= 5))
                ],
                className="mb-4",
            )
            
        ],id='card3'
    )
    return cards

def generate_cards4(d,flag):
    card_data_3 = flag_filter(d,flag)
    flag_name = card_data_3.loc[0,'Values']
    #total_pop = card_data_3.loc[1,'Values']
    #total_unique_ben = card_data_3.loc[2,'Values']
    total_household = card_data_3.loc[1,'Values']
    total_unique_hh = card_data_3.loc[2,'Values']

    img_ind = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/family.jpg?raw=true'
    if flag=='RURAL':
        img_hh = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/rural.jpg?raw=true'
    if flag=='URBAN':
        img_hh = 'https://github.com/Piyush-Tanwar/my_data/blob/gh-pages/urban.jpg?raw=true'
    cards = html.Div(
        [
            dbc.Row(
                [
                    #dbc.Col(dbc.Card(generate_card_content2(d,"TOTAL UNIQUE BENEFICIARIES",total_unique_ben,'',total_pop,img_ind,'Population',flag_name), color="#800015", inverse=True,style={'width':'18rem','height':'24rem','margin':'20px 20px 20px 20px'}),md=dict(size=2,offset = 3)),
                    dbc.Col(dbc.Card(generate_card_content2(d,"TOTAL HOUSEHOLD BENEFITED",total_unique_hh,' ',total_household,img_hh,'Total Household',flag_name), color="#800015", inverse=True,style={'width':'18rem','height':'24rem','margin':'20px 20px 20px 20px'}),md=dict(size=2,offset=1))
                ],
                className="mb-4",
            )
            
        ],id='card4'
    )
    return cards

####--------------create table for schemewise data-------####

def Total_ben_count_table_dash_dbt(data,last_row):
      
        
        Table = dash_table.DataTable(
            id='table1',
            columns=[{"name": i, "id": i}
                     for i in data.columns],
            data=data.to_dict('records'),
            fixed_rows={ 'headers': True, 'data': 0 },
            style_cell=dict(textAlign='left',fontSize = 10,fontFamily = 'sans-serif'),
            style_header={'backgroundColor':"paleturquoise",'fontWeight': 'bold','border': '1px solid'},
            style_data={'backgroundColor':"white",'border': '2px solid'},
            style_data_conditional=[
            {
                'if': {'row_index': last_row},
                'backgroundColor': 'grey',
                'fontWeight':'bold',
                'text-align':'center',
                #'border':'1px solid',
                'fontSize':15
            }
            ],
            style_cell_conditional=[
        {
            'if': {'column_id': ['HOUSEHOLD COUNT','BENEFICIARIES COUNT','AMOUNT(crores)']},
            'textAlign': 'center'
        } 
    ],
            style_table = {'height':'300px','width':'660px'}
            )
        return Table

def Total_ben_count_table_dash_non_dbt(data,last_row):
      
        
        Table = dash_table.DataTable(
            id='table2',
            columns=[{"name": i, "id": i}
                     for i in data.columns],
            data=data.to_dict('records'),
            #fixed_rows={ 'headers': True, 'data': 0 },
            style_cell=dict(textAlign='left',fontSize = 10,fontFamily = 'sans-serif'),
            style_header={'backgroundColor':"paleturquoise",'fontWeight': 'bold','border': '1px solid'},
            style_data={'backgroundColor':"white",'border': '2px solid'},
            style_data_conditional=[
            {
                'if': {'row_index': last_row},
                'backgroundColor': 'grey',
                'fontWeight':'bold',
                'text-align':'center',
                #'border':'1px solid',
                'fontSize':20
            }
            ],
            style_cell_conditional=[
        {
            'if': {'column_id': ['HOUSEHOLD COUNT','BENEFICIARIES COUNT','AMOUNT(crores)']},
            'textAlign': 'center'
        } 
    ],
            style_table = {'height':'auto','width':'660px'}
            )
        return Table
    
def scheme_amt_avg_hh(data):
      
        
        Table = dash_table.DataTable(
            id='table3',
            columns=[{"name": i, "id": i}
                     for i in data.columns],
            data=data.to_dict('records'),
            #fixed_rows={ 'headers': True, 'data': 0 },
            style_cell=dict(textAlign='left',fontSize = 10,fontFamily = 'sans-serif'),
            style_header={'backgroundColor':"paleturquoise",'fontWeight': 'bold','border': '1px solid'},
            style_data={'backgroundColor':"white",'border': '2px solid'},
            #style_data_conditional=[
            #{
             #   'if': {'row_index': last_row},
              #  'backgroundColor': 'grey',
               # 'fontWeight':'bold',
                #'text-align':'center',
                #'border':'1px solid',
                #'fontSize':20
            #}
            #],
            #style_cell_conditional=[
        #{
         #   'if': {'column_id': ['HOUSEHOLD COUNT','BENEFICIARIES COUNT','AMOUNT(crores)']},
          #  'textAlign': 'center'
        #} 
    #],
            style_table = {'height':'auto','width':'300px'}
            )
        return Table
    
def scheme_amt_avg_ben(data):
      
        
        Table = dash_table.DataTable(
            id='table4',
            columns=[{"name": i, "id": i}
                     for i in data.columns],
            data=data.to_dict('records'),
            #fixed_rows={ 'headers': True, 'data': 0 },
            style_cell=dict(textAlign='left',fontSize = 10,fontFamily = 'sans-serif'),
            style_header={'backgroundColor':"paleturquoise",'fontWeight': 'bold','border': '1px solid'},
            style_data={'backgroundColor':"white",'border': '2px solid'},
            #style_data_conditional=[
            #{
             #   'if': {'row_index': last_row},
              #  'backgroundColor': 'grey',
               # 'fontWeight':'bold',
                #'text-align':'center',
                #'border':'1px solid',
                #'fontSize':20
            #}
            #],
            #style_cell_conditional=[
        #{
         #   'if': {'column_id': ['HOUSEHOLD COUNT','BENEFICIARIES COUNT','AMOUNT(crores)']},
          #  'textAlign': 'center'
        #} 
    #],
            style_table = {'height':'auto','width':'300px'}
            )
        return Table
#####--------------end table creation----------#####

##----------------plot pie chart for schemes-------##
def pie_chart(title,value,name):

    
    fig = px.pie(names = name,values = value)
    fig.update_traces(#textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2))) 
    fig.update_layout(legend=dict(
    #orientation="h",
    #yanchor="bottom",
    #y=1.02,
    #xanchor="center",
    x=1.3),
    autosize=False,
    width=600,
    height=500,title_text='<b>'+title+'<b>', title_x=0.5,title_font_family="Times New Roman",
    title_font_color="#800015",title_font_size = 15)
    return fig

def pie_chart2(title,d,dist):
    colors = ['red','green','blue']
    card_data_3 = dist_filter(d,dist)
    data = card_data_3.iloc[3:6,:]
    names = data.iloc[:,0].tolist()
    values = data.iloc[:,1].tolist()    
    fig = px.pie(data,names = names,values = values)
    fig.update_traces(#textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2),colors = colors)) 
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    #y=1.02,
    xanchor="center",
    x=1.3),
    autosize=False,
    width=600,
    height=500,title_text='<b>'+title+ dist+'('+d+')'+'<b>', title_x=0.5,title_font_family="Times New Roman",
    title_font_color="#800015",title_font_size = 15)
    return fig

def pie_chart3(title,d,dist):
    colors = ['red','green','blue']
    card_data_3 = dist_filter(d,dist)
    data = card_data_3.iloc[8:11,:]
    names = data.iloc[:,0].tolist()
    values = data.iloc[:,1].tolist()    
    fig = px.pie(data,names = names,values = values)
    fig.update_traces(#textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2),colors = colors)) 
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    #y=1.02,
    xanchor="center",
    x=1.3),
    autosize=False,
    width=600,
    height=500,title_text='<b>'+title+ dist+'('+d+')'+'<b>', title_x=0.5,title_font_family="Times New Roman",
    title_font_color="#800015",title_font_size = 15)
    return fig

def pie_chart4(title,d,flag):
    colors = ['red','green','blue']
    card_data_3 = flag_filter(d,flag)
    data = card_data_3.iloc[3:6,:]
    names = data.iloc[:,0].tolist()
    values = data.iloc[:,1].tolist()    
    fig = px.pie(data,names = names,values = values)
    fig.update_traces(#textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2),colors = colors)) 
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    #y=1.02,
    xanchor="center",
    x=1.3),
    autosize=False,
    width=600,
    height=500,title_text='<b>'+title+ flag+'('+d+')'+'<b>', title_x=0.5,title_font_family="Times New Roman",
    title_font_color="#800015",title_font_size = 15)
    return fig

def pie_chart5(title,d):
    
    a,b,c,d = transfer_mode_filter_for_amt_range(d)
    data = a
    names = data.iloc[:,0].tolist()
    values = data.iloc[:,1].tolist()    
    fig = px.pie(data,names = names,values = values)
    fig.update_traces(#textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2))) 
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    #y=1.02,
    xanchor="center",
    x=1.3),
    autosize=False,
    width=600,
    height=500,
    title_text='<b>'+title+'<b>', title_x=0.5,title_font_family="Times New Roman",
    title_font_color="#800015",title_font_size = 15)
    return fig

def pie_chart6(title,d):
    colors = ['red','green','blue']
    a,b,c,d = transfer_mode_filter_for_amt_range(d)
    data = c
    names = data.iloc[:,0].tolist()
    values = data.iloc[:,1].tolist()    
    fig = px.pie(data,names = names,values = values)
    fig.update_traces(#textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2))) 
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    #y=1.02,
    xanchor="center",
    x=1.3),
    autosize=False,
    width=600,
    height=500,
    title_text='<b>'+title+'<b>', title_x=0.5,title_font_family="Times New Roman",
    title_font_color="#800015",title_font_size = 15)
    return fig

def pie_chart7(title,d):
    colors = ['red','green','blue']
    a,b,c,d = transfer_mode_filter_for_amt_range(d)
    data = b
    names = data.iloc[:,0].tolist()
    values = data.iloc[:,1].tolist()    
    fig = px.pie(data,names = names,values = values)
    fig.update_traces(#textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2))) 
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    #y=1.02,
    xanchor="center",
    x=1.3),
    autosize=False,
    width=600,
    height=500,
    title_text='<b>'+title+'<b>', title_x=0.5,title_font_family="Times New Roman",
    title_font_color="#800015",title_font_size = 15)
    return fig

def pie_chart8(title,d):
    colors = ['red','green','blue']
    a,b,c,d = transfer_mode_filter_for_amt_range(d)
    data = d
    names = data.iloc[:,0].tolist()
    values = data.iloc[:,1].tolist()    
    fig = px.pie(data,names = names,values = values)
    fig.update_traces(#textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2))) 
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    #y=1.02,
    xanchor="center",
    x=1.3),
    autosize=False,
    width=600,
    height=500,
    title_text='<b>'+title+'<b>', title_x=0.5,title_font_family="Times New Roman",
    title_font_color="#800015",title_font_size = 15)
    return fig

def graph1(title,value,name):
    return dcc.Graph(id='pie_chart1',figure=pie_chart(title,value,name))

def graph2(title,value,name):
    return dcc.Graph(id='pie_chart2',figure=pie_chart(title,value,name))

def graph3(title,value,name):
    return dcc.Graph(id='pie_chart3',figure=pie_chart(title,value,name))

def graph4(title,value,name):
    return dcc.Graph(id='pie_chart4',figure=pie_chart(title,value,name))


def graph5(title,d,dist):
    return dcc.Graph(id='pie_chart5',figure=pie_chart2(title,d,dist))

def graph6(title,d,dist):
    return dcc.Graph(id='pie_chart6',figure=pie_chart3(title,d,dist))

def graph9(title,d,flag):
    return dcc.Graph(id='pie_chart7',figure=pie_chart4(title,d,flag))

def graph14(title,d):
    return dcc.Graph(id='pie_chart8',figure=pie_chart5(title,d))

def graph15(title,d):
    return dcc.Graph(id='pie_chart9',figure=pie_chart6(title,d))

def graph16(title,d):
    return dcc.Graph(id='pie_chart10',figure=pie_chart7(title,d))

def graph17(title,d):
    return dcc.Graph(id='pie_chart11',figure=pie_chart8(title,d))

##====================end pie chart plot----------####

###---------------------bar plot====================####
def bar_chart_1(title,df):
    colors = ['red','blue','green','yellow','orange','black']
    top_5 = df['Scheme Name']

    fig = go.Figure(data=[
        go.Bar(name='Schemes', x=top_5, y=df['percent'],marker_color = colors,width = [0.5,0.5,0.5,0.5,0.5,0.5])
    ])
# Change the bar mode
    fig.update_layout(width = 600,height=600,yaxis_tickformat = '%',title_text='<b>'+title+'<b>', title_x=0.5,title_font_family="Times New Roman",title_font_color="#800015",title_font_size = 20)
    return fig

def bar_chart_2(title,df):
    colors = ['red','blue','green','yellow','orange','black']
    top_5 = df['Scheme Name']

    fig = go.Figure(data=[
        go.Bar(name='Schemes', x=top_5, y=df['percent'],marker_color = colors,width = [0.5,0.5,0.5,0.5,0.5,0.5])
    ])
# Change the bar mode
    fig.update_layout(width = 800,height=600,yaxis_tickformat = '%',title_text='<b>'+title+'<b>', title_x=0.5,title_font_family="Times New Roman",title_font_color="#800015",title_font_size = 20)
    return fig


def graph7(title,df):
    return dcc.Graph(id='bar_chart1',figure=bar_chart_1(title,df))

def graph8(title,df):
    return dcc.Graph(id='bar_chart2',figure=bar_chart_1(title,df))

def graph10(title,df):
    return dcc.Graph(id='bar_chart3',figure=bar_chart_2(title,df))

def graph11(title,df):
    return dcc.Graph(id='bar_chart4',figure=bar_chart_1(title,df))

def graph12(title,df):
    return dcc.Graph(id='bar_chart5',figure=bar_chart_1(title,df))

def graph13(title,df):
    return dcc.Graph(id='bar_chart6',figure=bar_chart_2(title,df))

##---------------------drop down------------------####
def first_drop_down():
    first_list = ['DBT','NON-DBT','DBT + NON-DBT']
    return first_list

def second_drop_down():
    second_list = ['SRIKAKULAM',
                  'VIZIANAGARAM',
                  'VISAKHAPATNAM',
                  'EAST GODAVARI',
                  'WEST GODAVARI',
                  'KRISHNA',
                  'GUNTUR',
                  'PRAKASAM',
                  'CHITTOOR',
                  'NELLORE',
                  'KURNOOL',
                  'KADAPA',
                  'ANANATAPUR',
                  'ALL'
                  ]
    return second_list

def third_drop_down():
    third_list = ['RURAL','URBAN']
    return third_list

def fourth_drop_down():
    first_list = ['DBT','NON-DBT','DBT + NON-DBT']
    return first_list

def fifth_drop_down():
    first_list = ['DBT','NON-DBT','DBT + NON-DBT']
    return first_list

def create_dropdown_list(list_1):
    dropdown_list = []
    for li in sorted(list_1):
        tmp_dict = {'label':li,'value':li}
        dropdown_list.append(tmp_dict)
    return dropdown_list

def get_first_dropdown():
    return html.Div([
                        html.Label(''),
                        dcc.Dropdown(id='my-id1',
                            options=create_dropdown_list(first_drop_down()),
                            value='DBT + NON-DBT'
                        ),
                        html.Div(id='my-div1')
                    ])

def get_second_dropdown():
    return html.Div([
                        html.Label(''),
                        dcc.Dropdown(id='my-id2',
                            options=create_dropdown_list(second_drop_down()),
                            value='ALL'
                        ),
                        html.Div(id='my-div2')
                    ])

def get_third_dropdown():
    return html.Div([
                        html.Label(''),
                        dcc.Dropdown(id='my-id3',
                            options=create_dropdown_list(third_drop_down()),
                            value='RURAL'
                        ),
                        html.Div(id='my-div3')
                    ])

def get_fourth_dropdown():
    return html.Div([
                        html.Label(''),
                        dcc.Dropdown(id='my-id4',
                            options=create_dropdown_list(first_drop_down()),
                            value='DBT + NON-DBT'
                        ),
                        html.Div(id='my-div4')
                    ])

def get_fifth_dropdown():
    return html.Div([
                        html.Label(''),
                        dcc.Dropdown(id='my-id5',
                            options=create_dropdown_list(first_drop_down()),
                            value='DBT + NON-DBT'
                        ),
                        html.Div(id='my-div5')
                    ])

### -------------drop down ends -----------------------##############

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'State Welfare Scheme Analysis'

def generate_layout():
    page_header = generate_page_header()
    layout = dbc.Container(
        [
            page_header,
            generate_cards1(),
            generate_cards2(),
            dbc.Row([dbc.Col(html.Div([html.Label('DBT Scheme Wise Household & Beneficiaries overview'),Total_ben_count_table_dash_dbt(overview_dbt,len(overview_dbt)-1)],style={'fontWeight':'bold','position':'relative','left':'20px','margin':'20px 20px 20px 20px'}),style={'margin':'5px 5px 5px 5px','padding-left':'250px'}),
                     
                     ]),
            dbc.Row([dbc.Col(graph1('DBT SCHEMEWISE(BENEFICIARIES)',overview_dbt.iloc[:21,3].tolist(),overview_dbt.iloc[:21,1].tolist())),
                     dbc.Col(graph2('DBT SCHEMEWISE(HOUSEHOLD)',overview_dbt.iloc[:21,2].tolist(),overview_dbt.iloc[:21,1].tolist()))
                     ]),
            dbc.Row(html.Div([html.Label('Non-DBT Scheme Wise Household & Beneficiaries overview'),Total_ben_count_table_dash_non_dbt(overview_non_dbt,len(overview_non_dbt)-1)],style={'margin':'20px 20px 20px 20px','position':'relative','left':'20px','fontWeight':'bold'}),style={'margin':'5px 5px 5px 5px','padding-left':'250px'}),
            dbc.Row([dbc.Col(graph3('NON-DBT SCHEMEWISE(BENEFICIARIES)',overview_non_dbt.iloc[:2,3].tolist(),overview_non_dbt.iloc[:2,1].tolist())),
                     dbc.Col(graph4('NON-DBT SCHEMEWISE(HOUSEHOLD)',overview_non_dbt.iloc[:2,2].tolist(),overview_non_dbt.iloc[:2,1].tolist()))
                     ]),
            dbc.Row(
                [
                    dbc.Col(get_first_dropdown(),md=dict(size=4,offset=4))                    
                ]
            
            ),
            dbc.Row(
                [
                    dbc.Col(get_second_dropdown(),md=dict(size=4,offset=4))                    
                ]
            
            ),
            dbc.Row(
                [
                    generate_cards3('DBT','KRISHNA'),
                
                ],style= {'margin-top':'90px'}
            
            ),
            dbc.Row(
                [
                    dbc.Col(graph5('Unique Beneficiaries with No. of schemes in ','DBT','ALL')),
                    dbc.Col(graph6('Households with No. of schemes in ','DBT','ALL'))
                
                ]
            
            ), dbc.Row(
                [
                    dbc.Col(get_fourth_dropdown(),md=dict(size=4,offset=4))                    
                ]
            
            ),
            
             dbc.Row(
                [
                    dbc.Col(get_third_dropdown(),md=dict(size=4,offset=4))                    
                ]
            
            ),
            
            dbc.Row(
                [
                    generate_cards4('DBT','RURAL'),
                    dbc.Col(graph9('Househoulds with No. of schemes in ','DBT','RURAL'),md=dict(size=2,offset = 2))
                
                ],style= {'margin-top':'90px'}
            
            ),
            
             dbc.Row(
                [
                    dbc.Col(get_fifth_dropdown(),md=dict(size=4,offset=4))                    
                ]
            
            ),
             dbc.Row([dbc.Col(graph14('Household counts for different benefit amount ranges','DBT'),style={'padding-top':'10px'}),
                     dbc.Col(graph15('Total amount for different benefit amount ranges(household)','DBT'),style={'padding-top':'10px'})
                     ]),
             
             dbc.Row([dbc.Col(graph16('Beneficiaries counts for different benefit amount ranges','DBT'),style={'padding-top':'10px'}),
                     dbc.Col(graph17('Total amount for different benefit amount ranges(beneficiaries)','DBT'),style={'padding-top':'10px'})
                     ]),
             dbc.Row(
                [   
              #      dbc.Col(graph10('Household-wise 3 schemes Top 5 combinations(DBT)',three_scheme_top_5),md=dict(offset=1)),
                    dbc.Col(html.Div([html.Label('No. of schemes Average Amount(Household)'),scheme_amt_avg_hh(scheme_avg_amt_hh)],style={'fontWeight':'bold'}),style={'padding-top':'30px','padding-left':'450px'})
                ],style= {'margin-top':'20px'}
            
            ),
            dbc.Row(
                [
                    dbc.Col(graph7('Household-wise 1 scheme Top 5(DBT)',one_scheme_top_5)),
                    dbc.Col(graph8('Household-wise 2 schemes Top 5 combinations(DBT)',two_scheme_top_5))
                
                ],style= {'margin-top':'20px'}
            
            ),
            dbc.Row(
                [   
                    dbc.Col(graph10('Household-wise 3 schemes Top 5 combinations(DBT)',three_scheme_top_5),md=dict(offset=3)),
               #     dbc.Col(html.Div([html.Label('No. of schemes Average Amount(Household)'),scheme_amt_avg_hh(scheme_avg_amt_hh)],style={'fontWeight':'bold'}),style={'padding-top':'150px'})
                ],style= {'margin-top':'20px'}
            
            ),
            dbc.Row(
                [
                    
              #      dbc.Col(graph13('Beneficiary-wise 3 schemes Top 5 combinations(DBT)',three_scheme_top_5_ben)),
                    dbc.Col(html.Div([html.Label('No. of schemes Average Amount(Household)'),scheme_amt_avg_ben(scheme_avg_amt_ben)],style={'fontWeight':'bold'}),style={'padding-top':'30px','padding-left':'450px'}),
                
                ],style= {'margin-top':'20px'}
            
            ),
            dbc.Row(
                [
                    dbc.Col(graph11('Beneficiary-wise 1 scheme Top 5(DBT)',one_scheme_top_5_ben)),
                    dbc.Col(graph12('Beneficiary-wise 2 schemes Top 5 combinations(DBT)',two_scheme_top_5_ben))
                
                ],style= {'margin-top':'20px'}
            
            ),
            dbc.Row(
                [
                    
                    dbc.Col(graph13('Beneficiary-wise 3 schemes Top 5 combinations(DBT)',three_scheme_top_5_ben),md=dict(offset=3)),
                #    dbc.Col(html.Div([html.Label('No. of schemes Average Amount(Household)'),scheme_amt_avg_ben(scheme_avg_amt_ben)],style={'fontWeight':'bold'}),style={'padding-top':'150px'}),
                
                ],style= {'margin-top':'20px','padding-bottom':'30px'}
            
            )
        ],fluid=True,style={'background-image': bg_image}
    )
    return layout

app.layout = generate_layout()

@app.callback(
     Output(component_id = 'card3',component_property = 'children'),
     [Input(component_id = 'my-id1',component_property = 'value'),
      Input(component_id = 'my-id2',component_property = 'value')] #dropdown
)

def update_output_div(value1,value2):
   return generate_cards3(value1,value2)

@app.callback(
     Output(component_id = 'card4',component_property = 'children'),
     [Input(component_id = 'my-id4',component_property = 'value'),
      Input(component_id = 'my-id3',component_property = 'value')] #dropdown
)

def update_output_div(value1,value2):
   return generate_cards4(value1,value2)

@app.callback(
     Output(component_id = 'pie_chart5',component_property = 'figure'),
     [Input(component_id = 'my-id1',component_property = 'value'),
      Input(component_id = 'my-id2',component_property = 'value')] #dropdown
)

def update_output(value1,value2):
   return pie_chart2('Unique Beneficiaries with No. of schemes in ',value1,value2)

@app.callback(
     Output(component_id = 'pie_chart6',component_property = 'figure'),
     [Input(component_id = 'my-id1',component_property = 'value'),
      Input(component_id = 'my-id2',component_property = 'value')] #dropdown
)

def update_output(value1,value2):
   return pie_chart3('Households with No. of schemes in ',value1,value2)

@app.callback(
     Output(component_id = 'pie_chart7',component_property = 'figure'),
     [Input(component_id = 'my-id4',component_property = 'value'),
      Input(component_id = 'my-id3',component_property = 'value')] #dropdown
)

def update_output(value3,value4):
   return pie_chart4('Households with No. of schemes in ',value3,value4)

@app.callback(
     Output(component_id = 'pie_chart8',component_property = 'figure'),
     [Input(component_id = 'my-id5',component_property = 'value')] #dropdown
)

def update_output(value2):
   return pie_chart5('Household counts for different benefit amount ranges',value2)

@app.callback(
     Output(component_id = 'pie_chart9',component_property = 'figure'),
     [Input(component_id = 'my-id5',component_property = 'value')] #dropdown
)

def update_output(value2):
   return pie_chart6('Total amount for different benefit amount ranges(household)',value2)

@app.callback(
     Output(component_id = 'pie_chart10',component_property = 'figure'),
     [Input(component_id = 'my-id5',component_property = 'value')] #dropdown
)

def update_output(value2):
   return pie_chart7('Household counts for different benefit amount ranges',value2)

@app.callback(
     Output(component_id = 'pie_chart11',component_property = 'figure'),
     [Input(component_id = 'my-id5',component_property = 'value')] #dropdown
)

def update_output(value2):
   return pie_chart8('Total amount for different benefit amount ranges(beneficiaries)',value2)


if __name__ == '__main__':
    app.run_server()
    
    
 