#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import packages
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import folium
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from streamlit_folium import folium_static


# In[3]:


import session_info
session_info.show()


# In[ ]:


pd.set_option("display.max_columns", None)
response = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=7783&compact=true&verbose=false&key=a3b3b3eb-7662-4796-9b6c-c87316c72e84")
print(response.status_code)
df1 = pd.json_normalize(response.json())
df1.head()


# In[ ]:


df1.shape


# In[ ]:


paal = pd.read_csv('laadpaaldata.csv')
paal.head()


# In[ ]:


paal.info()


# In[ ]:





# In[ ]:


paal.describe()


# In[ ]:


paal = paal.drop(paal[paal['ChargeTime'] < 0].index)
paal = paal.drop(paal[paal['ChargeTime'] > 10].index)

data = [paal['ChargeTime']]
group_labels = ['laadtijden']

ann1 = {'x': 8, 'y':0.35, 'showarrow': False, 
                    'font': {'color': 'black'}, 'text': "Gemiddelde laadtijd: 2.43 (2 uur en 26 min)"}
ann2 = {'x': 8, 'y':0.32, 'showarrow': False, 
                    'font': {'color': 'black'}, 'text': "Mediaan van de laadtijd: 2.23 (2 uur en 14 min)"}
#ann3 = {'x': 2, 'y':3800, 'showarrow': False, 
 #                   'font': {'color': 'black'}, 'text': "3700"}

fig = ff.create_distplot(data, group_labels, colors=['green'], bin_size=.2)
fig.update_layout(title = 'Histogram van de laadtijden met een benadering van de kansdichtheidsfunctie.',
                  xaxis_title = 'Laadtijd in uren',
                  yaxis_title = 'Dichtheid')
fig.update_layout({'annotations': [ann1, ann2]})
fig.show()    
st.write(fig)


# In[ ]:


fig, axes = plt.subplots(1, 2, figsize=(15, 5))
fig.suptitle('Initial Pokemon - 1st Generation')

sns.regplot(ax=axes[0],data = paal, y = 'TotalEnergy',x = 'ChargeTime',
            line_kws={"color": "red"})
axes[0].set_title("Zonder transformatie")

paal['sqrt_totalenergy'] = np.sqrt(paal['TotalEnergy'])
paal['sqrt_chargetime'] = np.sqrt(paal['ChargeTime'])

sns.regplot(ax=axes[1],data = paal, y = 'sqrt_totalenergy',x = 'sqrt_chargetime',
            line_kws={"color": "red"})
axes[1].set_title("Met transformatie")
st.write(fig)


# In[ ]:





# In[ ]:





# In[ ]:


locaties = df1[['AddressInfo.ID', 'AddressInfo.Title', 'AddressInfo.AddressLine1', 'AddressInfo.Town',
'AddressInfo.StateOrProvince', 'AddressInfo.Postcode', 'AddressInfo.Latitude', 'AddressInfo.Longitude']]
locaties.head()
#locaties.info()


# In[ ]:


locaties['AddressInfo.Postcode'] = locaties['AddressInfo.Postcode'].astype('string')
locaties['Postcode'] = locaties['AddressInfo.Postcode'].str.extract('(\d+)')
locaties['Postcode'] = locaties['Postcode'].fillna(0).astype(int)
locaties.info()


# In[ ]:


locaties['Provincie'] = locaties['Postcode'].astype('string')
locaties.head()


# In[ ]:


#locaties['Provincie'] = locaties.apply(lambda x: 'Overijssel' if x.Provincie >= 7440 and x.Provincie <= 7739 else x.Provincie, axis=1)

for index, row in locaties.iterrows():
    if row['Postcode'] <= 1299:
        locaties.loc[index,'Provincie'] = 'Noord-Holland'
    elif row['Postcode'] <= 1379:
        locaties.loc[index,'Provincie'] = 'Flevoland'
    elif row['Postcode'] <= 1384:
        locaties.loc[index,'Provincie'] = 'Noord-Holland'
    elif row['Postcode'] <= 1393:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 1394:
        locaties.loc[index,'Provincie'] = 'Noord-Holland'  
    elif row['Postcode'] <= 1396:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 1425:
        locaties.loc[index,'Provincie'] = 'Noord-Holland'
    elif row['Postcode'] <= 1427:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 1429:
        locaties.loc[index,'Provincie'] = 'Zuid-Holland'
    elif row['Postcode'] <= 2158:
        locaties.loc[index,'Provincie'] = 'Noord-Holland'
    elif row['Postcode'] <= 2164:
        locaties.loc[index,'Provincie'] = 'Zuid-Holland'
    elif row['Postcode'] <= 2165:
        locaties.loc[index,'Provincie'] = 'Noord-Holland'
    elif row['Postcode'] <= 3381:
        locaties.loc[index,'Provincie'] = 'Zuid-Holland'
    elif row['Postcode'] <= 3464:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 3466:
        locaties.loc[index,'Provincie'] = 'Zuid-Holland'
    elif row['Postcode'] <= 3769:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 3794:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 3836:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 3888:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 3899:
        locaties.loc[index,'Provincie'] = 'Flevoland'
    elif row['Postcode'] <= 3924:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 3925:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 3999:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 4119:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 4146:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 4162:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 4169:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 4199:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 4209:
        locaties.loc[index,'Provincie'] = 'Zuid-Holland'
    elif row['Postcode'] <= 4212:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 4213:
        locaties.loc[index,'Provincie'] = 'Zuid-Holland'
    elif row['Postcode'] <= 4219:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 4229:
        locaties.loc[index,'Provincie'] = 'Zuid-Holland'
    elif row['Postcode'] <= 4239:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 4241:
        locaties.loc[index,'Provincie'] = 'Zuid-Holland'
    elif row['Postcode'] <= 4249:
        locaties.loc[index,'Provincie'] = 'Utrecht'
    elif row['Postcode'] <= 4299:
        locaties.loc[index,'Provincie'] = 'Noord-Brabant'
    elif row['Postcode'] <= 4599:
        locaties.loc[index,'Provincie'] = 'Zeeland'
    elif row['Postcode'] <= 4671:
        locaties.loc[index,'Provincie'] = 'Noord-Brabant'
    elif row['Postcode'] <= 4679:
        locaties.loc[index,'Provincie'] = 'Zeeland'
    elif row['Postcode'] <= 4681:
        locaties.loc[index,'Provincie'] = 'Noord-Brabant'
    elif row['Postcode'] <= 4699:
        locaties.loc[index,'Provincie'] = 'Zeeland'
    elif row['Postcode'] <= 5299:
        locaties.loc[index,'Provincie'] = 'Noord-Brabant'
    elif row['Postcode'] <= 5335:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 5765:
        locaties.loc[index,'Provincie'] = 'Noord-Brabant'
    elif row['Postcode'] <= 5817:
        locaties.loc[index,'Provincie'] = 'Limburg'
    elif row['Postcode'] <= 5846:
        locaties.loc[index,'Provincie'] = 'Noord-Brabant'
    elif row['Postcode'] <= 6019:
        locaties.loc[index,'Provincie'] = 'Limburg'
    elif row['Postcode'] <= 6029:
        locaties.loc[index,'Provincie'] = 'Noord-Brabant'
    elif row['Postcode'] <= 6499:
        locaties.loc[index,'Provincie'] = 'Limburg'
    elif row['Postcode'] <= 6583:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 6599:
        locaties.loc[index,'Provincie'] = 'Limburg'
    elif row['Postcode'] <= 7399:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 7438:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 7439:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 7739:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 7766:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 7799:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 7949:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 7955:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 7999:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 8049:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 8054:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 8069:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 8099:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 8159:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 8195:
        locaties.loc[index,'Provincie'] = 'Gelderland'
    elif row['Postcode'] <= 8199:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 8259:
        locaties.loc[index,'Provincie'] = 'Flevoland'
    elif row['Postcode'] <= 8299:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 8322:
        locaties.loc[index,'Provincie'] = 'Flevoland'
    elif row['Postcode'] <= 8349:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 8354:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 8379:
        locaties.loc[index,'Provincie'] = 'Overijssel'
    elif row['Postcode'] <= 8387:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9299:
        locaties.loc[index,'Provincie'] = 'Friesland'
    elif row['Postcode'] <= 9349:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9399:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9478:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9479:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9499:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9509:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9539:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9563:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9564:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9569:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9579:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9653:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9659:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9748:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9749:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9759:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9769:
        locaties.loc[index,'Provincie'] = 'Drenthe'
    elif row['Postcode'] <= 9849:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9859:
        locaties.loc[index,'Provincie'] = 'Friesland'
    elif row['Postcode'] <= 9869:
        locaties.loc[index,'Provincie'] = 'Groningen'
    elif row['Postcode'] <= 9879:
        locaties.loc[index,'Provincie'] = 'Friesland'
    elif row['Postcode'] <= 9999:
        locaties.loc[index,'Provincie'] = 'Groningen'
    else :
        locaties.loc[index,'Provincie'] = 'Onbekend'


# In[ ]:


locaties.info()


# In[ ]:


locaties.Provincie.value_counts()


# In[ ]:


def color_producer(type):
    if type == 'Gelderland':
        return 'blue'
    if type == 'Zuid-Holland':
        return 'green'
    if type == 'Limburg':
        return 'orange'
    if type == 'Overijssel':
        return 'red'
    if type == 'Noord-Brabant':
        return 'darkviolet'
    if type == 'Utrecht':
        return 'lawngreen'
    if type == 'Drenthe':
        return 'cyan'
    if type == 'Noord-Holland':
        return 'saddlebrown'
    if type == 'Zeeland':
        return 'forestgreen'
    if type == 'Groningen':
        return 'royalblue'
    if type == 'Friesland':
        return 'magenta'
    if type == 'Flevoland':
        return 'gold'
    if type == 'Onbekend':
        return 'gray'
    


# In[ ]:


search = locaties.loc[locaties['Provincie'].str.contains("Onbekend", case=False)]
search


# In[ ]:


def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


# In[ ]:


m = folium.Map(location=[52.373726, 4.893975], zoom_start=8)

for index, row in locaties.iterrows():
    folium.vector_layers.Circle(location = [row['AddressInfo.Latitude'], row['AddressInfo.Longitude']],
                                popup = (row['AddressInfo.AddressLine1'],row['AddressInfo.Town']),
                                radius = 1, color = color_producer(row['Provincie']),
                                fill = True).add_to(m)

m = add_categorical_legend(m, 'Provincie',
                            labels = ['Gelderland', 'Zuid-Holland', 'Limburg', 'Overijssel', 'Noord-Braband', 'Utrecht',
                                      'Drenthe', 'Noord-Holland', 'Zeeland', 'Groningen', 'Friesland', 'Flevoland'],
                            colors = ['blue', 'green', 'orange', 'red', 'darkviolet', 'lawngreen', 'cyan', 'saddlebrown',
                                      'forestgreen', 'royalblue', 'magenta', 'gold'])
    

folium_static(m)


# In[ ]:


rdw = pd.DataFrame(pd.read_csv("RDW_Merged.csv"))
rdw.head()


# In[ ]:


rdw["Datum"] = pd.to_datetime(rdw.Jaar.astype(str) + '/' + rdw.Maand.astype(str) + '/01')

rdw['Waarde'] = 1


# In[ ]:


autos_per_maand = pd.DataFrame(rdw.groupby(['Datum','Brandstof'])['Waarde'].sum())
autos_per_maand_cum = pd.DataFrame(autos_per_maand.groupby('Brandstof')['Waarde'].cumsum())
autos_per_maand_cum.reset_index(drop=False, inplace=True)


# In[ ]:


fig = px.line(autos_per_maand_cum, x='Datum', y='Waarde',
                   color = 'Brandstof',
                   title= 'Lijndiagram',
                   )
fig.update_yaxes(title_text='Aantal')
fig.update_layout(title_text="cumulatieve lijndiagram aantal autos per maand per brandstof categorie", title_x=0.5)
fig.update_xaxes(rangeslider_visible=True)
fig.show()
st.write(fig)

