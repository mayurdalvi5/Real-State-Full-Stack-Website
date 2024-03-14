import streamlit as st
import pickle
import numpy as np
import pandas as pd
import sklearn

st.set_page_config(page_title = "viz Demo")

with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)
# pipeline = pickle.load(open('pipeline.pkl', 'rb'))

# st.dataframe(df)

st.header("Enter your Input")

# property type
property_type = st.selectbox('Property Type',['flat', 'house'])

# sector
sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

# Bedroom
bedroom = float(st.selectbox('Number of Bedroom', sorted(df['bedRoom'].unique().tolist())))

# Bathroom
bathroom = float(st.selectbox('Number of Bathroom',sorted(df['bathroom'].unique().tolist())))

# Balcony
balcony = (st.selectbox('Balconies', sorted(df['balcony'].unique().tolist())))

# propery age
property_age = (st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist())))

# Build up area
build_up_area = float(st.number_input("Built Up Area"))

# Servent Room
servant_room = float(st.selectbox('Servant Room ', [0.0, 1.0]))

# Store Room
store_room = float(st.selectbox( 'Store Room ', [0.0, 1.0]))


# Furnishing Type
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

# Luxury Category
luxury_category = (st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist())))

# Floor Category
floor_category = (st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist())))


if st.button("Predict"):

    # form a dataframe
    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, build_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    # st.dataframe(one_df)

    #predict
    base_price = np.expm1(pipeline.predict(one_df)[0])
    low = base_price - 0.22
    high = base_price + 0.22

    # display
    st.text("The price of the {} is between {} Cr and {} Cr ".format(property_type,round(low, 2),round(high, 2)))