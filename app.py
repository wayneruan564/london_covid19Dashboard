# Source: https://data.london.gov.uk/dataset/coronavirus--covid-19--cases

from londonData import *

from dash import *
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'style.css']
)

app.layout = dbc.Alert(
    "Hello, Bootstrap!", className="m-5"
)


#weekly covid cases mapped onto a geographic map.
geo_weeklycases = px.choropleth(df_merged1,
                    geojson=df_merged1.geometry,
                    locations=df_merged1.index,
                    color=df_merged1.columns[-1],
                    projection="mercator",
                    title="Weekly Covid19 Cases Per 100,000 People in London Boroughs")

geo_weeklycases.update_geos(fitbounds="locations", visible=False)

#shows line chart of past covid cases.
dailyCases = px.line(df_grouped, x=x, y=y, title="Daily Covid19 Case in London")

#bar graph displaying daily covid case in the past 14 days.
lastTwoWeeks = px.bar(df_lastTwoWeeks, x=x1, y=y1, title='Covid Cases in the last 14 days')

#heatmap of weekly cases in London by borough.
weekly_heatmap = px.imshow(weekly_case, text_auto=False, title='Weekly Covid Case in London per 100,000 people, by Borough')

#pie chart showing age distribution of recent week's covid hospital cases.
pieChart = px.pie(hospitalAdmissionRecent, values='weekly_admissions', names='age', title='Covid19 Hospital Admissions, by Age')


#font-style, color for the graphs.
fontStyle = 'courier'
backgroundColor = '#23262F'
textColor = 'white'


#remove color in the graph background.
lastTwoWeeks.update_layout(plot_bgcolor = backgroundColor,
                  paper_bgcolor= backgroundColor,
                  title = {'x':0.5}, 
                  font = {"family" : fontStyle, "color": textColor})

dailyCases.update_layout(plot_bgcolor = backgroundColor,
                  paper_bgcolor= backgroundColor,
                  title = {'x':0.5}, 
                  font = {"family" : fontStyle, "color": textColor})

weekly_heatmap.update_layout(plot_bgcolor = backgroundColor,
                  paper_bgcolor= backgroundColor,
                  title = {'x':0.5}, 
                  font = {"family" : fontStyle, "color": textColor})

pieChart.update_layout(plot_bgcolor = backgroundColor,
                  paper_bgcolor= backgroundColor,
                  title = {'x':0.5}, 
                  font = {"family" : fontStyle, "color": textColor})

geo_weeklycases.update_layout(plot_bgcolor = backgroundColor,
                  paper_bgcolor= backgroundColor,
                  geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                  title = {'x':0.5}, 
                  font = {"family" : fontStyle, "color": textColor})


#hide the gridlines.
lastTwoWeeks.update_yaxes(showgrid=False)
dailyCases.update_yaxes(showgrid=False)
dailyCases.update_xaxes(showgrid=False)




df_daily_grouped = df_daily.groupby(by=['date']).sum()


#retrieves latest information from our data and store them to variables.
currentDate = ''
total_case = df_daily_grouped['new_cases'].sum()
total_death = df_daily_grouped['new_deaths'].sum()
new_case = df_daily_grouped['new_cases'].iloc[-1]
new_case_previous = df_daily_grouped['new_cases'].iloc[-2]
new_death = df_daily_grouped['new_deaths'].iloc[-1]
new_death_previous = df_daily_grouped['new_deaths'].iloc[-2]
pop = population['ONS'].sum()



app.layout = dbc.Container([
    html.Div(children=[html.H1(id='Title', children='London Covid19 Tracker'),   
                      html.Div(id='subheading', style={}, children='''
                        Tracking the impact of covid on london healthcare
                    ''') ], style={'text-align':'center'}),

   dbc.Row([
    
    dbc.Col([
        #total cases
        dbc.Row(
            html.Div(className="info-container", style={}, children=[html.Div(className="info-header", children='''Total Cases: '''), 
                                                              html.Div(className="info case-count", children=str(total_case))
                                                             ])),
        
        #total deaths
        dbc.Row(
             html.Div(className="info-container", style={}, children=[html.Div(className="info-header", children='''Total Death: '''), 
                                                              html.Div(className="info death-count", children=str(total_death))
                                                              ])),
        
        #today's new cases.
        dbc.Row(
             html.Div(className="info-container", style={}, children=[html.Div(className="info-header", children='''New Cases on ''' + str(df_grouped.index[-1]) + ''': '''), 
                                                              html.Div(className="info case-count", children=str(new_case)),
                                                              html.Div(className="info-change", style={}, children='''Change in Daily Case: '''+ str(new_case - new_case_previous)), 
                                                              ])),
        
        #today's new cases.
        dbc.Row(
             html.Div(className="info-container", style={}, children=[html.Div(className="info-header", children='''New Deaths on ''' + str(df_grouped.index[-1]) + ''': '''), 
                                                               html.Div(className="info death-count", children=str(new_death)),
                                                              html.Div(className="info-change", style={}, children='''Change in Daily Death: '''+ str(new_death - new_death_previous)),
                                                              ])),

        
        dbc.Row([
            dbc.Row(dcc.Graph(id='last-14-daily-case', figure=lastTwoWeeks)),

            dbc.Row(dcc.Graph(id='weekly-hospital-case-age', figure=pieChart)),

            dbc.Row(
                html.Div(
                className='time', children='''Last updated : Week Ending ''' + str(hospitalAdmissionRecent.iloc[0]['week_ending']))
            ),
            ]
            ),  

        ],
        md=4
        ),
    
      dbc.Col([
            dbc.Row(dcc.Graph(id="daily-case", figure=dailyCases)),
            dbc.Row(dcc.Graph(id="weekly-covid-case-per-100000", figure=geo_weeklycases)),
            dbc.Row(dcc.Graph(id='heatmap-weekly-case-borough', figure=weekly_heatmap)),
            ],
            style={'text-align':'center'}, 
            md=8
            ),  
       
   ])
    
])

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
