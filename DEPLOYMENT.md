# 🚀 Deployment Guide

This guide provides step-by-step instructions for deploying your Crime Analysis Dashboard to various platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ All project files committed to a Git repository
- ✅ `requirements.txt` file with all dependencies
- ✅ `streamlit_dashboard.py` as your main application file
- ✅ Data files (`crime_data_processed.csv`, `crime_data_original.csv`)

## 🌐 Option 1: Streamlit Cloud (Recommended)

**Best for**: Quick deployment, free hosting, automatic updates

### Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Fill in the details:
     - **Repository**: `your-username/your-repo-name`
     - **Branch**: `main`
     - **Main file path**: `streamlit_dashboard.py`
   - Click "Deploy"

3. **Your app will be live at**: `https://your-app-name.streamlit.app`

### Advantages:
- ✅ Completely free
- ✅ Automatic deployments from GitHub
- ✅ No server management
- ✅ Built-in analytics
- ✅ Custom domains available

---

## 🐳 Option 2: Docker + Any Cloud Platform

**Best for**: Full control, custom configurations, enterprise use

### Steps:

1. **Build Docker Image**
   ```bash
   docker build -t crime-dashboard .
   ```

2. **Test Locally**
   ```bash
   docker run -p 8501:8501 crime-dashboard
   ```

3. **Deploy to Your Preferred Platform**

#### Google Cloud Run:
```bash
# Tag for Google Container Registry
docker tag crime-dashboard gcr.io/YOUR_PROJECT_ID/crime-dashboard

# Push to GCR
docker push gcr.io/YOUR_PROJECT_ID/crime-dashboard

# Deploy to Cloud Run
gcloud run deploy crime-dashboard \
  --image gcr.io/YOUR_PROJECT_ID/crime-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### AWS ECS:
```bash
# Create ECR repository
aws ecr create-repository --repository-name crime-dashboard

# Tag and push
docker tag crime-dashboard YOUR_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/crime-dashboard
aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com
docker push YOUR_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/crime-dashboard
```

#### Azure Container Instances:
```bash
# Build and push to Azure Container Registry
az acr build --registry YOUR_REGISTRY_NAME --image crime-dashboard .

# Deploy
az container create \
  --resource-group YOUR_RESOURCE_GROUP \
  --name crime-dashboard \
  --image YOUR_REGISTRY_NAME.azurecr.io/crime-dashboard \
  --ports 8501 \
  --dns-name-label crime-dashboard
```

---

## ☁️ Option 3: Heroku

**Best for**: Simple deployment, good for small to medium apps

### Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-crime-dashboard
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Open the App**
   ```bash
   heroku open
   ```

### Note:
- Heroku requires a credit card for verification (even for free tier)
- Free tier is being discontinued, consider paid plans

---

## 🚂 Option 4: Railway

**Best for**: Simple deployment, good alternative to Heroku

### Steps:

1. **Go to Railway**
   - Visit [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect it's a Python app

3. **Configure**
   - Set the start command: `streamlit run streamlit_dashboard.py --server.port=$PORT --server.address=0.0.0.0`
   - Add environment variables if needed

---

## 🔧 Option 5: VPS/Cloud Server

**Best for**: Full control, custom domain, specific requirements

### Steps:

1. **Set up a VPS** (DigitalOcean, Linode, AWS EC2, etc.)

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **Clone and Setup**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/crime-dashboard.service
   ```
   
   Add this content:
   ```ini
   [Unit]
   Description=Crime Dashboard
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/your-repo
   Environment="PATH=/home/ubuntu/your-repo/venv/bin"
   ExecStart=/home/ubuntu/your-repo/venv/bin/streamlit run streamlit_dashboard.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start the Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable crime-dashboard
   sudo systemctl start crime-dashboard
   ```

6. **Configure Nginx** (optional, for custom domain)
   ```bash
   sudo nano /etc/nginx/sites-available/crime-dashboard
   ```
   
   Add this content:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

---

## 🔍 Troubleshooting

### Common Issues:

1. **Port Issues**
   - Ensure the port is correctly set in your deployment configuration
   - Check if the port is available and not blocked by firewall

2. **Dependencies**
   - Verify all packages in `requirements.txt` are compatible
   - Some packages might need system dependencies

3. **Data Files**
   - Ensure data files are included in your repository
   - Check file paths in your code

4. **Memory Issues**
   - Streamlit apps can be memory-intensive
   - Consider upgrading your deployment plan if needed

### Performance Tips:

1. **Optimize Data Loading**
   - Use `@st.cache_data` for expensive operations
   - Load only necessary data

2. **Reduce Package Size**
   - Remove unused dependencies
   - Use lighter alternatives where possible

3. **Monitor Usage**
   - Keep track of resource usage
   - Optimize based on actual usage patterns

---

## 📞 Support

If you encounter issues:
1. Check the platform's documentation
2. Review error logs
3. Test locally first
4. Contact platform support if needed

## 🎉 Success!

Once deployed, your dashboard will be accessible via a public URL and can be shared with others!
