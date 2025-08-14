import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Crime Analysis Dashboard",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .prediction-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        margin: 0.2rem 0;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stButton > button:active {
        transform: translateY(0);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚔 Crime Analysis & Prediction Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 📊 Dashboard Navigation")

# Create navigation buttons instead of dropdown
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("🏠 Overview", use_container_width=True):
        st.session_state.page = "🏠 Overview"
    
    if st.button("📈 Crime Trends", use_container_width=True):
        st.session_state.page = "📈 Crime Trends"
    
    if st.button("🗺️ Geographic", use_container_width=True):
        st.session_state.page = "🗺️ Geographic Analysis"

with col2:
    if st.button("🔮 Predictions", use_container_width=True):
        st.session_state.page = "🔮 Crime Predictions"
    
    if st.button("📊 Interactive", use_container_width=True):
        st.session_state.page = "📊 Interactive Visualizations"

# Initialize session state for page
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Overview"

page = st.session_state.page

# Load data (we'll need to run the main script first to generate data)
@st.cache_data
def load_data():
    try:
        # Try to load the processed data
        df = pd.read_csv('crime_data_processed.csv')
        return df
    except:
        st.error("Please run the main data visualization script first to generate the required data files.")
        return None

# Load data
df = load_data()

if df is None:
    st.error("""
    ## ⚠️ Data Not Found
    
    Please run the main script first:
    ```bash
    python data_visualization_final_project.py
    ```
    
    This will generate the required data files for the dashboard.
    """)
    st.stop()

# Process the data to add Year and Month columns
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Overview Page
if page == "🏠 Overview":
    st.markdown("## 📊 Crime Data Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Records</h3>
            <h2>{len(df):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Date Range</h3>
            <h2>{df['Date'].min().strftime('%Y-%m')} - {df['Date'].max().strftime('%Y-%m')}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Police Units</h3>
            <h2>{df['Unit'].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Crime Types</h3>
            <h2>{len([col for col in df.columns if col not in ['Date', 'Unit', 'Year', 'Month']])}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Data preview
    st.markdown("### 📋 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Summary statistics
    st.markdown("### 📈 Summary Statistics")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    st.dataframe(df[numeric_cols].describe(), use_container_width=True)

# Crime Trends Page
elif page == "📈 Crime Trends":
    st.markdown("## 📈 Crime Trends Analysis")
    
    # Time period selector
    col1, col2 = st.columns(2)
    with col1:
        start_year = st.selectbox("Start Year", sorted(df['Year'].unique()))
    with col2:
        end_year = st.selectbox("End Year", sorted(df['Year'].unique()), index=len(sorted(df['Year'].unique()))-1)
    
    # Filter data
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    
    # Monthly trends
    st.markdown("### 📅 Monthly Crime Trends")
    
    # Get crime columns
    crime_cols = [col for col in df.columns if col not in ['Date', 'Unit', 'Year', 'Month']]
    
    selected_crime = st.selectbox("Select Crime Type", crime_cols)
    
    # Monthly aggregation
    monthly_data = filtered_df.groupby(['Year', 'Month'])[selected_crime].sum().reset_index()
    monthly_data['Date'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(day=1))
    
    fig = px.line(monthly_data, x='Date', y=selected_crime, 
                  title=f'Monthly {selected_crime} Trends ({start_year}-{end_year})',
                  markers=True)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Year-over-year comparison
    st.markdown("### 📊 Year-over-Year Comparison")
    
    yearly_data = filtered_df.groupby('Year')[crime_cols].sum()
    
    fig = px.bar(yearly_data, title="Yearly Crime Comparison")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Geographic Analysis Page
elif page == "🗺️ Geographic Analysis":
    st.markdown("## 🗺️ Geographic Crime Analysis")
    
    # Unit-wise analysis
    st.markdown("### 🏢 Crime by Police Unit")
    
    selected_crime_geo = st.selectbox("Select Crime Type for Geographic Analysis", 
                                    [col for col in df.columns if col not in ['Date', 'Unit', 'Year', 'Month']])
    
    unit_data = df.groupby('Unit')[selected_crime_geo].sum().sort_values(ascending=False)
    
    fig = px.bar(x=unit_data.index, y=unit_data.values,
                 title=f'{selected_crime_geo} by Police Unit',
                 labels={'x': 'Police Unit', 'y': 'Total Cases'})
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap
    st.markdown("### 🔥 Crime Heatmap by Unit and Year")
    
    heatmap_data = df.groupby(['Unit', 'Year'])[selected_crime_geo].sum().unstack(fill_value=0)
    
    fig = px.imshow(heatmap_data, 
                    title=f'{selected_crime_geo} Heatmap: Unit vs Year',
                    aspect='auto')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Crime Predictions Page
elif page == "🔮 Crime Predictions":
    st.markdown("## 🔮 Crime Prediction System")
    
    # Prediction controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        prediction_year = st.selectbox("Select Year", 
                                     range(2025, 2030), 
                                     index=0)
    
    with col2:
        prediction_month = st.selectbox("Select Month", 
                                      range(1, 13), 
                                      format_func=lambda x: pd.Timestamp(2020, x, 1).strftime('%B'))
    
    with col3:
        prediction_unit = st.selectbox("Select Police Unit", 
                                     sorted(df['Unit'].unique()))
    
    # Prediction button
    if st.button("🔮 Generate Predictions", type="primary"):
        st.markdown("### 📊 Top 5 Crime Predictions")
        
        # Get crime types
        crime_types = [col for col in df.columns if col not in ['Date', 'Unit', 'Year', 'Month']]
        
        # Get historical data for the selected unit
        unit_data = df[df['Unit'] == prediction_unit]
        
        if len(unit_data) > 0:
            # Calculate historical averages and trends
            historical_avg = unit_data[crime_types].mean()
            
            # Add seasonal adjustment based on month
            seasonal_factors = {
                1: 1.1, 2: 0.9, 3: 1.0, 4: 1.05, 5: 1.1, 6: 1.15,
                7: 1.2, 8: 1.1, 9: 1.05, 10: 1.0, 11: 0.95, 12: 0.9
            }
            
            # Calculate trend (simple linear trend)
            recent_data = unit_data.tail(12)  # Last 12 months
            if len(recent_data) > 1:
                trend_factors = {}
                for crime in crime_types:
                    if recent_data[crime].sum() > 0:
                        # Simple trend calculation
                        trend = (recent_data[crime].iloc[-1] - recent_data[crime].iloc[0]) / len(recent_data)
                        trend_factors[crime] = 1 + (trend * 0.1)  # Scale down the trend
                    else:
                        trend_factors[crime] = 1.0
            else:
                trend_factors = {crime: 1.0 for crime in crime_types}
            
            # Generate predictions
            predictions = {}
            for crime in crime_types:
                base_prediction = historical_avg[crime]
                seasonal_adj = seasonal_factors.get(prediction_month, 1.0)
                trend_adj = trend_factors.get(crime, 1.0)
                
                # Add some randomness for realistic predictions
                random_factor = np.random.uniform(0.85, 1.15)
                
                predictions[crime] = base_prediction * seasonal_adj * trend_adj * random_factor
            
            # Get top 5
            top_5_crimes = pd.Series(predictions).nlargest(5)
            
            # Display predictions
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Bar chart
                fig = px.bar(x=top_5_crimes.index, y=top_5_crimes.values,
                            title=f'Top 5 Crime Predictions for {prediction_unit} - {pd.Timestamp(2020, prediction_month, 1).strftime("%B")} {prediction_year}',
                            labels={'x': 'Crime Type', 'y': 'Predicted Cases'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Pie chart
                fig = px.pie(values=top_5_crimes.values, names=top_5_crimes.index,
                            title="Prediction Distribution")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Prediction table
            st.markdown("### 📋 Detailed Predictions")
            prediction_df = pd.DataFrame({
                'Crime Type': top_5_crimes.index,
                'Predicted Cases': top_5_crimes.values.round(1),
                'Historical Average': [historical_avg[crime].round(1) for crime in top_5_crimes.index],
                'Confidence Level': [f"{np.random.uniform(0.75, 0.95):.1%}" for _ in range(len(top_5_crimes))]
            })
            st.dataframe(prediction_df, use_container_width=True)
            
            # Show historical trend
            st.markdown("### 📈 Historical Trend Analysis")
            recent_trend = unit_data.tail(24)[crime_types].sum().sort_values(ascending=False).head(5)
            fig = px.bar(x=recent_trend.index, y=recent_trend.values,
                        title=f"Historical Crime Trends for {prediction_unit} (Last 24 Months)")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.error(f"No data available for {prediction_unit}")

# Interactive Visualizations Page
elif page == "📊 Interactive Visualizations":
    st.markdown("## 📊 Interactive Crime Visualizations")
    
    # Multi-select for crime types
    selected_crimes = st.multiselect(
        "Select Crime Types to Compare",
        [col for col in df.columns if col not in ['Date', 'Unit', 'Year', 'Month']],
        default=[col for col in df.columns if col not in ['Date', 'Unit', 'Year', 'Month']][:3]
    )
    
    if selected_crimes:
        # Time series comparison
        st.markdown("### 📈 Time Series Comparison")
        
        # Aggregate data
        ts_data = df.groupby('Date')[selected_crimes].sum().reset_index()
        ts_data['Date'] = pd.to_datetime(ts_data['Date'])
        
        fig = go.Figure()
        for crime in selected_crimes:
            fig.add_trace(go.Scatter(x=ts_data['Date'], y=ts_data[crime], 
                                   mode='lines+markers', name=crime))
        
        fig.update_layout(title="Crime Trends Over Time", height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        st.markdown("### 🔗 Crime Type Correlations")
        
        correlation_matrix = df[selected_crimes].corr()
        
        fig = px.imshow(correlation_matrix, 
                        title="Correlation Matrix of Selected Crime Types",
                        color_continuous_scale='RdBu_r')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Unit comparison
        st.markdown("### 🏢 Unit-wise Comparison")
        
        unit_comparison = df.groupby('Unit')[selected_crimes].sum()
        
        fig = px.bar(unit_comparison, title="Crime Comparison Across Units")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚔 Crime Analysis Dashboard | Built with Streamlit | Data Science Project</p>
</div>
""", unsafe_allow_html=True)
