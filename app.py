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

if page == "About":
    st.title("Sri Lanka Political Violence and Fatalities Analysis Dashboard")
    st.markdown("""
    This dashboard presents an analysis of monthly political **events and fatalities** in **Sri Lanka**.

    ### Purpose
    The goal is to help users explore trends, severity, and distribution of political unrest across time.

    ### Features
    - Interactive timeline visualizations of monthly and cumulative trends
    - Dynamic filters by year, quarter, and event/fatality categories
    - Calendar heatmap showing seasonal patterns
    - Comparative analysis across quarters and years
    - Identification of high-risk periods through alert system
    - Advanced hierarchical visualization of event patterns
    - Export capabilities for further analysis
    """)

    #sample data
    st.subheader("Sample of the Dataset")
    st.dataframe(df.head(), use_container_width=True)

    #key metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Months", df.shape[0])
    col2.metric("Total Events", int(df['Events'].sum()))
    col3.metric("Total Fatalities", int(df['Fatalities'].sum()))

    #summary statistics of the dataset
    st.subheader("Summary Statistics of the dataset")
    stats = df[['Events', 'Fatalities']].describe().loc[['mean', '50%', 'std', 'min', 'max']]
    stats.rename(index={'50%': 'median'}, inplace=True)
    st.dataframe(stats.style.format("{:.2f}"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div style='text-align:center; color:gray;'>Data Science Indiviual Coursework</div>", unsafe_allow_html=True)