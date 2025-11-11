from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os

app = Flask(__name__)
CORS(app)

# Global variables for models
disease_model = None
cancer_model = None
scaler = None
label_encoder = None
symptom_list = []
disease_info = {}

def load_datasets():
    """Load all CSV datasets"""
    try:
        import os
        # Get the directory of the current file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load disease-symptom dataset
        disease_df = pd.read_csv(os.path.join(base_dir, 'dataset_cleaned.csv'))
        
        # Load cancer dataset
        cancer_df = pd.read_csv(os.path.join(base_dir, 'Cancer_Data.csv'))
        
        # Load descriptions
        descriptions_df = pd.read_csv(os.path.join(base_dir, 'symptom_Description.csv'))
        
        # Load precautions
        precautions_df = pd.read_csv(os.path.join(base_dir, 'symptom_precaution.csv'))
        
        # Load severity
        severity_df = pd.read_csv(os.path.join(base_dir, 'Symptom-severity.csv'))
        
        return disease_df, cancer_df, descriptions_df, precautions_df, severity_df
    except Exception as e:
        print(f"Error loading datasets: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None, None

def prepare_disease_model():
    """Load pre-trained disease prediction model"""
    global disease_model, label_encoder, symptom_list, disease_info
    
    try:
        # Load pre-trained model and artifacts
        with open('models/disease_model.pkl', 'rb') as f:
            disease_model = pickle.load(f)
        
        with open('models/disease_label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
        
        with open('models/symptom_list.pkl', 'rb') as f:
            symptom_list = pickle.load(f)
        
        # Load disease info from CSV files
        _, _, descriptions_df, precautions_df, _ = load_datasets()
        
        # Prepare disease info
        for _, row in descriptions_df.iterrows():
            disease = row['Disease']
            disease_info[disease] = {
                'description': row['Description']
            }
        
        for _, row in precautions_df.iterrows():
            disease = row['Disease']
            if disease in disease_info:
                precautions = [
                    row['Precaution_1'], 
                    row['Precaution_2'], 
                    row['Precaution_3'], 
                    row['Precaution_4']
                ]
                disease_info[disease]['precautions'] = [p for p in precautions if pd.notna(p)]
        
        print("Disease prediction model loaded successfully!")
        return True
    
    except Exception as e:
        print(f"Error loading disease model: {e}")
        import traceback
        traceback.print_exc()
        return False

def prepare_cancer_model():
    """Load pre-trained cancer diagnosis model"""
    global cancer_model, scaler
    
    try:
        # Load pre-trained model and artifacts
        with open('models/cancer_model.pkl', 'rb') as f:
            cancer_model = pickle.load(f)
        
        with open('models/cancer_scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        
        print("Cancer prediction model loaded successfully!")
        return True
    
    except Exception as e:
        print(f"Error loading cancer model: {e}")
        import traceback
        traceback.print_exc()
        return False

# Initialize models on startup - Fixed for Flask 2.3+
# Models are now initialized in __main__ block instead of using deprecated decorator

@app.route('/')
def home():
    return jsonify({
        'message': 'Health Assistant API',
        'version': '1.0',
        'endpoints': {
            '/api/symptoms': 'GET - Get all available symptoms',
            '/api/predict-disease': 'POST - Predict disease from symptoms',
            '/api/predict-cancer': 'POST - Predict cancer diagnosis',
            '/api/disease-info/<disease>': 'GET - Get disease information',
            '/api/health': 'GET - API health check'
        }
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'disease_model': disease_model is not None,
        'cancer_model': cancer_model is not None
    })

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get all available symptoms"""
    return jsonify({
        'symptoms': symptom_list,
        'count': len(symptom_list)
    })

@app.route('/api/predict-disease', methods=['POST'])
def predict_disease():
    """Predict disease based on symptoms"""
    try:
        data = request.get_json()
        selected_symptoms = data.get('symptoms', [])
        
        if not selected_symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Create feature vector
        feature_vector = [1 if symptom in selected_symptoms else 0 for symptom in symptom_list]
        feature_vector = np.array(feature_vector).reshape(1, -1)
        
        # Get predictions with probabilities
        prediction_proba = disease_model.predict_proba(feature_vector)[0]
        
        # Get top 5 predictions
        top_5_indices = np.argsort(prediction_proba)[-5:][::-1]
        
        predictions = []
        for idx in top_5_indices:
            disease = label_encoder.inverse_transform([idx])[0]
            confidence = float(prediction_proba[idx] * 100)
            
            if confidence > 0:
                pred_data = {
                    'disease': disease,
                    'confidence': round(confidence, 2),
                    'description': disease_info.get(disease, {}).get('description', 'No description available'),
                    'precautions': disease_info.get(disease, {}).get('precautions', [])
                }
                predictions.append(pred_data)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'symptoms_provided': len(selected_symptoms)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict-cancer', methods=['POST'])
def predict_cancer():
    """Predict cancer diagnosis from features"""
    try:
        data = request.get_json()
        features = data.get('features', [])
        
        if len(features) != 30:
            return jsonify({'error': 'Expected 30 features'}), 400
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Predict
        prediction = cancer_model.predict(features_scaled)[0]
        probability = cancer_model.predict_proba(features_scaled)[0]
        
        diagnosis = 'Malignant' if prediction == 1 else 'Benign'
        confidence = float(max(probability) * 100)
        
        return jsonify({
            'success': True,
            'diagnosis': diagnosis,
            'confidence': round(confidence, 2),
            'risk_level': 'High' if prediction == 1 and confidence > 80 else 'Medium' if prediction == 1 else 'Low',
            'probabilities': {
                'benign': round(float(probability[0]) * 100, 2),
                'malignant': round(float(probability[1]) * 100, 2)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/disease-info/<disease>', methods=['GET'])
def get_disease_info(disease):
    """Get detailed information about a disease"""
    if disease in disease_info:
        return jsonify({
            'success': True,
            'disease': disease,
            'info': disease_info[disease]
        })
    else:
        return jsonify({'error': 'Disease not found'}), 404

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """Batch prediction for multiple symptom sets"""
    try:
        data = request.get_json()
        symptom_sets = data.get('symptom_sets', [])
        
        results = []
        for symptoms in symptom_sets:
            feature_vector = [1 if symptom in symptoms else 0 for symptom in symptom_list]
            feature_vector = np.array(feature_vector).reshape(1, -1)
            
            prediction_proba = disease_model.predict_proba(feature_vector)[0]
            top_idx = np.argmax(prediction_proba)
            disease = label_encoder.inverse_transform([top_idx])[0]
            confidence = float(prediction_proba[top_idx] * 100)
            
            results.append({
                'symptoms': symptoms,
                'prediction': disease,
                'confidence': round(confidence, 2)
            })
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/severity-score', methods=['POST'])
def calculate_severity():
    """Calculate severity score based on symptoms"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        _, _, _, _, severity_df = load_datasets()
        
        total_score = 0
        symptom_scores = []
        
        for symptom in symptoms:
            severity_row = severity_df[severity_df['Symptom'] == symptom]
            if not severity_row.empty:
                weight = int(severity_row.iloc[0]['weight'])
                total_score += weight
                symptom_scores.append({
                    'symptom': symptom,
                    'severity': weight
                })
        
        avg_score = total_score / len(symptoms) if symptoms else 0
        
        # Determine severity level
        if avg_score < 3:
            severity_level = 'Mild'
        elif avg_score < 5:
            severity_level = 'Moderate'
        else:
            severity_level = 'Severe'
        
        return jsonify({
            'success': True,
            'total_score': total_score,
            'average_score': round(avg_score, 2),
            'severity_level': severity_level,
            'symptom_scores': symptom_scores
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize models
    print("Initializing models...")
    prepare_disease_model()
    prepare_cancer_model()
    
    print("\n" + "="*50)
    print("Health Assistant API Server")
    print("="*50)
    print("Server starting on http://localhost:5000")
    print("API Endpoints:")
    print("  - GET  /api/symptoms")
    print("  - POST /api/predict-disease")
    print("  - POST /api/predict-cancer")
    print("  - GET  /api/disease-info/<disease>")
    print("  - POST /api/batch-predict")
    print("  - POST /api/severity-score")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
