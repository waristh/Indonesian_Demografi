#!/usr/bin/env python
# coding: utf-8

# In[1]:


# from google.colab import drive
# drive.mount('/content/gdrive')


# In[2]:


# cd /content/gdrive/MyDrive/Test_Data_Analyst/


# In[3]:


# !pip install geojson
# # !pip install plotly==4.13.0
# !pip install dash==1.19.0
# !pip install dash-core-components==1.3.1
# !pip install dash-html-components==1.0.1
# !pip install dash-renderer==1.1.2
# !pip install flask==1.1.2
# !pip install geopandas==0.8.1
# !pip install jupyter_dash
# !pip install dash_bootstrap_components


# In[ ]:





# In[ ]:





# In[4]:


import pandas as pd
import geojson
with open('kabkota.geojson') as f:
    gj = geojson.load(f)
indo_kabkota_geojson = gj
# indo_kabkota_geojson["features"]


# In[ ]:





# In[5]:


# indo_kabkota = pd.io.json.json_normalize(indo_kabkota_geojson['features'])
# # indo_kabkota = indo_kabkota[['properties.ID_0','properties.NAME_0','properties.ID_1','properties.NAME_1','properties.ID_2','properties.NAME_2']]
# indo_kabkota


# In[ ]:





# In[6]:


df = pd.read_excel('Data_Bersih_id.xlsx')
df


# In[7]:


# a = df[['Kota_Kabupaten']]
# a.to_excel('a.xlsx',index=False)
# b = indo_kabkota[['properties.NAME_2','properties.ID_2']]
# b.to_excel('b.xlsx',index=False)


# In[8]:


import plotly.express as px


# In[9]:


# fig=px.choropleth(df,
#                   geojson=indo_kabkota_geojson,
#                   featureidkey="properties.ID_2",   
#                   locations='id',        #column in dataframe
#                   color='Indeks_Pembangunan_Manusia',  #dataframe
# #                   color_continuous_scale='Inferno',
#                   color_continuous_scale=px.colors.diverging.Tealrose,
#                   # color_continuous_scale=px.colors.qualitative.Light24,
#                   # color_continuous_midpoint=2,
#                   # projection='orthographic',
#                   hover_name='Kota_Kabupaten',
#                   hover_data=["Area"],
#                   # title='Jumlah Penduduk Kabupaten' ,  
#                   # height=700
#                   )
# fig.update_geos(fitbounds="locations", visible=False)
# # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

# fig = px.bar(df, x='Kota_Kabupaten', y='Jumlah_Penduduk', 
#              color='Kota_Kabupaten', width=1200)
# fig.show()


# In[10]:


# # import plotly.graph_objects as go
# # token = "pk.eyJ1Ijoid2FyaXN0cmloYXJtb2tvIiwiYSI6ImNrcnEwNXhpbzBjM2ozMW44dXJpOXJ2bnoifQ.2LLK5iQUwXY6nXocSQb9sA"

# fig = px.choropleth_mapbox(df, 
#                            geojson=indo_kabkota_geojson, 
#                            color="Area",
#                            locations="id", 
#                            featureidkey="properties.ID_2",
#                            center={"lat": 0.7893, "lon":113.9213 },
#                            mapbox_style="carto-positron", zoom=3)
# fig.update_geos(fitbounds="locations", visible=True)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


# In[11]:


px.scatter(df,x='PDRB',y='PDRB_Per_Kapita',color='Provinsi',template='seaborn')


# In[12]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc

# geojson = indo_kabkota_geojson
option = ['PDRB',
       'PDRB_Per_Kapita', 'Indeks_Pembangunan_Manusia', 'Jumlah_Penduduk',
       'Luas_Wilayah', 'Dana_Alokasi_Umum',
       'Pengeluaran_Riil_per_Kapita_ per_Tahun', 'Nilai_UMR',
       'Jumlah_Penduduk_Miskin', 'Jumlah_Penduduk_Bekerja',
       'Pengguna_Internet', 'Pemilik_Ponsel', 'Pengguna_Ponsel',
       'Jumlah_Kelurahan', 'Jumlah_Desa', 'Kepadatan_Penduduk',
       ]
lokasi = ['Area','Provinsi','Kota_Kabupaten','Regional']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = JupyterDash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
###########################################################################################################
#Setting Layout awal dashboard
app.layout = html.Div([
    html.H1(children="DEMOGRAFI PENDUDUK INDONESIA",style={'text-align': 'center'}),

    dcc.Dropdown(id="pilihan",
                 options=[{'value': x, 'label': x} 
                          for x in option],
                 value=option[0],                  
                 multi=False,
                 style={'width': "80%"}
                 ),
    
    dcc.Graph(id="choropleth",figure={}),
    html.Br(),
    
    dcc.RadioItems(
        id='lokasi', 
        options=[{'value': x, 'label': x} 
                 for x in lokasi],
        value='Area',
        labelStyle={'display': 'inline-block'}
    ),
    
#     html.Br(),    
    dcc.Graph(id="bar-chart",figure={}),
    html.Br(),
])

#################################################################################################
#Membuat callback  input & outputnya
@app.callback(
    Output('choropleth', 'figure'),
    [Input('pilihan', 'value')],
)

#Display Map Sesuai Pilihan
def display_choropleth(pilihan):
    # Plotly Express
    fig = px.choropleth(
        data_frame=df,
        geojson=indo_kabkota_geojson,
        featureidkey="properties.ID_2",
        locations='id',
        color=pilihan,
        hover_name='Kota_Kabupaten',
#         hover_data=[option],
#         color_continuous_scale=px.colors.diverging.Tealrose,
        labels={'Demografi Jumlah Penduduk Indonesia'},
        template='seaborn',
#         height=700,
#         width = 1800,
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

# def draw_choropleth(pilihan):
#     fig = px.choropleth_mapbox(df, 
#                             geojson=indo_kabkota_geojson, 
#                             color=pilihan,
#                             locations="id", 
#                             featureidkey="properties.ID_2",
#                             center={"lat": 0.7893, "lon":113.9213 },                               
#                             color_continuous_scale="Viridis",
#                             #range_color=(0, 12),
#                             mapbox_style="carto-positron",
#                             zoom=4, 
#                             opacity=0.5,
#                             )
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
#                         height=700,
#                         )
#     return fig

@app.callback(
     Output('bar-chart', 'figure'),
    [Input('lokasi', 'value'),Input('pilihan', 'value')],
)
#Display Bar Chart Sesuai Pilihan & lokasi
def update_bar_chart(lokasi,pilihan):
    fig = px.bar(df.sort_values(by=pilihan,ascending=False), x=lokasi, y=pilihan, 
                 color=lokasi,
                 hover_data=[pilihan,'Kota_Kabupaten'],
                 template='ggplot2',
#                  width=1800,
                 height=800,
                )

    return fig

##################################################################################################

#Running Web Server
if __name__ == '__main__':
#     app.run_server(debug=True, use_reloader=False)
    app.run_server(mode='inline')


# In[ ]:





# In[ ]:





# In[ ]:




