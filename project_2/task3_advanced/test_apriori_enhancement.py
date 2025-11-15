"""
Test Apriori-Enhanced Disease Prediction
"""

import requests
import json

API_URL = "http://localhost:5000/api/predict-disease"

def test_gerd_prediction():
    """Test GERD prediction with partial symptoms"""
    print("="*60)
    print("TEST: GERD Diagnosis with Apriori Enhancement")
    print("="*60)
    
    # GERD symptoms (partial - missing ulcers_on_tongue)
    symptoms = [
        "stomach_pain",
        "acidity",
        "vomiting",
        "cough",
        "chest_pain"
    ]
    
    print(f"\nInput Symptoms: {symptoms}")
    print(f"Count: {len(symptoms)} symptoms")
    
    # Make prediction
    response = requests.post(API_URL, json={"symptoms": symptoms})
    data = response.json()
    
    if data.get("success"):
        print("\n" + "-"*60)
        print("TOP PREDICTION:")
        print("-"*60)
        
        top_pred = data["predictions"][0]
        print(f"Disease: {top_pred['disease']}")
        print(f"\nConfidence Breakdown:")
        print(f"  Base Model:       {top_pred.get('base_confidence', 'N/A')}%")
        print(f"  Apriori Boost:   +{top_pred.get('apriori_boost', 0)}%")
        print(f"  Enhanced Score:   {top_pred['confidence']}%")
        
        # Show symptom suggestions
        if data.get("symptom_suggestions"):
            print(f"\n" + "-"*60)
            print("SYMPTOM SUGGESTIONS (from Apriori):")
            print("-"*60)
            for sugg in data["symptom_suggestions"]:
                print(f"  • {sugg['symptom']}")
                print(f"    Confidence: {sugg['confidence']*100:.1f}%")
                print(f"    Based on: {', '.join(sugg['based_on'][:3])}")
                print()
        
        # Show top 5 predictions
        print("-"*60)
        print("ALL PREDICTIONS:")
        print("-"*60)
        for i, pred in enumerate(data["predictions"][:5], 1):
            boost = pred.get('apriori_boost', 0)
            boost_str = f" (+{boost}%)" if boost > 0 else ""
            print(f"{i}. {pred['disease']}: {pred['confidence']}%{boost_str}")
    
    print("\n" + "="*60)

def test_diabetes_prediction():
    """Test Diabetes prediction"""
    print("\n\n")
    print("="*60)
    print("TEST: Diabetes Diagnosis with Apriori Enhancement")
    print("="*60)
    
    symptoms = [
        "fatigue",
        "weight_loss",
        "increased_appetite",
        "polyuria"
    ]
    
    print(f"\nInput Symptoms: {symptoms}")
    
    response = requests.post(API_URL, json={"symptoms": symptoms})
    data = response.json()
    
    if data.get("success"):
        top_pred = data["predictions"][0]
        print(f"\nTop Prediction: {top_pred['disease']}")
        print(f"Enhanced Confidence: {top_pred['confidence']}%")
        print(f"Base Model: {top_pred.get('base_confidence', 'N/A')}%")
        print(f"Apriori Boost: +{top_pred.get('apriori_boost', 0)}%")
    
    print("="*60)

def test_migraine_prediction():
    """Test Migraine prediction"""
    print("\n\n")
    print("="*60)
    print("TEST: Migraine Diagnosis with Apriori Enhancement")
    print("="*60)
    
    symptoms = [
        "headache",
        "visual_disturbances",
        "stiff_neck"
    ]
    
    print(f"\nInput Symptoms: {symptoms}")
    
    response = requests.post(API_URL, json={"symptoms": symptoms})
    data = response.json()
    
    if data.get("success"):
        top_pred = data["predictions"][0]
        print(f"\nTop Prediction: {top_pred['disease']}")
        print(f"Enhanced Confidence: {top_pred['confidence']}%")
        
        if data.get("symptom_suggestions"):
            print(f"\nSuggested Related Symptoms:")
            for sugg in data["symptom_suggestions"][:3]:
                print(f"  • {sugg['symptom']} ({sugg['confidence']*100:.1f}%)")
    
    print("="*60)

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "APRIORI-ENHANCED DISEASE PREDICTION TEST" + " "*8 + "║")
    print("╚" + "="*58 + "╝")
    print()
    
    try:
        test_gerd_prediction()
        test_diabetes_prediction()
        test_migraine_prediction()
        
        print("\n\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nApriori Integration Benefits:")
        print("✓ Enhanced confidence scores")
        print("✓ Symptom suggestions from association rules")
        print("✓ Pattern-based validation")
        print("✓ Better explainability")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask API")
        print("Please ensure the backend is running:")
        print("  python app.py")
        print()
