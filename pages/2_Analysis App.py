import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn


st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

new_df = pd.read_csv('Datasets/data_viz1.csv')
feature_text = pickle.load(open('feature_text.pkl', 'rb'))

numeric_columns = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
group_df = new_df.groupby('sector')[numeric_columns].mean()

# Geo Map
st.header('Geo Map')
fig = px.scatter_mapbox(group_df, lat='latitude', lon='longitude',
                        color='price_per_sqft', size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        zoom=10, mapbox_style='open-street-map',
                        width=1200, height=700,
                        hover_name=group_df.index)

st.plotly_chart(fig, use_container_width=True)

# plotting for wordcloud
st.header("WordCloud")
wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      stopwords={'s'},
                      min_font_size=10).generate(feature_text)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

# plotting Scatter plot Area VS Price

st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat', 'house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x='built_up_area', y="price",
                      color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x='built_up_area', y='price',
                      title='Area Vs Price')

    st.plotly_chart(fig1, use_container_width=True)

# BHK piechart

st.header("BHK Pie Chart")

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df.query('sector == @selected_sector'), names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)

# Side by Side Boxplot bedroom price

st.header('Side by Side BHK price Comparision')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')
st.plotly_chart(fig3, use_container_width=True)

# Distribution plot of prices and houses

st.header("Side by Side Distribution plot for property type")

fig4 = plt.figure(figsize=(10,4))
sns.distplot(new_df[new_df['property_type']== 'house']['price'])
sns.distplot(new_df[new_df['property_type']== 'flat']['price'])
st.pyplot(fig4)