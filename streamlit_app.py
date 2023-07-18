import streamlit as sl
import pandas as pd
import requests as rq
import snowflake.connector

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

sl.title('My Parents New Healthy Diner')
sl.header('Breakfast Menu')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinich & Rocket Smoothie')
sl.text('🐔 Hard Boiled Free-Rnage Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

sl.dataframe(fruits_to_show)

sl.header('Fruityvice Fruit Advice')
fruit_choice = sl.text_input('What fruit would you like more information about?', 'Kiwi')
sl.write('User entered ', fruit_choice)

fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#sl.text(fruityvice_response.json())

fruityvice_normalised = pd.json_normalize(fruityvice_response.json())
sl.dataframe(fruityvice_normalised)

my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT FRUIT_NAME FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
sl.header("The Fruit Load list contains:")
sl.dataframe(my_data_rows)

#extra_fruit_list = my_data_rows.set_index('FRUIT_NAME')
extra_fruit = sl.multiselect('Add another fruit?', list(my_data_rows))
sl.write(extra_fruit, ' selected')
