# Quick Start: Pattern-Enhanced Cancer Prediction

## What's New?
Your Task 3 cancer diagnosis app now includes **Sequential Pattern Mining** from Task 2!

## Key Features Added

### 1. Pattern Detection Module (`pattern_detector.py`)
- Analyzes tumor features using GSP algorithm results
- Detects 32 discriminative patterns (18 malignant, 14 benign)
- Provides risk scores and explanations

### 2. Enhanced API Response
The `/api/predict-cancer` endpoint now returns:
```json
{
  "diagnosis": "Malignant",
  "confidence": 92.5,
  "pattern_analysis": {
    "malignant_patterns_detected": 18,
    "benign_patterns_detected": 11,
    "malignant_score": 2.58,
    "benign_score": 1.27,
    "agreement_with_model": true,
    "explanation": "..."
  },
  "top_patterns": {
    "top_malignant_patterns": [...],
    "top_benign_patterns": [...]
  }
}
```

### 3. Interactive Frontend Display
New UI section shows:
- 📊 Pattern detection counts (malignant/benign/agreement)
- 📈 Visual risk score bars
- 📝 Detailed explanation text
- 🔴🟢 Top detected patterns with strengths

## Quick Test

### Option 1: Direct Pattern Test (Fastest)
```bash
cd c:\Users\ivans\SC4020_Task3
.\venv\Scripts\python.exe test_pattern_direct.py
```

### Option 2: Full Integration Test
```bash
# Terminal 1: Start server
cd c:\Users\ivans\SC4020_Task3
.\venv\Scripts\Activate.ps1
python app.py

# Terminal 2: Run test
.\venv\Scripts\python.exe test_patterns.py
```

### Option 3: Use the Web UI
1. Start the Flask server (see above)
2. Open frontend: `cd frontend; npm start`
3. Go to "Cancer Diagnosis" tab
4. Click "Load Malignant Sample" or "Load Benign Sample"
5. Click "Predict Diagnosis"
6. Scroll down to see **Sequential Pattern Analysis** section!

## What Patterns Mean

### 🔴 Malignant Patterns
These indicate cancer risk:
- Large size features cluster together
- High values in: area, perimeter, radius
- Example: `{high_area_mean, high_perimeter_mean}` (23% support)

### 🟢 Benign Patterns
These indicate benign tumors:
- Diverse feature combinations
- Texture, smoothness, symmetry patterns
- Example: `{high_texture_mean, high_texture_worst}` (12% support)

## Understanding the Scores

- **Malignant Score**: Sum of strengths of detected malignant patterns (higher = more cancer risk)
- **Benign Score**: Sum of strengths of detected benign patterns (higher = less cancer risk)
- **Agreement**: Does pattern analysis match the ML model prediction?
  - ✅ Yes = More confident in prediction
  - ⚠️ No = Review case, possible edge case

## Interpreting Results

### Example 1: Strong Malignant Case
```
ML Model: Malignant (92.5% confidence)
Patterns: 18 malignant, 11 benign
Scores: Malignant=2.58, Benign=1.27
Agreement: ✅ YES
```
**Interpretation**: High confidence, patterns support ML prediction. Clear malignant case.

### Example 2: Edge Case
```
ML Model: Benign (55% confidence)
Patterns: 0 malignant, 0 benign
Scores: Malignant=0.0, Benign=0.0
Agreement: ✅ YES (by default)
```
**Interpretation**: No strong patterns detected. Rely primarily on ML model. Consider additional tests.

### Example 3: Disagreement (Rare)
```
ML Model: Malignant (65% confidence)
Patterns: 2 malignant, 8 benign
Scores: Malignant=0.35, Benign=0.92
Agreement: ⚠️ NO
```
**Interpretation**: Patterns suggest benign, but ML says malignant. Flag for medical review!

## API Usage

### With Pattern Analysis (Default)
```python
import requests

response = requests.post('http://localhost:5000/api/predict-cancer', json={
    'features': [17.99, 10.38, 122.8, ...],  # 30 values
    'include_patterns': True  # Optional, defaults to True
})

result = response.json()
print(result['diagnosis'])
print(result['pattern_analysis']['explanation'])
```

### Without Pattern Analysis
```python
response = requests.post('http://localhost:5000/api/predict-cancer', json={
    'features': [...],
    'include_patterns': False  # Faster, ML-only prediction
})
```

## Technical Details

- **Algorithm**: GSP (Generalized Sequential Pattern Mining)
- **Binning**: Quantile discretization (3 bins: low/medium/high)
- **Training Data**: 569 cancer samples (212 malignant, 357 benign)
- **Patterns**: Mined from Task 2 with min_support=15, max_length=10
- **Overhead**: ~5-10ms per prediction (negligible)

## Files to Check

1. **`pattern_detector.py`** - Core pattern detection logic
2. **`app.py`** - Flask API with enhanced `/api/predict-cancer` endpoint
3. **`frontend/src/App.js`** - UI with pattern analysis display
4. **`GSP_INTEGRATION.md`** - Complete integration documentation
5. **`test_pattern_direct.py`** - Direct pattern detector test
6. **`test_patterns.py`** - Full integration test

## Troubleshooting

### Pattern detector not loading
**Error**: `ModuleNotFoundError: No module named 'pattern_detector'`
**Fix**: Make sure `pattern_detector.py` is in the same directory as `app.py`

### Discretizer warning
**Warning**: `FutureWarning: quantile_method='linear'...`
**Impact**: Harmless warning, does not affect functionality

### Server not starting
**Error**: `Port 5000 already in use`
**Fix**: 
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py:
app.run(host='0.0.0.0', port=5001, debug=True)
```

### No patterns detected
**Reason**: Some samples may not match the 32 pre-defined patterns
**Solution**: This is normal! Fall back to ML model prediction

## Next Steps

1. ✅ **Test the integration** with `test_pattern_direct.py`
2. ✅ **Try the web UI** and see pattern analysis in action
3. ✅ **Review `GSP_INTEGRATION.md`** for complete documentation
4. 📊 **Analyze patterns** to understand what makes tumors malignant vs benign
5. 🎓 **Use for SC4020 Task 3** submission and presentation!

## Questions?

Check these files:
- `GSP_INTEGRATION.md` - Complete integration guide
- `task2/gsp4cancer.py` - Original GSP algorithm
- `task2/output_quantile.txt` - Pattern mining results

**Congratulations! Your cancer diagnosis app now has advanced pattern mining capabilities!** 🎉
