import streamlit as sl
import pandas as pd
import requests as rq
import snowflake.connector
from urllib.error import URLError

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
try:
  fruit_choice = sl.text_input('What fruit would you like more information about?')
  if not fruit_chioce:
    sl.error("Please enter a fruit to get information")
  else:
    fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalised = pd.json_normalize(fruityvice_response.json())
    sl.dataframe(fruityvice_normalised)
except URLError as e:
  sl.error()
sl.write('User entered ', fruit_choice)

sl.stop()

my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT FRUIT_NAME FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
sl.header("The Fruit Load list contains:")
sl.dataframe(my_data_rows)

extra_fruit = sl.text_input('Add another fruit?')
sl.write(extra_fruit, ' added.  Thanks.')

my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('Test');")
