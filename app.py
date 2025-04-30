import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar

st.set_page_config(
    page_title="Sri Lanka Events and Fatalities Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv")
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'] + '-01')
    df['Month_Year'] = df['Month'] + ' ' + df['Year'].astype(str)
    return df

df = load_data()

#sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["About", "Dashboard"])
