# 🧪 Testing Guide - Health Assistant Pro

This guide helps you test all features of the Health Assistant application.

## 🚀 Quick Test

After starting the application, verify it's working:

```bash
# Test backend health
curl http://localhost:5000/api/health

# Expected response:
# {"status":"healthy","disease_model":true,"cancer_model":true}
```

---

## 🔬 Automated Testing

### Run Complete Test Suite

```bash
# Make sure backend is running first
python app.py &

# In another terminal, run tests
python test-api-script.py
```

The test script checks:
- ✅ API health and connectivity
- ✅ Symptom retrieval
- ✅ Disease prediction with multiple test cases
- ✅ Cancer diagnosis with sample data
- ✅ Disease information lookup
- ✅ Severity score calculation
- ✅ Batch prediction functionality

---

## 🧪 Manual Testing Guide

### Test 1: Disease Prediction (Common Cold)

**Symptoms:** fever, cough, headache, fatigue

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/predict-disease \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "cough", "headache", "fatigue"]}'
```

**Expected:** Should predict "Common Cold" with high confidence

---

### Test 2: Disease Prediction (Diabetes)

**Symptoms:** increased_appetite, excessive_hunger, polyuria, fatigue

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/predict-disease \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["increased_appetite", "excessive_hunger", "polyuria", "fatigue"]}'
```

**Expected:** Should predict "Diabetes" with high confidence

---

### Test 3: Disease Prediction (Heart Attack)

**Symptoms:** chest_pain, breathlessness, sweating

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/predict-disease \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["chest_pain", "breathlessness", "sweating"]}'
```

**Expected:** Should predict "Heart attack" as top result

---

### Test 4: Cancer Diagnosis (Malignant Case)

**Features:** Sample malignant tumor data

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/predict-cancer \
  -H "Content-Type: application/json" \
  -d '{"features": [17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}'
```

**Expected:** 
- Diagnosis: "Malignant"
- Confidence: ~97-98%
- Risk Level: "High"

---

### Test 5: Cancer Diagnosis (Benign Case)

**Features:** Sample benign tumor data

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/predict-cancer \
  -H "Content-Type: application/json" \
  -d '{"features": [13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766, 0.2699, 0.7886, 2.058, 23.56, 0.008462, 0.0146, 0.02387, 0.01315, 0.0198, 0.0023, 15.11, 19.26, 99.7, 711.2, 0.144, 0.1773, 0.239, 0.1288, 0.2977, 0.07259]}'
```

**Expected:**
- Diagnosis: "Benign"
- Confidence: ~85-95%
- Risk Level: "Low"

---

### Test 6: Severity Score

**Symptoms:** high_fever, chest_pain, breathlessness

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/severity-score \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["high_fever", "chest_pain", "breathlessness"]}'
```

**Expected:**
- Total Score: 18
- Average Score: 6.0
- Severity Level: "Severe"

---

### Test 7: Get Disease Information

**Using curl:**
```bash
curl http://localhost:5000/api/disease-info/Common%20Cold
```

**Expected:** Returns description and precautions for Common Cold

---

### Test 8: Batch Prediction

**Multiple symptom sets:**

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/batch-predict \
  -H "Content-Type: application/json" \
  -d '{"symptom_sets": [["fever", "cough"], ["headache", "dizziness"], ["chest_pain", "breathlessness"]]}'
```

**Expected:** Returns predictions for all three symptom sets

---

## 🌐 Frontend Testing

### Manual UI Testing Checklist

#### Disease Predictor Tab
- [ ] Load symptom list (should show 130+ symptoms)
- [ ] Search for symptoms (e.g., "fever")
- [ ] Select multiple symptoms
- [ ] Verify selected symptoms appear in blue boxes
- [ ] Click "Predict Disease"
- [ ] Verify top 5 predictions appear
- [ ] Check confidence scores are displayed
- [ ] Verify precautions are shown
- [ ] Click "Reset" and verify form clears

#### Cancer Diagnosis Tab
- [ ] Click "Load Malignant Sample" button
- [ ] Verify all 30 fields are populated
- [ ] Click "Predict Diagnosis"
- [ ] Verify diagnosis shows "Malignant"
- [ ] Check confidence score is high (>90%)
- [ ] Verify risk level is "High"
- [ ] Click "Load Benign Sample"
- [ ] Verify diagnosis shows "Benign"
- [ ] Click "Reset" and verify fields clear

#### About Tab
- [ ] Click "About" tab
- [ ] Verify content loads
- [ ] Check all sections are readable
- [ ] Verify disclaimer is visible

---

## 🐛 Error Testing

### Test Error Handling

#### Empty Symptoms
```bash
curl -X POST http://localhost:5000/api/predict-disease \
  -H "Content-Type: application/json" \
  -d '{"symptoms": []}'
```
**Expected:** Error message "No symptoms provided"

#### Invalid Cancer Features
```bash
curl -X POST http://localhost:5000/api/predict-cancer \
  -H "Content-Type: application/json" \
  -d '{"features": [1, 2, 3]}'
```
**Expected:** Error message "Expected 30 features"

#### Non-existent Disease
```bash
curl http://localhost:5000/api/disease-info/NonExistentDisease
```
**Expected:** 404 error "Disease not found"

---

## 📊 Performance Testing

### Test Response Times

**Using curl with timing:**
```bash
# Disease prediction
time curl -X POST http://localhost:5000/api/predict-disease \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "cough"]}'

# Cancer prediction  
time curl -X POST http://localhost:5000/api/predict-cancer \
  -H "Content-Type: application/json" \
  -d '{"features": [17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}'
```

**Expected Response Times:**
- Disease Prediction: < 100ms
- Cancer Diagnosis: < 50ms
- Symptom List: < 20ms

---

## 🔄 Stress Testing

### Concurrent Requests

**Using Apache Bench (if installed):**
```bash
# Test 100 requests with 10 concurrent connections
ab -n 100 -c 10 -p test_payload.json -T application/json \
  http://localhost:5000/api/predict-disease
```

**Create test_payload.json:**
```json
{"symptoms": ["fever", "cough", "headache"]}
```

---

## ✅ Testing Checklist

### Backend API
- [ ] Health check returns healthy status
- [ ] All 7 endpoints respond correctly
- [ ] Error handling works properly
- [ ] Models load successfully
- [ ] Response times are acceptable
- [ ] CORS headers are present
- [ ] JSON responses are valid

### Frontend
- [ ] Application loads without errors
- [ ] All tabs are functional
- [ ] Symptom search works
- [ ] Disease prediction displays results
- [ ] Cancer diagnosis accepts input
- [ ] Sample data buttons work
- [ ] Reset buttons clear forms
- [ ] Responsive design works on mobile

### Models
- [ ] Disease model exists in models/ directory
- [ ] Cancer model exists in models/ directory
- [ ] Models can be loaded successfully
- [ ] Predictions are reasonable
- [ ] Confidence scores are valid (0-100%)

### Deployment
- [ ] Docker build succeeds
- [ ] Docker containers start properly
- [ ] docker-compose works end-to-end
- [ ] Setup scripts complete without errors
- [ ] Start scripts launch application

---

## 🎯 Sample Test Data

### Common Symptom Combinations

**Respiratory Issues:**
```json
{"symptoms": ["cough", "breathlessness", "phlegm", "chest_pain"]}
```

**Gastrointestinal:**
```json
{"symptoms": ["vomiting", "diarrhoea", "abdominal_pain", "nausea"]}
```

**Liver Problems:**
```json
{"symptoms": ["yellowish_skin", "yellowing_of_eyes", "dark_urine", "abdominal_pain"]}
```

**Cardiac:**
```json
{"symptoms": ["chest_pain", "breathlessness", "sweating", "fast_heart_rate"]}
```

### Cancer Feature Sets

**Malignant Sample 1:**
```json
{"features": [17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}
```

**Benign Sample 1:**
```json
{"features": [13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766, 0.2699, 0.7886, 2.058, 23.56, 0.008462, 0.0146, 0.02387, 0.01315, 0.0198, 0.0023, 15.11, 19.26, 99.7, 711.2, 0.144, 0.1773, 0.239, 0.1288, 0.2977, 0.07259]}
```

---

## 📝 Test Report Template

After testing, document your results:

```
# Test Report - Health Assistant Pro

## Test Date: [DATE]
## Tester: [NAME]
## Environment: [Local/Docker/Cloud]

### Backend Tests
- Health Check: ✅/❌
- Disease Prediction: ✅/❌
- Cancer Diagnosis: ✅/❌
- Error Handling: ✅/❌

### Frontend Tests
- UI Loading: ✅/❌
- Disease Tab: ✅/❌
- Cancer Tab: ✅/❌
- About Tab: ✅/❌

### Performance
- Average Response Time: [X]ms
- Concurrent Requests: [X]
- Memory Usage: [X]MB

### Issues Found
1. [Description]
2. [Description]

### Notes
[Any additional observations]
```

---

## 🆘 Troubleshooting Tests

### If Tests Fail

1. **Check backend is running:**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Check models are trained:**
   ```bash
   ls models/
   # Should see: disease_model.pkl, cancer_model.pkl, etc.
   ```

3. **Check logs for errors:**
   ```bash
   # Look at terminal where app.py is running
   ```

4. **Retrain models if needed:**
   ```bash
   python train-models-script.py
   ```

5. **Verify CSV files exist:**
   ```bash
   ls *.csv
   # Should see: dataset_cleaned.csv, Cancer_Data.csv, etc.
   ```

---

## 📞 Need Help?

If tests continue to fail:
1. Check the main README.md
2. Review DEPLOYMENT_README.md  
3. Verify all dependencies are installed
4. Try running setup script again
5. Check Python and Flask versions

---

**Happy Testing! 🧪**

Remember: This is an educational project. Test results should be analyzed critically and not used for actual medical decisions.
