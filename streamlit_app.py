import streamlit as sl
import pandas as pn

my_fruit_list = pn.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

sl.title('My Parents New Healthy Diner')
sl.header('Breakfast Menu')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinich & Rocket Smoothie')
sl.text('🐔 Hard Boiled Free-Rnage Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

streamlit.dataframe(my_fruit_list)
