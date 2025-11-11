
#  Health Assistant Pro - SC4020 Task 3

> **AI-Powered Disease Prediction & Cancer Diagnosis System**

This project implements Task 3 of the SC4020 Data Mining course, building a complete healthcare application that applies insights from Tasks 1 (Apriori) and 2 (GSP).

##  Quick Start

**Windows:**
```cmd
setup.bat
start.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh start.sh
./setup.sh
./start.sh
```

**Docker:**
```bash
docker-compose up --build
```

Access at: `http://localhost:5000`

** Full documentation: See [DEPLOYMENT_README.md](DEPLOYMENT_README.md)**

---

## What's Implemented

### Task 3 Solution Features

1. **Disease Prediction Engine**
   - 130+ symptoms analyzed
   - 40+ diseases predicted
   - Confidence scoring
   - Precautionary recommendations
   - Real-time web interface

2. **Cancer Diagnosis System**
   - Breast cancer classification
   - 30 tumor feature analysis  
   - 96%+ accuracy
   - Risk level assessment
   - Interactive feature input

3. **Full-Stack Web Application**
   - React frontend with modern UI
   - Flask REST API backend
   - Machine Learning models
   - Docker deployment ready
   - Comprehensive testing suite

### How It Connects to Tasks 1 & 2

| From Task | Knowledge Applied | In Task 3 |
|-----------|------------------|-----------|
| **Task 1 (Apriori)** | Frequent symptom itemsets | Symptom-based disease prediction with association rules |
| **Task 2 (GSP)** | Sequential cancer feature patterns | Feature-based cancer diagnosis with pattern recognition |

---

## Project Files

### Core Application Files
- **app.py** - Flask REST API server (Fixed all bugs)
- **train-models-script.py** - ML model training
- **frontend/** - React web application
- **models/** - Trained ML models (generated)

### Data Files
- **dataset_cleaned.csv** - Disease-symptom mappings
- **Cancer_Data.csv** - Wisconsin breast cancer data
- **symptom_Description.csv** - Disease descriptions
- **symptom_precaution.csv** - Safety measures
- **Symptom-severity.csv** - Symptom weights

### Deployment Files
- **Dockerfile** - Backend container
- **docker-compose.yml** - Multi-container setup
- **setup.bat / setup.sh** - Automated installation
- **start.bat / start.sh** - Quick launch scripts
- **.env.example** - Configuration template

---

## Bug Fixes Applied

### Critical Fixes
1.  **Fixed deprecated `@app.before_first_request`** - Updated to Flask 2.3+ compatible initialization
2.  **Removed invalid `pickle-mixin`** dependency - Not needed for scikit-learn
3.  **Added absolute path handling** - Prevents file not found errors
4.  **Added proper error handling** - Comprehensive try-catch with tracebacks
5.  **Fixed CORS configuration** - Allows frontend-backend communication
6.  **Added model directory creation** - Prevents missing directory errors

### Enhancements
-  Production-ready Docker configuration
-  Health check endpoints
-  Comprehensive logging
-  Environment variable support
-  Automated setup scripts
-  Complete test suite

---

##  API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/symptoms` | GET | Get all symptoms |
| `/api/predict-disease` | POST | Predict disease from symptoms |
| `/api/predict-cancer` | POST | Diagnose cancer from features |
| `/api/disease-info/<name>` | GET | Get disease details |
| `/api/severity-score` | POST | Calculate symptom severity |
| `/api/batch-predict` | POST | Batch predictions |

See [DEPLOYMENT_README.md](DEPLOYMENT_README.md) for full API documentation.

---

##  Testing

```bash
# Run comprehensive API tests
python test-api-script.py

# Test individual endpoint
curl http://localhost:5000/api/health
```

---

##  Important Notes

1. **Educational Purpose Only** - Not for actual medical diagnosis
2. **No PHI** - Does not collect or store personal health information
3. **Demo Data** - Uses public datasets for demonstration
4. **Consult Professionals** - Always seek qualified medical advice

---

##  Model Performance

### Disease Prediction
- **Algorithm:** Random Forest
- **Training Accuracy:** ~92%
- **CV Score:** ~90%
- **Features:** 130+
- **Classes:** 40+

### Cancer Diagnosis
- **Algorithm:** Gradient Boosting
- **Testing Accuracy:** ~96%
- **Features:** 30
- **Classes:** 2 (Benign/Malignant)

---

## Overview

This project explores **data mining in healthcare** through three main tasks.  
Each task builds on the previous one to extract knowledge from medical data and apply it to a real-world healthcare problem.

| Task | Focus | Algorithm | Dataset | Weight |
|------|--------|------------|----------|---------|
| 1 | Symptom co-occurrence | Apriori | Disease–Symptom dataset | 30% |
| 2 | Cancer feature sequences | GSP (Generalized Sequential Pattern) | Breast Cancer Wisconsin dataset | 40% |
| 3 | Open healthcare application | Flexible | One or both datasets | 30% |

---

## Task 1 — Symptom Co-occurrence (Apriori)

### Goal  
Find **symptom combinations** that frequently occur together in the same disease.

### Method  
- Treat each **disease** as a *basket* and its **symptoms** as *items*.  
- Implement the **Apriori algorithm** from scratch to mine frequent itemsets and association rules.  
- Select suitable **minimum support** and **confidence** thresholds.  
- Clean the data by normalizing symptom names and handling duplicates.  
- Optionally augment with mirrored datasets for robustness.

### Outputs  
- **Frequent itemsets:** groups of symptoms often co-occurring.  
- **Association rules:** e.g. `{fever, cough} → {sore throat}`.  
- **Metrics:** support, confidence, and lift values.  
- **Clinical interpretation:** meaningful symptom clusters (e.g. respiratory, gastrointestinal).

### Insight Produced  
Task 1 provides **knowledge of symptom co-occurrence**, forming a foundation for explainable, symptom-driven reasoning in healthcare applications.

---

## Task 2 — Cancer Feature Sequences (GSP)

### Goal  
Discover **ordered feature patterns** that distinguish **malignant** and **benign** breast cancer cases.

### Method  
1. **Discretization:** Convert continuous features into *low / medium / high* categories using  
   - Uniform,  
   - Quantile, and  
   - K-means binning (perform sensitivity analysis).  
2. **Ranking:** Rank features per patient by z-score or mutual information w.r.t. diagnosis.  
3. **Sequence Creation:** Form top-k ordered itemsets (sequence length ≤ L, max-gap = 1).  
4. **Run GSP:** Mine frequent sequences separately for malignant and benign groups.  
5. **Reporting:** Compare mined patterns across binning strategies and note computational complexity.

### Outputs  
- **Frequent sequences:** e.g. ⟨{high_radius}, {high_texture}⟩ → malignant.  
- **Group-specific trends:** distinguishing patterns for each diagnosis type.  
- **Sensitivity study:** how discretization choice affects patterns.

### Insight Produced  
Task 2 yields **diagnostic feature patterns** — interpretable signatures that highlight key differences between malignant and benign samples.

---

## Task 3 — Open Healthcare Application (Your Part)

### Goal  
Develop a **working healthcare application** that uses insights or data from Tasks 1 and/or 2.  
Use any valid analytical, machine-learning, deep-learning, or LLM-based approach, provided the design is **justified** and **reproducible**.

### Requirements  
- Functional and documented code.  
- Evidence of results (plots, screenshots, evaluation metrics).  
- Clear explanation covering:
  - Objective and motivation.  
  - Data and preprocessing steps.  
  - Algorithms or models used.  
  - Connection to Tasks 1–2.  
  - Evaluation or qualitative demonstration.  
  - Justification of design choices.

### Recommended Skills & Tools
| Area | Libraries / Skills | Purpose |
|------|--------------------|----------|
| Data handling | `pandas`, `numpy` | Clean and transform data |
| Visualization | `matplotlib`, `seaborn`, `plotly` | Plot patterns and results |
| Machine learning | `scikit-learn`, `mlxtend` | Train or evaluate models |
| Optional NLP / LLM | `transformers`, `openai` (if allowed) | Build explainable or conversational tools |
| Reporting | Markdown / Jupyter / PDF | Document methodology and outcomes |

---

## How Tasks 1 & 2 Support Task 3

| Source | What It Produces | How It Helps Task 3 |
|---------|------------------|---------------------|
| **Task 1 (Apriori)** | Frequent symptom sets and association rules | Enables symptom-level reasoning, clustering, and explainable diagnostic tools |
| **Task 2 (GSP)** | Sequential cancer feature patterns | Supports cancer risk scoring, feature selection, and interpretability |
| **Both Combined** | Knowledge of symptom + feature relationships | Enables integrated, multi-level healthcare decision support |

---

## Example Project Ideas for Task 3

| Idea | Dataset(s) | Approach | Example Output |
|------|-------------|-----------|----------------|
| **Symptom-Based Disease Recommender** | Disease–Symptom | Use Apriori rules to suggest likely diseases from entered symptoms | Input: {fever, cough} → Suggest: Influenza, COVID-19 |
| **Cancer Risk Scoring Tool** | Breast Cancer | Use GSP sequences as interpretable rules or features in a classifier | Pattern ⟨{high_radius}, {high_texture}⟩ → High malignancy risk |
| **Hybrid Diagnostic Assistant** | Both | Combine Apriori + GSP insights into an explainable decision system | Step 1: Predict disease → Step 2: Assess malignancy likelihood |

---

## Inter-Task Summary

| Task | Output | Knowledge Type | Contribution |
|------|---------|----------------|---------------|
| **1** | Frequent symptom itemsets + association rules | Symptom-level patterns | Foundation for symptom reasoning and clustering |
| **2** | Frequent feature sequences for M/B | Diagnostic feature patterns | Foundation for explainable cancer assessment |
| **3** | Working healthcare application | Applied decision logic | Demonstrates practical, justified use of mined knowledge |

---

