import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar

st.set_page_config(
    page_title="Sri Lanka Political Violence and Fatalities Analysis Dashboard",
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

#background image
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                        url("https://images.unsplash.com/photo-1634749044918-b94ad51d8567?q=80&w=1470&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-blend-mode: multiply;
        }
        .about-content {
            background-color: rgba(20, 20, 20, 0.9) !important;
            color: white !important;
            border-left: 5px solid #e63946;
        }
        /* Force all text white */
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Sri Lanka Political Violence and Fatalities Analysis Dashboard")
    st.markdown("""
    This dashboard presents an analysis of monthly political **events and fatalities** in **Sri Lanka**.

    ### Purpose
    The goal is to help users explore trends, severity, and distribution of political unrest across time.

    ### Features
    - Time series and cumulative visualizations of events and fatalities
    - Interactive filters by year range, specific years, quarter, and severity categories
    - Calendar heatmap to identify monthly activity patterns
    - Quarterly and categorical comparisons with bar and pie charts
    - Outlier detection and identification of top months by events and fatalities
    - Event-Fatality correlation and risk matrix
    - Threshold-based alert system for high-risk periods
    - Hierarchical view of events by Year > Quarter > Month
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
    st.markdown("<div style='text-align:center; color:gray; font-size:12px;'>Data Science Indiviual Coursework</div>", unsafe_allow_html=True)

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

    st.title("Sri Lanka Political Violence and Fatalities Analysis Dashboard")
    st.markdown(f"Data from **{filtered_df['Date'].min().strftime('%B %Y')}** to **{filtered_df['Date'].max().strftime('%B %Y')}**")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Events", int(filtered_df['Events'].sum()))
    col2.metric("Total Fatalities", int(filtered_df['Fatalities'].sum()))
    col3.metric("Avg Events/Month", round(filtered_df['Events'].mean(), 1))
    col4.metric("Avg Fatalities/Month", round(filtered_df['Fatalities'].mean(), 1))

#tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trends", "Categories", "Calendar", "Deep Dive", "Advanced"])


#trends tab 
    with tab1:
        st.subheader("Events and Fatalities Over Time")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Events'], name="Events", line=dict(color='blue')), secondary_y=False)
        fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Fatalities'], name="Fatalities", line=dict(color='red')), secondary_y=True)
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Events",
            yaxis2_title="Fatalities",
            hovermode="x unified",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Cumulative Events and Fatalities")
        fig_cum = px.area(
            filtered_df,
            x='Date',
            y=['Cumulative_Events', 'Cumulative_Fatalities'],
            labels={'value': 'Count', 'variable': 'Metric'},
        )
        st.plotly_chart(fig_cum, use_container_width=True)


#categories tab
    with tab2:
        st.subheader("Event and Fatality Categories")
        col1, col2 = st.columns(2)

        with col1:
            pie_events = px.pie(
                filtered_df.groupby('Events_Category')['Events'].sum().reset_index(),
                values='Events', names='Events_Category', title="Events by Category"
            )
            st.plotly_chart(pie_events, use_container_width=True)

        with col2:
            pie_fatalities = px.pie(
                filtered_df.groupby('Fatalities_Category')['Fatalities'].sum().reset_index(),
                values='Fatalities', names='Fatalities_Category', title="Fatalities by Category"
            )
            st.plotly_chart(pie_fatalities, use_container_width=True)

        st.subheader("Quarterly Breakdown")
        quarterly_df = filtered_df.groupby(['Year', 'Quarter']).agg({
            'Events': ['sum', 'mean'],
            'Fatalities': ['sum', 'mean']
        }).reset_index()
        quarterly_df.columns = ['Year', 'Quarter', 'Total_Events', 'Avg_Events', 'Total_Fatalities', 'Avg_Fatalities']

        fig_q1 = px.bar(
            quarterly_df, x='Year', y='Total_Events', color='Quarter', barmode='group',
            title="Total Events by Quarter"
        )
        st.plotly_chart(fig_q1, use_container_width=True)

        fig_q2 = px.bar(
            quarterly_df, x='Year', y='Total_Fatalities', color='Quarter', barmode='group',
            title="Total Fatalities by Quarter"
        )
        st.plotly_chart(fig_q2, use_container_width=True)

        fig_q3 = px.bar(
            quarterly_df, x='Year', y='Avg_Events', color='Quarter', barmode='group',
            title="Average Events per Quarter"
        )
        st.plotly_chart(fig_q3, use_container_width=True)

        fig_q4 = px.bar(
            quarterly_df, x='Year', y='Avg_Fatalities', color='Quarter', barmode='group',
            title="Average Fatalities per Quarter"
        )
        st.plotly_chart(fig_q4, use_container_width=True)


#calendar view tab
    with tab3:
        st.subheader("Monthly Events Heatmap")

        month_order = list(calendar.month_name)[1:]
        month_abbr = list(calendar.month_abbr)[1:]

        heatmap_data = filtered_df.pivot_table(
            index='Month',
            columns='Year', 
            values='Events',
            aggfunc='sum'
        ).fillna(0)

        heatmap_data = heatmap_data.reindex(month_order)

        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Year", y="Month", color="Events"),
            x=heatmap_data.columns.tolist(),
            y=[m[:3] for m in heatmap_data.index],
            aspect="auto",
            color_continuous_scale='YlOrRd'
        )
        fig.update_xaxes(side="top")
        fig.update_yaxes(tickvals=list(range(12)), ticktext=month_abbr)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Fatal vs Non-Fatal Months")
        fatal_counts = filtered_df['Is_Fatal'].value_counts().reset_index()
        fatal_counts.columns = ['Is_Fatal', 'Count']
        fig_bar = px.bar(
            fatal_counts, x='Is_Fatal', y='Count', color='Is_Fatal',
            labels={'Is_Fatal': 'Had Fatalities'},
        )
        st.plotly_chart(fig_bar, use_container_width=True)


#deep dive tab
    with tab4:
        st.subheader("Average Events by Month")
        avg_monthly = filtered_df.groupby('Month')['Events'].mean().reset_index()
        
        month_order = list(calendar.month_name)[1:]
        avg_monthly['Month'] = pd.Categorical(avg_monthly['Month'], categories=month_order, ordered=True)
        avg_monthly = avg_monthly.sort_values('Month')

        fig_bar_month = px.bar(
            avg_monthly,
            x='Month', y='Events',
            title="Average Monthly Events",
            labels={'Events': 'Average Events'}
        )
        st.plotly_chart(fig_bar_month, use_container_width=True)

        st.subheader("Top 5 Months by Events and Fatalities")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Top 5 by Events**")
            top_events = filtered_df.nlargest(5, 'Events')[['Month_Year', 'Events']]
            st.dataframe(top_events.set_index('Month_Year'), height=200)

        with col2:
            st.markdown("**Top 5 by Fatalities**")
            top_fatalities = filtered_df.nlargest(5, 'Fatalities')[['Month_Year', 'Fatalities']]
            st.dataframe(top_fatalities.set_index('Month_Year'), height=200)


#advanced analytics tab
    with tab5:
        st.subheader("Advanced Visualizations")
        
        st.markdown("#### Events vs Fatalities Correlation")
        fig_scatter = px.scatter(
            filtered_df,
            x="Events", y="Fatalities",
            trendline="lowess",
            hover_name="Month_Year",
            color="Quarter",
            size="Fatalities"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("#### Risk Matrix")
        risk_df = filtered_df.groupby(['Events_Category','Fatalities_Category']).size().reset_index(name='Counts')
        fig_risk = px.scatter(
            risk_df,
            x="Events_Category",
            y="Fatalities_Category",
            size="Counts",
            color="Counts",
            title="Event Frequency vs Severity"
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        
        st.markdown("#### Alert System")
        col1, col2 = st.columns(2)
        with col1:
            event_threshold = st.slider("Event threshold for alerts:", 0, 100, 30)
        with col2:
            fatal_threshold = st.slider("Fatality threshold for alerts:", 0, 100, 10)
        
        alerts = filtered_df[
            (filtered_df['Events'] > event_threshold) | 
            (filtered_df['Fatalities'] > fatal_threshold)
        ]
        
        if not alerts.empty:
            st.warning(f" {len(alerts)} alert(s) triggered!")
            st.dataframe(alerts[['Month_Year', 'Events', 'Fatalities']].sort_values('Events', ascending=False))
        else:
            st.success("No alerts triggered for current thresholds")
        
        st.markdown("#### Hierarchical View")
        if not filtered_df.empty:
            try:
                hierarchy_df = filtered_df.groupby(['Year', 'Quarter', 'Month']).agg({
                    'Events': 'sum',
                    'Fatalities': 'mean'
                }).reset_index()
                
                hierarchy_df['Events_Adjusted'] = hierarchy_df['Events'] + 0.1
                
                fig_hierarchy = px.treemap(
                    hierarchy_df,
                    path=['Year', 'Quarter', 'Month'],
                    values='Events_Adjusted',
                    color='Fatalities',
                    title="Events Hierarchy (Size=Events, Color=Fatalities)",
                    color_continuous_scale='RdYlBu_r',
                    height=700
                )
                fig_hierarchy.update_traces(
                    textinfo="label+value",
                    textfont=dict(size=14),
                    hovertemplate='<b>%{label}</b><br>Events: %{value:.0f}<br>Avg Fatalities: %{color:.2f}',
                    textposition="middle center",
                    insidetextfont=dict(size=12)
                )
                fig_hierarchy.update_layout(
                    margin=dict(l=10, r=10, b=10, t=50),
                    uniformtext=dict(minsize=10, mode='hide')
                )
                st.plotly_chart(fig_hierarchy, use_container_width=True)
                
            except Exception as e:
                st.error("Could not generate hierarchical view with current data filters.")
                st.info("Try adjusting your filters to include more data.")
        else:
            st.warning("No data available for the selected filters to display hierarchy.")

    st.markdown("---")
    st.markdown("<div style='text-align:center; color:gray; font-size:12px;'>Data Science Individual Coursework</div>", unsafe_allow_html=True)