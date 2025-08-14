# 🚔 Crime Analysis & Prediction Dashboard

A comprehensive data visualization and crime prediction dashboard built with Streamlit, featuring interactive visualizations and machine learning-powered predictions.

## 📊 Features

- **Interactive Crime Trends Analysis** - Explore crime patterns over time
- **Geographic Crime Distribution** - Visualize crime by police units
- **Machine Learning Predictions** - Get top 5 crime predictions for any future date
- **Modern UI/UX** - Professional dashboard with gradient styling
- **Real-time Data Processing** - Dynamic data loading and analysis

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
1. Clone the repository:
```bash
git clone <your-repo-url>
cd crime-analysis-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the main script to generate data:
```bash
python data_visualization_final_project.py
```

5. Start the dashboard:
```bash
streamlit run streamlit_dashboard.py
```

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended)

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and main file (`streamlit_dashboard.py`)
6. Click "Deploy"

**Advantages:**
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ Easy setup
- ✅ No server management

### 2. Heroku

**Steps:**
1. Create a `Procfile`:
```
web: streamlit run streamlit_dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. Deploy to Heroku:
```bash
heroku create your-app-name
git add .
git commit -m "Initial deployment"
git push heroku main
```

### 3. Railway

**Steps:**
1. Connect your GitHub repository to Railway
2. Set environment variables if needed
3. Deploy automatically

### 4. Google Cloud Platform

**Steps:**
1. Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Deploy to Google Cloud Run:
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/crime-dashboard
gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/crime-dashboard --platform managed
```

## 📁 Project Structure

```
crime-analysis-dashboard/
├── streamlit_dashboard.py      # Main dashboard application
├── data_visualization_final_project.py  # Data processing and ML models
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── crime_data_processed.csv   # Processed crime data
├── crime_data_original.csv    # Original crime data
└── venv/                      # Virtual environment
```

## 🔧 Configuration

### Environment Variables
- `STREAMLIT_SERVER_PORT`: Port for the Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

### Customization
- Modify `streamlit_dashboard.py` to change dashboard layout
- Update CSS in the dashboard for custom styling
- Add new visualizations in the appropriate sections

## 📈 Usage

1. **Overview**: View key metrics and data summary
2. **Crime Trends**: Analyze crime patterns over time
3. **Geographic Analysis**: Explore crime distribution by location
4. **Predictions**: Generate crime predictions for future dates
5. **Interactive Visualizations**: Compare multiple crime types

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- Plotly for interactive visualizations
- Pandas for data manipulation
- Scikit-learn for machine learning capabilities

## 📞 Support

For support, please open an issue on GitHub or contact the development team.
