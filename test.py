import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

os.chdir(r"C:\Users\LENOVO\PycharmProjects\data_mu\datasets")
df = pd.read_csv("by_constituency_2016_2022.csv", encoding = "ISO-8859-1")

print(df)