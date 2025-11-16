"""
Test script for pattern detection integration
"""
import requests
import json

API_URL = "http://localhost:5000"

# Sample malignant tumor features (from first row of Cancer_Data.csv)
malignant_sample = [
    17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
    1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
    25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
]

# Sample benign tumor features
benign_sample = [
    13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766,
    0.2699, 0.7886, 2.058, 23.56, 0.008462, 0.0146, 0.02387, 0.01315, 0.0198, 0.0023,
    15.11, 19.26, 99.7, 711.2, 0.144, 0.1773, 0.239, 0.1288, 0.2977, 0.07259
]

def test_cancer_prediction(features, label):
    """Test cancer prediction with pattern analysis"""
    print(f"\n{'='*60}")
    print(f"Testing {label} Sample")
    print(f"{'='*60}")
    
    payload = {
        'features': features,
        'include_patterns': True
    }
    
    try:
        response = requests.post(f"{API_URL}/api/predict-cancer", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✓ API Response: Success")
            print(f"\n📊 ML MODEL PREDICTION:")
            print(f"  Diagnosis: {result['diagnosis']}")
            print(f"  Confidence: {result['confidence']}%")
            print(f"  Risk Level: {result['risk_level']}")
            print(f"  Probabilities: Benign={result['probabilities']['benign']}%, Malignant={result['probabilities']['malignant']}%")
            
            if 'pattern_analysis' in result:
                pa = result['pattern_analysis']
                print(f"\n🔍 SEQUENTIAL PATTERN ANALYSIS:")
                print(f"  Malignant patterns detected: {pa['malignant_patterns_detected']}")
                print(f"  Benign patterns detected: {pa['benign_patterns_detected']}")
                print(f"  Malignant score: {pa['malignant_score']}")
                print(f"  Benign score: {pa['benign_score']}")
                print(f"  Pattern prediction: {pa['pattern_prediction']}")
                print(f"  Pattern confidence: {pa['pattern_confidence']}%")
                print(f"  Agreement with ML model: {pa['agreement_with_model']}")
                
                print(f"\n📝 EXPLANATION:")
                print(pa['explanation'])
                
                if 'top_patterns' in result:
                    tp = result['top_patterns']
                    print(f"\n🔴 TOP MALIGNANT PATTERNS:")
                    for i, p in enumerate(tp['top_malignant_patterns'], 1):
                        print(f"  {i}. {' → '.join(p['pattern'])} (strength: {p['strength']:.3f})")
                    
                    print(f"\n🟢 TOP BENIGN PATTERNS:")
                    for i, p in enumerate(tp['top_benign_patterns'], 1):
                        print(f"  {i}. {' → '.join(p['pattern'])} (strength: {p['strength']:.3f})")
            else:
                print("\n⚠️  Pattern analysis not available")
                
        else:
            print(f"\n✗ API Error: {response.status_code}")
            print(f"  {response.text}")
            
    except Exception as e:
        print(f"\n✗ Connection Error: {e}")
        print("  Make sure the Flask server is running on http://localhost:5000")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("PATTERN DETECTION INTEGRATION TEST")
    print("="*60)
    
    # Test health endpoint
    try:
        health = requests.get(f"{API_URL}/api/health")
        if health.status_code == 200:
            h = health.json()
            print(f"\n✓ Server Status: {h['status']}")
            print(f"  Disease Model: {'Loaded' if h['disease_model'] else 'Not Loaded'}")
            print(f"  Cancer Model: {'Loaded' if h['cancer_model'] else 'Not Loaded'}")
        else:
            print(f"\n✗ Server not responding")
            exit(1)
    except Exception as e:
        print(f"\n✗ Cannot connect to server: {e}")
        print("  Please start the Flask server: python app.py")
        exit(1)
    
    # Test both samples
    test_cancer_prediction(malignant_sample, "MALIGNANT")
    test_cancer_prediction(benign_sample, "BENIGN")
    
    print(f"\n{'='*60}")
    print("TEST COMPLETE")
    print(f"{'='*60}\n")
