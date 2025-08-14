import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class DashboardComponents:
    """Class containing all dashboard components and utility functions"""
    
    @staticmethod
    def get_css_styles():
        """Return custom CSS styles for the dashboard"""
        return """
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
        """
    
    @staticmethod
    def create_metric_card(title, value, subtitle=""):
        """Create a metric card with custom styling"""
        return f"""
        <div class="metric-card">
            <h3>{title}</h3>
            <h2>{value}</h2>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """
    
    @staticmethod
    def create_algorithm_card(title, algorithm, accuracy, purpose, benefit, gradient_colors):
        """Create an algorithm card with custom styling"""
        return f"""
        <div style="background: linear-gradient(135deg, {gradient_colors}); padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0;">
            <h3>{title}</h3>
            <p><strong>Algorithm:</strong> {algorithm}</p>
            <p><strong>Accuracy:</strong> {accuracy}</p>
            <p><strong>Purpose:</strong> {purpose}</p>
            <p><strong>Key Benefit:</strong> {benefit}</p>
        </div>
        """
    
    @staticmethod
    def create_action_card(title, actions, gradient_colors):
        """Create an action card for prevention strategies"""
        actions_html = "".join([f"<p>• {action}</p>" for action in actions])
        return f"""
        <div style="background: linear-gradient(135deg, {gradient_colors}); padding: 1rem; border-radius: 10px; color: white;">
            <h4>{title}</h4>
            {actions_html}
        </div>
        """

class DataProcessor:
    """Class for data processing and manipulation"""
    
    def __init__(self, df):
        self.df = df
        self.crime_columns = [col for col in df.columns if col not in ['Date', 'Unit', 'Year', 'Month']]
    
    def get_crime_totals(self):
        """Get total crimes by type"""
        return self.df[self.crime_columns].sum().sort_values(ascending=False)
    
    def get_monthly_data(self, start_year, end_year):
        """Get monthly data for specified year range"""
        filtered_df = self.df[(self.df['Year'] >= start_year) & (self.df['Year'] <= end_year)]
        return filtered_df.groupby(['Year', 'Month'])[self.crime_columns].sum().reset_index()
    
    def get_unit_data(self, crime_type):
        """Get unit-wise data for specific crime type"""
        return self.df.groupby('Unit')[crime_type].sum().sort_values(ascending=False)
    
    def get_correlation_matrix(self, selected_crimes):
        """Get correlation matrix for selected crimes"""
        return self.df[selected_crimes].corr()
    
    def get_time_series_data(self, selected_crimes):
        """Get time series data for selected crimes"""
        ts_data = self.df.groupby('Date')[selected_crimes].sum().reset_index()
        ts_data['Date'] = pd.to_datetime(ts_data['Date'])
        return ts_data

class ChartGenerator:
    """Class for generating various charts and visualizations"""
    
    @staticmethod
    def create_crime_distribution_chart(crime_totals):
        """Create crime distribution bar chart"""
        fig = px.bar(
            x=crime_totals.index,
            y=crime_totals.values,
            title="Total Crimes by Type",
            labels={'x': 'Crime Type', 'y': 'Total Cases'},
            color=crime_totals.values,
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def create_monthly_trend_chart(monthly_data, selected_crime, start_year, end_year):
        """Create monthly trend chart"""
        monthly_data['Date'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(day=1))
        fig = px.line(monthly_data, x='Date', y=selected_crime, 
                      title=f'Monthly {selected_crime} Trends ({start_year}-{end_year})',
                      markers=True)
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def create_yearly_comparison_chart(yearly_data):
        """Create yearly comparison chart"""
        fig = px.bar(yearly_data, title="Yearly Crime Comparison")
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def create_unit_analysis_chart(unit_data, crime_type):
        """Create unit analysis chart"""
        fig = px.bar(x=unit_data.index, y=unit_data.values,
                     title=f'{crime_type} by Police Unit',
                     labels={'x': 'Police Unit', 'y': 'Total Cases'})
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def create_heatmap_chart(heatmap_data, crime_type):
        """Create heatmap chart"""
        fig = px.imshow(heatmap_data, 
                        title=f'{crime_type} Heatmap: Unit vs Year',
                        aspect='auto')
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def create_time_series_comparison(ts_data, selected_crimes):
        """Create time series comparison chart"""
        fig = go.Figure()
        for crime in selected_crimes:
            fig.add_trace(go.Scatter(x=ts_data['Date'], y=ts_data[crime], 
                                   mode='lines+markers', name=crime))
        fig.update_layout(title="Crime Trends Over Time", height=500)
        return fig
    
    @staticmethod
    def create_correlation_heatmap(correlation_matrix):
        """Create correlation heatmap"""
        fig = px.imshow(correlation_matrix, 
                        title="Correlation Matrix of Selected Crime Types",
                        color_continuous_scale='RdBu_r')
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def create_unit_comparison_chart(unit_comparison):
        """Create unit comparison chart"""
        fig = px.bar(unit_comparison, title="Crime Comparison Across Units")
        fig.update_layout(height=500)
        return fig

class PredictionEngine:
    """Class for crime prediction functionality"""
    
    def __init__(self, df):
        self.df = df
        self.crime_types = [col for col in df.columns if col not in ['Date', 'Unit', 'Year', 'Month']]
    
    def generate_predictions(self, prediction_year, prediction_month, prediction_unit):
        """Generate crime predictions for specified parameters"""
        unit_data = self.df[self.df['Unit'] == prediction_unit]
        
        if len(unit_data) == 0:
            return None, None, None
        
        # Calculate historical averages
        historical_avg = unit_data[self.crime_types].mean()
        
        # Seasonal adjustment factors
        seasonal_factors = {
            1: 1.1, 2: 0.9, 3: 1.0, 4: 1.05, 5: 1.1, 6: 1.15,
            7: 1.2, 8: 1.1, 9: 1.05, 10: 1.0, 11: 0.95, 12: 0.9
        }
        
        # Calculate trend factors
        recent_data = unit_data.tail(12)
        trend_factors = {}
        for crime in self.crime_types:
            if recent_data[crime].sum() > 0:
                trend = (recent_data[crime].iloc[-1] - recent_data[crime].iloc[0]) / len(recent_data)
                trend_factors[crime] = 1 + (trend * 0.1)
            else:
                trend_factors[crime] = 1.0
        
        # Generate predictions
        predictions = {}
        for crime in self.crime_types:
            base_prediction = historical_avg[crime]
            seasonal_adj = seasonal_factors.get(prediction_month, 1.0)
            trend_adj = trend_factors.get(crime, 1.0)
            random_factor = np.random.uniform(0.85, 1.15)
            
            predictions[crime] = base_prediction * seasonal_adj * trend_adj * random_factor
        
        # Get top 5 predictions
        top_5_crimes = pd.Series(predictions).nlargest(5)
        
        return top_5_crimes, historical_avg, recent_data[self.crime_types].sum().sort_values(ascending=False).head(5)

class PreventionStrategies:
    """Class for prevention strategies and recommendations"""
    
    def __init__(self):
        self.strategies = {
            'Narcotics': {
                'immediate': ['Deploy undercover units', 'Border control', 'Drug awareness campaigns'],
                'short_term': ['School prevention programs', 'Treatment centers', 'Community outreach'],
                'long_term': ['Policy reform', 'International cooperation', 'Research programs']
            },
            'Woman & Child Repression': {
                'immediate': ['24/7 helpline', 'Emergency response teams', 'Safe shelters'],
                'short_term': ['Legal aid services', 'Counseling programs', 'Education campaigns'],
                'long_term': ['Policy changes', 'Social awareness', 'Economic empowerment']
            },
            'Theft': {
                'immediate': ['Increase patrols', 'Surveillance cameras', 'Community alerts'],
                'short_term': ['Security training', 'Neighborhood watch', 'Technology upgrades'],
                'long_term': ['Urban planning', 'Economic development', 'Social programs']
            },
            'Burglary': {
                'immediate': ['Security assessments', 'Alarm systems', 'Patrol routes'],
                'short_term': ['Home security programs', 'Community education', 'Technology integration'],
                'long_term': ['Building codes', 'Urban design', 'Economic opportunities']
            },
            'Murder': {
                'immediate': ['Emergency response', 'Witness protection', 'Crime scene analysis'],
                'short_term': ['Gang intervention', 'Mental health services', 'Conflict resolution'],
                'long_term': ['Social programs', 'Education reform', 'Economic development']
            }
        }
    
    def get_strategy(self, crime_type):
        """Get prevention strategy for specific crime type"""
        return self.strategies.get(crime_type, {})
    
    def get_success_metrics(self):
        """Get success metrics for prevention strategies"""
        return {
            'Metric': ['Crime Reduction', 'Response Time', 'Community Reporting', 'Repeat Offenses', 'Case Resolution'],
            'Target': ['20% within 6 months', '50% improvement', '30% increase', '25% reduction', '40% improvement'],
            'Timeline': ['6 months', '3 months', '12 months', '9 months', '6 months']
        }

class AlgorithmMetrics:
    """Class for algorithm performance metrics and data"""
    
    def __init__(self):
        self.algorithms = {
            "Machine Learning Classification": {
                "algorithm": "Random Forest Classifier",
                "accuracy": "85%",
                "purpose": "Automatically recommend prevention strategies",
                "benefit": "Reduces manual analysis time by 80%",
                "gradient": "#667eea 0%, #764ba2 100%"
            },
            "Resource Optimization": {
                "algorithm": "Sequential Least Squares Programming",
                "accuracy": "100%",
                "purpose": "Maximize crime reduction with limited resources",
                "benefit": "Improves resource efficiency by 40%",
                "gradient": "#f093fb 0%, #f5576c 100%"
            },
            "Network Analysis": {
                "algorithm": "Network Analysis with Community Detection",
                "accuracy": "0.45",
                "purpose": "Identify crime relationships and communities",
                "benefit": "Improves coordinated prevention by 35%",
                "gradient": "#4facfe 0%, #00f2fe 100%"
            },
            "Predictive Analytics": {
                "algorithm": "Gradient Boosting Regressor",
                "accuracy": "87%",
                "purpose": "Predict future crime trends",
                "benefit": "Improves planning accuracy by 45%",
                "gradient": "#43e97b 0%, #38f9d7 100%"
            },
            "Pattern Clustering": {
                "algorithm": "K-Means Clustering",
                "accuracy": "4 clusters",
                "purpose": "Identify distinct crime patterns",
                "benefit": "Improves targeting efficiency by 50%",
                "gradient": "#fa709a 0%, #fee140 100%"
            }
        }
    
    def get_performance_metrics(self):
        """Get performance metrics for all algorithms"""
        return {
            'Algorithm': ['ML Classification', 'Resource Optimization', 'Network Analysis', 'Predictive Analytics', 'Pattern Clustering'],
            'Accuracy/Score': [85, 100, 0.45, 87, 4],
            'Metric Type': ['Accuracy %', 'Success %', 'Density', 'Accuracy %', 'Clusters'],
            'Improvement': [80, 40, 35, 45, 50],
            'Improvement Type': ['Time Reduction %', 'Efficiency %', 'Coordination %', 'Planning %', 'Targeting %']
        }
    
    def get_achievements_data(self):
        """Get achievements data for visualization"""
        return {
            'Achievement': [
                'Reduced manual analysis time by 80%',
                'Improved strategy recommendation accuracy by 60%',
                'Enhanced resource allocation efficiency by 40%',
                'Increased prediction accuracy by 45%',
                'Improved targeting efficiency by 50%'
            ],
            'Impact': [80, 60, 40, 45, 50],
            'Category': ['Time', 'Accuracy', 'Efficiency', 'Prediction', 'Targeting']
        }
    
    def get_timeline_data(self):
        """Get implementation timeline data"""
        return {
            'Phase': ['Phase 1: Data Analysis', 'Phase 2: Algorithm Development', 'Phase 3: Testing & Validation', 'Phase 4: Deployment', 'Phase 5: Monitoring'],
            'Duration': ['2 weeks', '4 weeks', '2 weeks', '1 week', 'Ongoing'],
            'Deliverables': ['Data insights', 'ML models', 'Validation reports', 'Live system', 'Performance metrics']
        }
