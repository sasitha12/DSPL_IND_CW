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

#about page
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

#dashboard page
else:
    st.sidebar.header("Filter Data")

    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())

    year_range = st.sidebar.slider(
        "Select Year Range", min_value=min_year, max_value=max_year,
        value=(min_year, max_year)
    )

    selected_years = st.sidebar.multiselect(
        "Select Specific Year(s)",
        options=sorted(df['Year'].unique()),
        default=sorted(df['Year'].unique())
    )

    quarters = st.sidebar.multiselect("Select Quarter(s)",
        options=sorted(df['Quarter'].unique()),
        default=sorted(df['Quarter'].unique())
    )

    event_categories = st.sidebar.multiselect("Event Categories",
        options=sorted(df['Events_Category'].unique()),
        default=sorted(df['Events_Category'].unique())
    )

    fatality_categories = st.sidebar.multiselect("Fatality Categories",
        options=sorted(df['Fatalities_Category'].unique()),
        default=sorted(df['Fatalities_Category'].unique())
    )

    filtered_df = df[
        (df['Year'] >= year_range[0]) &
        (df['Year'] <= year_range[1]) &
        (df['Year'].isin(selected_years)) &
        (df['Quarter'].isin(quarters)) &
        (df['Events_Category'].isin(event_categories)) &
        (df['Fatalities_Category'].isin(fatality_categories))
    ]