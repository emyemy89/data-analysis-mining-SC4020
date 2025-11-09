# 🏥 Health Assistant - AI-Powered Disease Prediction System

A comprehensive medical diagnosis system using Machine Learning to predict diseases based on symptoms and diagnose cancer from tumor measurements.

## 📋 Features

### Disease Prediction
- **130+ Symptoms** database
- **40+ Disease** predictions
- Real-time symptom-based analysis
- Confidence scoring
- Disease descriptions & precautions
- Severity assessment

### Cancer Diagnosis
- Breast cancer classification (Benign/Malignant)
- 30-feature tumor analysis
- Probability scoring
- Risk level assessment
- Based on Wisconsin Breast Cancer Dataset

### Technology Stack
- **Backend**: Flask, Python 3.9+
- **Frontend**: React 18, Tailwind CSS
- **ML Models**: 
  - Random Forest Classifier (Disease Prediction)
  - Gradient Boosting Classifier (Cancer Diagnosis)
- **API**: RESTful API with CORS support
- **Deployment**: Docker, Docker Compose

---

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.9+
- Node.js 18+
- Docker (optional)
```

### Option 1: Local Setup

#### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd health-assistant
```

#### 2. Setup Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Train ML models (first time only)
python train_models.py

# Run Flask API server
python app.py
```

Backend will run on `http://localhost:5000`

#### 3. Setup Frontend

```bash
# Create React app (if not exists)
npx create-react-app frontend
cd frontend

# Install dependencies
npm install lucide-react

# Copy App.jsx to src/App.jsx
# Update API_BASE_URL if needed

# Start React app
npm start
```

Frontend will run on `http://localhost:3000`

---

### Option 2: Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access application
# Backend: http://localhost:5000
# Frontend: http://localhost:3000
```

---

## 📁 Project Structure

```
health-assistant/
├── app.py                          # Flask API server
├── train_models.py                 # ML model training script
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose setup
├── README.md                       # This file
│
├── models/                         # Trained ML models (generated)
│   ├── disease_model.pkl
│   ├── disease_label_encoder.pkl
│   ├── symptom_list.pkl
│   ├── cancer_model.pkl
│   ├── cancer_scaler.pkl
│   └── *.json                      # Model metadata
│
├── dataset_cleaned.csv             # Disease-symptom dataset
├── Cancer_Data.csv                 # Cancer diagnosis dataset
├── symptom_Description.csv         # Disease descriptions
├── symptom_precaution.csv          # Safety precautions
├── Symptom-severity.csv            # Symptom severity weights
│
└── frontend/                       # React application
    ├── public/
    ├── src/
    │   ├── App.jsx                 # Main React component
    │   └── index.js
    └── package.json
```

---

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### Get All Symptoms
```
GET /api/symptoms

Response:
{
  "symptoms": ["fever", "cough", ...],
  "count": 130
}
```

### Predict Disease
```
POST /api/predict-disease

Request Body:
{
  "symptoms": ["fever", "cough", "headache"]
}

Response:
{
  "success": true,
  "predictions": [
    {
      "disease": "Common Cold",
      "confidence": 85.5,
      "description": "...",
      "precautions": ["...", "..."]
    }
  ]
}
```

### Predict Cancer
```
POST /api/predict-cancer

Request Body:
{
  "features": [17.99, 10.38, 122.8, ...]  // 30 features
}

Response:
{
  "success": true,
  "diagnosis": "Benign",
  "confidence": 95.2,
  "risk_level": "Low",
  "probabilities": {
    "benign": 95.2,
    "malignant": 4.8
  }
}
```

### Get Disease Information
```
GET /api/disease-info/<disease_name>
```

### Calculate Severity Score
```
POST /api/severity-score

Request Body:
{
  "symptoms": ["fever", "chest_pain"]
}

Response:
{
  "total_score": 14,
  "average_score": 7.0,
  "severity_level": "Severe"
}
```

### Batch Prediction
```
POST /api/batch-predict

Request Body:
{
  "symptom_sets": [
    ["fever", "cough"],
    ["headache", "fatigue"]
  ]
}
```

---

## 🧪 Testing the API

### Using cURL

**Test Disease Prediction:**
```bash
curl -X POST http://localhost:5000/api/predict-disease \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "cough", "headache"]}'
```

**Test Cancer Prediction:**
```bash
curl -X POST http://localhost:5000/api/predict-cancer \
  -H "Content-Type: application/json" \
  -d '{"features": [17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}'
```

### Using Python Requests

```python
import requests

# Disease prediction
response = requests.post('http://localhost:5000/api/predict-disease', 
    json={'symptoms': ['fever', 'cough', 'fatigue']})
print(response.json())

# Cancer prediction
features = [17.99, 10.38, 122.8, ...] # 30 features
response = requests.post('http://localhost:5000/api/predict-cancer',
    json={'features': features})
print(response.json())
```

---

## 📊 Model Performance

### Disease Prediction Model
- **Algorithm**: Random Forest Classifier
- **Accuracy**: ~92% (varies by dataset)
- **Features**: 130+ symptoms
- **Classes**: 40+ diseases

### Cancer Diagnosis Model
- **Algorithm**: Gradient Boosting Classifier
- **Accuracy**: ~96% on test set
- **Features**: 30 tumor measurements
- **Classes**: Benign / Malignant

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
API_HOST=0.0.0.0
API_PORT=5000
CORS_ORIGINS=http://localhost:3000
```

### Frontend Configuration

Update `API_BASE_URL` in `App.jsx`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

---

## 🧬 Data Sources

1. **Disease-Symptom Dataset**: Curated medical dataset with disease-symptom mappings
2. **Cancer Dataset**: Wisconsin Breast Cancer Dataset (UCI ML Repository)
3. **Symptom Severity**: Medical literature-based severity weights
4. **Disease Descriptions**: Verified medical descriptions
5. **Precautions**: WHO and CDC guidelines

---

## ⚠️ Important Disclaimers

### Medical Disclaimer
This application is for **educational and informational purposes only**. It should NOT be used as:
- A substitute for professional medical advice
- A diagnostic tool for actual medical conditions
- A replacement for consultation with healthcare providers

### Limitations
- Predictions are based on statistical models, not clinical diagnosis
- Accuracy depends on data quality and completeness
- Individual cases may vary significantly
- Always consult qualified medical professionals

---

## 🐛 Troubleshooting

### Backend Issues

**Models not loading:**
```bash
python train_models.py
```

**Port already in use:**
```bash
# Change port in app.py
app.run(port=5001)
```

**CORS errors:**
```python
# Update CORS settings in app.py
CORS(app, origins=["http://localhost:3000"])
```

### Frontend Issues

**API connection failed:**
- Check backend is running on port 5000
- Update `API_BASE_URL` in App.jsx
- Check CORS configuration

**Dependencies not installing:**
```bash
npm install --legacy-peer-deps
```

---

## 📈 Future Enhancements

- [ ] User authentication & history
- [ ] Medical imaging analysis
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Real-time chat with medical bot
- [ ] Integration with wearable devices
- [ ] Appointment scheduling
- [ ] Prescription management

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Authors

Created for educational purposes as a demonstration of ML in healthcare applications.

---

## 🙏 Acknowledgments

- UCI Machine Learning Repository (Cancer Dataset)
- Medical symptom databases
- Open-source ML libraries (scikit-learn, Flask, React)
- Healthcare professionals for validation

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review API endpoints

---

## 🔒 Security Notes

- Never store real patient data
- Implement proper authentication for production
- Use HTTPS in production environments
- Regular security audits recommended
- Comply with HIPAA/GDPR if handling real data

---

**Remember**: This is a demonstration project. Always consult healthcare professionals for medical advice.

---

Made with ❤️ for healthcare education
