import streamlit as sl
import pandas as pd
import requests as rq
import snowflake.connector
from urllib.error import URLError

#Fruityvice Functions
def get_fruityvice_data(fruit_name):
  fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_name)
  fruityvice_normalised = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalised

#Snowflake Functions
#my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT FRUIT_NAME FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('Test');")
    return new_fruit + ' added.  Thanks.'

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
  if not fruit_choice:
    sl.error("Please enter a fruit to get information")
  else:
    sl.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  sl.error()
#sl.write('User entered ', fruit_choice)

if sl.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  sl.header("The Fruit Load list contains:")
  sl.dataframe(my_data_rows)

extra_fruit = sl.text_input('Add another fruit?')
if sl.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
  sl.write(insert_row_snowflake(extra_fruit))

sl.stop()

#my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('Test');")
