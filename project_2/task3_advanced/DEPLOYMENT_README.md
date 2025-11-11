# 🏥 Health Assistant Pro - Medical Prediction System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered healthcare application combining disease prediction and cancer diagnosis using machine learning. Built for **SC4020 Data Mining Task 3**.

## 🎯 Features

### Disease Prediction System
- **130+ Symptoms** database
- **40+ Disease** predictions  
- Real-time confidence scoring
- Symptom-based intelligent matching
- Precautionary measures for each disease
- Description and background information

### Cancer Diagnosis System
- **Breast Cancer Classification** (Benign/Malignant)
- **30-feature** tumor analysis
- **96%+ accuracy** with Gradient Boosting
- Risk level assessment
- Probability distributions
- Sample data loading for testing

### Web Application
- Modern, responsive React UI
- Real-time API integration
- Interactive symptom selection
- Multi-tab interface
- Mobile-friendly design
- Comprehensive about section

## 📊 Project Structure

```
SC4020_Task3/
├── app.py                          # Flask REST API server (MAIN)
├── train-models-script.py          # ML model training script
├── requirements.txt                # Python dependencies
├── dataset_cleaned.csv             # Disease-symptom dataset
├── Cancer_Data.csv                 # Wisconsin breast cancer dataset
├── symptom_Description.csv         # Disease descriptions
├── symptom_precaution.csv          # Precautionary measures
├── Symptom-severity.csv            # Symptom severity weights
├── test-api-script.py              # API testing script
├── Dockerfile                      # Backend Docker configuration
├── docker-compose.yml              # Multi-container orchestration
├── setup.sh / setup.bat            # Automated setup scripts
├── start.sh / start.bat            # Quick start scripts
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── .dockerignore                   # Docker ignore rules
├── frontend/                       # React frontend application
│   ├── package.json               # Node.js dependencies
│   ├── Dockerfile                 # Frontend Docker configuration
│   ├── nginx.conf                 # Nginx configuration
│   ├── public/
│   │   └── index.html            # HTML entry point
│   └── src/
│       ├── index.js              # React entry point
│       ├── index.css             # Global styles
│       └── App.js                # Main React component
└── models/                        # ML models directory (generated)
    ├── disease_model.pkl
    ├── disease_label_encoder.pkl
    ├── symptom_list.pkl
    ├── cancer_model.pkl
    ├── cancer_scaler.pkl
    └── cancer_features.pkl
```

## 🚀 Quick Start

### Method 1: Automated Setup (Recommended)

#### Windows
```powershell
# Run setup script
setup.bat

# Start the application
start.bat
```

#### Linux/Mac
```bash
# Make scripts executable
chmod +x setup.sh start.sh

# Run setup script
./setup.sh

# Start the application
./start.sh
```

### Method 2: Manual Setup

#### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Node.js 18+ (optional, for frontend)
- Git

#### Backend Setup

1. **Clone or navigate to the repository**
   ```bash
   cd SC4020_Task3
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Linux/Mac)
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train ML models**
   ```bash
   python train-models-script.py
   ```
   This will create models in the `models/` directory.

5. **Start the Flask server**
   ```bash
   python app.py
   ```
   
   Server will start at: `http://localhost:5000`

#### Frontend Setup (Optional)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```
   
   Frontend will open at: `http://localhost:3000`

### Method 3: Docker Deployment

#### Prerequisites
- Docker
- Docker Compose

#### Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the application:**
- Backend API: `http://localhost:5000`
- Frontend UI: `http://localhost:3000` (if using frontend container)

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "disease_model": true,
  "cancer_model": true
}
```

#### 2. Get All Symptoms
```http
GET /api/symptoms
```
**Response:**
```json
{
  "symptoms": ["fever", "cough", "headache", ...],
  "count": 131
}
```

#### 3. Predict Disease
```http
POST /api/predict-disease
Content-Type: application/json

{
  "symptoms": ["fever", "cough", "headache", "fatigue"]
}
```
**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "disease": "Common Cold",
      "confidence": 85.5,
      "description": "A viral infection of your nose and throat...",
      "precautions": ["Drink vitamin C rich drinks", "Take vapour", ...]
    },
    ...
  ],
  "symptoms_provided": 4
}
```

#### 4. Predict Cancer
```http
POST /api/predict-cancer
Content-Type: application/json

{
  "features": [17.99, 10.38, 122.8, ..., 0.1189]  # 30 values
}
```
**Response:**
```json
{
  "success": true,
  "diagnosis": "Malignant",
  "confidence": 97.5,
  "risk_level": "High",
  "probabilities": {
    "benign": 2.5,
    "malignant": 97.5
  }
}
```

#### 5. Get Disease Information
```http
GET /api/disease-info/<disease_name>
```
**Example:** `/api/disease-info/Common Cold`

**Response:**
```json
{
  "success": true,
  "disease": "Common Cold",
  "info": {
    "description": "...",
    "precautions": ["...", "..."]
  }
}
```

#### 6. Calculate Severity Score
```http
POST /api/severity-score
Content-Type: application/json

{
  "symptoms": ["high_fever", "chest_pain", "breathlessness"]
}
```
**Response:**
```json
{
  "success": true,
  "total_score": 18,
  "average_score": 6.0,
  "severity_level": "Severe",
  "symptom_scores": [
    {"symptom": "high_fever", "severity": 7},
    {"symptom": "chest_pain", "severity": 7},
    {"symptom": "breathlessness", "severity": 4}
  ]
}
```

#### 7. Batch Prediction
```http
POST /api/batch-predict
Content-Type: application/json

{
  "symptom_sets": [
    ["fever", "cough"],
    ["headache", "dizziness"],
    ["chest_pain", "breathlessness"]
  ]
}
```

## 🧪 Testing

### Run API Tests
```bash
# Install test dependencies (if not already installed)
pip install colorama requests

# Run comprehensive tests
python test-api-script.py
```

The test script will:
- Test all API endpoints
- Validate responses
- Display colored output
- Generate test report

### Manual Testing

#### Test Disease Prediction
```bash
curl -X POST http://localhost:5000/api/predict-disease \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "cough", "headache"]}'
```

#### Test Cancer Prediction
```bash
curl -X POST http://localhost:5000/api/predict-cancer \
  -H "Content-Type: application/json" \
  -d '{"features": [17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}'
```

## 🤖 Machine Learning Models

### Disease Prediction Model
- **Algorithm:** Random Forest Classifier
- **Features:** 130+ symptoms (binary encoding)
- **Classes:** 40+ diseases
- **Accuracy:** ~92% (training), ~90% (cross-validation)
- **Training Time:** ~30 seconds
- **File:** `models/disease_model.pkl`

### Cancer Diagnosis Model
- **Algorithm:** Gradient Boosting Classifier
- **Features:** 30 tumor measurements (standardized)
- **Classes:** Benign (0) / Malignant (1)
- **Accuracy:** ~98% (training), ~96% (testing)
- **Training Time:** ~10 seconds
- **File:** `models/cancer_model.pkl`

## 📦 Dependencies

### Backend (Python)
```
Flask==2.3.3
flask-cors==4.0.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

### Frontend (Node.js)
```
react==18.2.0
react-dom==18.2.0
react-scripts==5.0.1
lucide-react==0.294.0
axios==1.6.2
```

## 🐛 Troubleshooting

### Issue: Models not found
**Solution:**
```bash
python train-models-script.py
```

### Issue: Port 5000 already in use
**Solution:**
```bash
# Find process using port
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -ti:5000

# Kill the process or change port in app.py
```

### Issue: CORS errors in frontend
**Solution:**
- Ensure backend is running
- Check `CORS` configuration in `app.py`
- Verify API_URL in frontend `.env`

### Issue: Module not found
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or for frontend
cd frontend && npm install
```

### Issue: Training fails
**Solution:**
- Ensure all CSV files are present
- Check CSV file format and encoding
- Verify sufficient disk space for models

## 🌐 Deployment

### Production Deployment Checklist

- [ ] Set `FLASK_ENV=production` in environment
- [ ] Use `gunicorn` for WSGI server
- [ ] Enable HTTPS (use reverse proxy like Nginx)
- [ ] Set up proper CORS origins
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up backups for models
- [ ] Use containerization (Docker)

### Deploy to Cloud

#### Heroku
```bash
# Add Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create health-assistant
git push heroku main
```

#### AWS/Azure/GCP
Use Docker containers with the provided Dockerfile and docker-compose.yml

## ⚠️ Important Disclaimer

**This application is for educational purposes only.**

- **NOT for actual medical diagnosis**
- **NOT a replacement for professional medical advice**
- **Should NOT be used in clinical settings**
- **Always consult qualified healthcare providers**

This is a demonstration project for data mining and machine learning in healthcare. The predictions are based on limited datasets and should not be used for real medical decisions.

## 📊 Project Context

### SC4020 Task 3 Requirements
This project fulfills Task 3 requirements:
- ✅ Uses insights from Task 1 (Symptom Co-occurrence) 
- ✅ Uses insights from Task 2 (Cancer Feature Sequences)
- ✅ Working healthcare application
- ✅ Justified and documented approach
- ✅ Reproducible results
- ✅ Clear evaluation/demonstration

### Datasets Used
1. **Disease-Symptom Dataset** (dataset_cleaned.csv)
   - 300+ disease-symptom combinations
   - 40+ unique diseases
   - 130+ unique symptoms

2. **Wisconsin Breast Cancer Dataset** (Cancer_Data.csv)
   - 569 tumor samples
   - 30 numerical features
   - Binary classification (Malignant/Benign)

3. **Supporting Datasets**
   - symptom_Description.csv
   - symptom_precaution.csv
   - Symptom-severity.csv

## 🤝 Contributing

This is an educational project. Contributions for learning purposes are welcome:

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

MIT License - See LICENSE file for details

## 👥 Authors

- **SC4020 Task 3 Project**
- Educational demonstration of healthcare data mining

## 🙏 Acknowledgments

- UCI Machine Learning Repository
- Wisconsin Breast Cancer Dataset
- Open-source community
- scikit-learn team
- Flask & React communities

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the API documentation
3. Run the test script for diagnostics
4. Check logs for error messages

## 🔄 Version History

### Version 1.0.0 (Current)
- Initial release
- Disease prediction system
- Cancer diagnosis system
- Web UI
- REST API
- Docker support
- Comprehensive documentation

---

**Made with ❤️ for healthcare education and ML learning**

🏥 **Health Assistant Pro** - Bringing AI to Healthcare Education
