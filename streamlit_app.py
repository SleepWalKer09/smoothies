# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie.""")

title = st.text_input('Name on Smoothie: ')
st.write('The name on your smoothie whill be: ',title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections = 5)

if ingredient_list:
    ingredients_string = ''
    name_on_order = title
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (name_on_order, ingredients)
        VALUES ('{name_on_order}', '{ingredients_string}')
    """
    
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
