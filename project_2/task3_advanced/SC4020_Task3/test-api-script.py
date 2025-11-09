"""
Comprehensive API Testing Script
Tests all endpoints of the Health Assistant API
"""

import requests
import json
import time
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

API_BASE_URL = "http://localhost:5000/api"

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"{Fore.CYAN}{Style.BRIGHT}{text:^70}")
    print("="*70)

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}✗ {text}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.YELLOW}ℹ {text}")

def print_response(response_data):
    """Pretty print JSON response"""
    print(f"{Fore.BLUE}{json.dumps(response_data, indent=2)}")

def test_health_check():
    """Test API health check endpoint"""
    print_header("Testing Health Check Endpoint")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"API is healthy!")
            print_response(data)
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is the server running?")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_get_symptoms():
    """Test get symptoms endpoint"""
    print_header("Testing Get Symptoms Endpoint")
    
    try:
        response = requests.get(f"{API_BASE_URL}/symptoms", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved {data['count']} symptoms")
            print_info(f"First 10 symptoms: {data['symptoms'][:10]}")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_disease_prediction():
    """Test disease prediction endpoint"""
    print_header("Testing Disease Prediction Endpoint")
    
    test_cases = [
        {
            "name": "Common Cold Symptoms",
            "symptoms": ["fever", "cough", "headache", "fatigue"]
        },
        {
            "name": "Diabetes Symptoms",
            "symptoms": ["increased_appetite", "excessive_hunger", "polyuria", "fatigue"]
        },
        {
            "name": "Heart Attack Symptoms",
            "symptoms": ["chest_pain", "breathlessness", "sweating"]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{Fore.MAGENTA}Test Case: {test_case['name']}")
        print_info(f"Symptoms: {', '.join(test_case['symptoms'])}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/predict-disease",
                json={"symptoms": test_case["symptoms"]},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print_success(f"Prediction successful!")
                    
                    if data.get('predictions'):
                        print(f"\n{Fore.GREEN}Top 3 Predictions:")
                        for i, pred in enumerate(data['predictions'][:3], 1):
                            print(f"  {i}. {pred['disease']} - {pred['confidence']:.1f}% confidence")
                            if pred.get('precautions'):
                                print(f"     Precautions: {', '.join(pred['precautions'][:2])}")
                    return True
                else:
                    print_error(f"Prediction failed: {data.get('error')}")
            else:
                print_error(f"Request failed with status {response.status_code}")
                print_response(response.json())
        except Exception as e:
            print_error(f"Error: {str(e)}")
        
        time.sleep(1)  # Small delay between requests
    
    return True

def test_cancer_prediction():
    """Test cancer prediction endpoint"""
    print_header("Testing Cancer Prediction Endpoint")
    
    # Sample feature values (from dataset)
    test_cases = [
        {
            "name": "Malignant Case",
            "features": [17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 
                        0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 
                        0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 
                        184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]
        },
        {
            "name": "Benign Case",
            "features": [13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781,
                        0.1885, 0.05766, 0.2699, 0.7886, 2.058, 23.56, 0.008462,
                        0.0146, 0.02387, 0.01315, 0.0198, 0.0023, 15.11, 19.26,
                        99.7, 711.2, 0.144, 0.1773, 0.239, 0.1288, 0.2977, 0.07259]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{Fore.MAGENTA}Test Case: {test_case['name']}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/predict-cancer",
                json={"features": test_case["features"]},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print_success(f"Prediction successful!")
                    print(f"\n{Fore.GREEN}Results:")
                    print(f"  Diagnosis: {data['diagnosis']}")
                    print(f"  Confidence: {data['confidence']}%")
                    print(f"  Risk Level: {data['risk_level']}")
                    print(f"  Benign Probability: {data['probabilities']['benign']}%")
                    print(f"  Malignant Probability: {data['probabilities']['malignant']}%")
                else:
                    print_error(f"Prediction failed: {data.get('error')}")
            else:
                print_error(f"Request failed with status {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
        
        time.sleep(1)
    
    return True

def test_disease_info():
    """Test disease information endpoint"""
    print_header("Testing Disease Info Endpoint")
    
    diseases = ["Common Cold", "Diabetes", "Hypertension"]
    
    for disease in diseases:
        print(f"\n{Fore.MAGENTA}Fetching info for: {disease}")
        
        try:
            response = requests.get(f"{API_BASE_URL}/disease-info/{disease}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print_success(f"Information retrieved!")
                    info = data.get('info', {})
                    if info.get('description'):
                        print(f"  Description: {info['description'][:100]}...")
                    if info.get('precautions'):
                        print(f"  Precautions: {', '.join(info['precautions'][:2])}")
            else:
                print_error(f"Request failed with status {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
        
        time.sleep(0.5)
    
    return True

def test_severity_score():
    """Test severity score calculation"""
    print_header("Testing Severity Score Endpoint")
    
    test_symptoms = ["high_fever", "chest_pain", "breathlessness"]
    print_info(f"Symptoms: {', '.join(test_symptoms)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/severity-score",
            json={"symptoms": test_symptoms},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Severity calculated!")
                print(f"\n{Fore.GREEN}Results:")
                print(f"  Total Score: {data['total_score']}")
                print(f"  Average Score: {data['average_score']}")
                print(f"  Severity Level: {data['severity_level']}")
                
                if data.get('symptom_scores'):
                    print(f"\n  Individual Scores:")
                    for score in data['symptom_scores']:
                        print(f"    - {score['symptom']}: {score['severity']}")
                return True
        else:
            print_error(f"Request failed with status {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print_header("Testing Batch Prediction Endpoint")
    
    symptom_sets = [
        ["fever", "cough"],
        ["headache", "dizziness"],
        ["chest_pain", "breathlessness"]
    ]
    
    print_info(f"Testing {len(symptom_sets)} symptom sets")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/batch-predict",
            json={"symptom_sets": symptom_sets},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Batch prediction successful!")
                print(f"\n{Fore.GREEN}Results:")
                for i, result in enumerate(data['results'], 1):
                    print(f"  {i}. Symptoms: {', '.join(result['symptoms'])}")
                    print(f"     Prediction: {result['prediction']} ({result['confidence']}%)")
                return True
        else:
            print_error(f"Request failed with status {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return False

def run_all_tests():
    """Run all API tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + f"{Fore.CYAN}{Style.BRIGHT}{'HEALTH ASSISTANT API TEST SUITE':^68}" + Style.RESET_ALL + "║")
    print("╚" + "="*68 + "╝")
    
    tests = [
        ("Health Check", test_health_check),
        ("Get Symptoms", test_get_symptoms),
        ("Disease Prediction", test_disease_prediction),
        ("Cancer Prediction", test_cancer_prediction),
        ("Disease Information", test_disease_info),
        ("Severity Score", test_severity_score),
        ("Batch Prediction", test_batch_prediction)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
        
        time.sleep(1)
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}Tests Passed: {Fore.GREEN}{passed}{Fore.CYAN}/{total}")
    print(f"{'='*70}\n")
    
    if passed == total:
        print(f"{Fore.GREEN}{Style.BRIGHT}🎉 All tests passed successfully!")
    else:
        print(f"{Fore.YELLOW}⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests interrupted by user.")
    except Exception as e:
        print_error(f"Test suite crashed: {str(e)}")
