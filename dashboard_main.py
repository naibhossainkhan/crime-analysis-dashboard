import streamlit as st
import pandas as pd
from dashboard_components import DashboardComponents
from dashboard_pages import (
    OverviewPage, CrimeTrendsPage, GeographicPage, PredictionsPage, 
    InteractivePage, AdvancedAlgorithmsPage, PreventionStrategiesPage, 
    BenefitsAchievementsPage
)

class CrimeAnalysisDashboard:
    """Main dashboard class that orchestrates all components and pages"""
    
    def __init__(self):
        """Initialize the dashboard"""
        self.components = DashboardComponents()
        self.df = None
        self.pages = {}
        self.setup_page_config()
        self.load_data()
        self.initialize_pages()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="Crime Analysis Dashboard",
            page_icon="🚔",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply custom CSS
        st.markdown(self.components.get_css_styles(), unsafe_allow_html=True)
        
        # Main header
        st.markdown('<h1 class="main-header">🚔 Crime Analysis & Prediction Dashboard</h1>', unsafe_allow_html=True)
    
    @staticmethod
    @st.cache_data
    def _load_data():
        """Load and cache the crime data"""
        try:
            df = pd.read_csv('crime_data_processed.csv')
            df['Date'] = pd.to_datetime(df['Date'])
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    
    def load_data(self):
        """Load data and handle errors"""
        self.df = CrimeAnalysisDashboard._load_data()
        
        if self.df is None:
            st.error("""
            ## ⚠️ Data Not Found
            
            Please ensure 'crime_data_processed.csv' exists in the current directory.
            """)
            st.stop()
    
    def initialize_pages(self):
        """Initialize all page objects"""
        if self.df is not None:
            self.pages = {
                "🏠 Overview": OverviewPage(self.df),
                "📈 Crime Trends": CrimeTrendsPage(self.df),
                "🗺️ Geographic Analysis": GeographicPage(self.df),
                "🔮 Crime Predictions": PredictionsPage(self.df),
                "📊 Interactive Visualizations": InteractivePage(self.df),
                "🤖 Advanced Algorithms": AdvancedAlgorithmsPage(),
                "🛡️ Prevention Strategies": PreventionStrategiesPage(self.df),
                "🎯 Benefits & Achievements": BenefitsAchievementsPage()
            }
    
    def create_sidebar(self):
        """Create the sidebar navigation"""
        st.sidebar.markdown("## 📊 Dashboard Navigation")
        
        # Create navigation buttons
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
        
        # Advanced Algorithms Section
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 🤖 Advanced Algorithms")
        
        col3, col4 = st.sidebar.columns(2)
        
        with col3:
            if st.button("🤖 ML Algorithms", use_container_width=True):
                st.session_state.page = "🤖 Advanced Algorithms"
            
            if st.button("🎯 Prevention", use_container_width=True):
                st.session_state.page = "🛡️ Prevention Strategies"
        
        with col4:
            if st.button("📊 Benefits", use_container_width=True):
                st.session_state.page = "🎯 Benefits & Achievements"
    
    def get_current_page(self):
        """Get the current page from session state"""
        if 'page' not in st.session_state:
            st.session_state.page = "🏠 Overview"
        return st.session_state.page
    
    def render_current_page(self):
        """Render the current page"""
        current_page = self.get_current_page()
        
        if current_page in self.pages:
            try:
                self.pages[current_page].render()
            except Exception as e:
                st.error(f"Error rendering {current_page}: {e}")
                st.info("Please try refreshing the page or contact support.")
        else:
            st.error(f"Page '{current_page}' not found.")
    
    def render_footer(self):
        """Render the dashboard footer"""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🚔 Crime Analysis Dashboard | Built with Streamlit | Data Science Project</p>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Main method to run the dashboard"""
        try:
            # Create sidebar
            self.create_sidebar()
            
            # Render current page
            self.render_current_page()
            
            # Render footer
            self.render_footer()
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Please check the console for more details.")

def main():
    """Main function to run the dashboard"""
    dashboard = CrimeAnalysisDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
