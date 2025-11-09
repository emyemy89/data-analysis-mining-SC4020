"""
Train and save machine learning models for disease and cancer prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import json

def train_disease_model():
    """Train disease prediction model"""
    print("\n" + "="*60)
    print("TRAINING DISEASE PREDICTION MODEL")
    print("="*60)
    
    # Load data
    print("\n[1] Loading dataset...")
    df = pd.read_csv('dataset_cleaned.csv')
    print(f"✓ Loaded {len(df)} disease-symptom records")
    
    # Get unique symptoms
    print("\n[2] Extracting symptoms...")
    all_symptoms = set()
    for symptoms in df['Symptoms']:
        for symptom in symptoms.split(';'):
            all_symptoms.add(symptom.strip())
    
    symptom_list = sorted(list(all_symptoms))
    print(f"✓ Found {len(symptom_list)} unique symptoms")
    
    # Create feature matrix
    print("\n[3] Creating feature matrix...")
    X = []
    y = []
    
    for _, row in df.iterrows():
        disease = row['Disease']
        symptoms = [s.strip() for s in row['Symptoms'].split(';')]
        
        # Binary encoding: 1 if symptom present, 0 otherwise
        feature_vector = [1 if symptom in symptoms else 0 for symptom in symptom_list]
        X.append(feature_vector)
        y.append(disease)
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"✓ Feature matrix shape: {X.shape}")
    print(f"✓ Number of diseases: {len(set(y))}")
    
    # Encode labels
    print("\n[4] Encoding disease labels...")
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Split data
    print("\n[5] Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    print(f"✓ Training set: {len(X_train)} samples")
    print(f"✓ Testing set: {len(X_test)} samples")
    
    # Train model
    print("\n[6] Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print("✓ Model trained successfully!")
    
    # Evaluate model
    print("\n[7] Evaluating model...")
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"✓ Training Accuracy: {train_score:.2%}")
    print(f"✓ Testing Accuracy: {test_score:.2%}")
    
    # Cross-validation
    print("\n[8] Performing cross-validation...")
    cv_scores = cross_val_score(model, X, y_encoded, cv=5)
    print(f"✓ Cross-validation scores: {cv_scores}")
    print(f"✓ Mean CV score: {cv_scores.mean():.2%} (+/- {cv_scores.std() * 2:.2%})")
    
    # Save model
    print("\n[9] Saving model and artifacts...")
    with open('models/disease_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models/disease_label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    with open('models/symptom_list.pkl', 'wb') as f:
        pickle.dump(symptom_list, f)
    
    print("✓ Model saved to models/disease_model.pkl")
    print("✓ Label encoder saved to models/disease_label_encoder.pkl")
    print("✓ Symptom list saved to models/symptom_list.pkl")
    
    # Save model info
    model_info = {
        'model_type': 'RandomForestClassifier',
        'n_estimators': 100,
        'training_accuracy': float(train_score),
        'testing_accuracy': float(test_score),
        'cv_mean_score': float(cv_scores.mean()),
        'n_symptoms': len(symptom_list),
        'n_diseases': len(label_encoder.classes_),
        'diseases': label_encoder.classes_.tolist()
    }
    
    with open('models/disease_model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print("✓ Model info saved to models/disease_model_info.json")
    
    print("\n" + "="*60)
    print("DISEASE MODEL TRAINING COMPLETE!")
    print("="*60)
    
    return model, label_encoder, symptom_list

def train_cancer_model():
    """Train cancer diagnosis model"""
    print("\n" + "="*60)
    print("TRAINING CANCER DIAGNOSIS MODEL")
    print("="*60)
    
    # Load data
    print("\n[1] Loading cancer dataset...")
    df = pd.read_csv('Cancer_Data.csv')
    print(f"✓ Loaded {len(df)} cancer samples")
    print(f"✓ Malignant: {(df['diagnosis'] == 'M').sum()}")
    print(f"✓ Benign: {(df['diagnosis'] == 'B').sum()}")
    
    # Prepare features
    print("\n[2] Preparing features...")
    X = df.drop(['id', 'diagnosis'], axis=1)
    y = df['diagnosis'].map({'M': 1, 'B': 0})
    
    feature_names = X.columns.tolist()
    print(f"✓ Number of features: {len(feature_names)}")
    
    # Split data
    print("\n[3] Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"✓ Training set: {len(X_train)} samples")
    print(f"✓ Testing set: {len(X_test)} samples")
    
    # Scale features
    print("\n[4] Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("✓ Features scaled successfully!")
    
    # Train model
    print("\n[5] Training Gradient Boosting model...")
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    print("✓ Model trained successfully!")
    
    # Evaluate model
    print("\n[6] Evaluating model...")
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"✓ Training Accuracy: {train_score:.2%}")
    print(f"✓ Testing Accuracy: {test_score:.2%}")
    
    # Detailed evaluation
    y_pred = model.predict(X_test_scaled)
    
    print("\n[7] Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Benign', 'Malignant']))
    
    print("\n[8] Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"True Negatives (Benign): {cm[0][0]}")
    print(f"False Positives: {cm[0][1]}")
    print(f"False Negatives: {cm[1][0]}")
    print(f"True Positives (Malignant): {cm[1][1]}")
    
    # Feature importance
    print("\n[9] Top 10 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_importance.head(10).to_string(index=False))
    
    # Save model
    print("\n[10] Saving model and artifacts...")
    with open('models/cancer_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models/cancer_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    with open('models/cancer_features.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    
    print("✓ Model saved to models/cancer_model.pkl")
    print("✓ Scaler saved to models/cancer_scaler.pkl")
    print("✓ Features saved to models/cancer_features.pkl")
    
    # Save model info
    model_info = {
        'model_type': 'GradientBoostingClassifier',
        'n_estimators': 100,
        'training_accuracy': float(train_score),
        'testing_accuracy': float(test_score),
        'n_features': len(feature_names),
        'feature_names': feature_names,
        'top_features': feature_importance.head(10).to_dict('records')
    }
    
    with open('models/cancer_model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print("✓ Model info saved to models/cancer_model_info.json")
    
    print("\n" + "="*60)
    print("CANCER MODEL TRAINING COMPLETE!")
    print("="*60)
    
    return model, scaler, feature_names

def main():
    """Main training pipeline"""
    import os
    
    # Create models directory
    if not os.path.exists('models'):
        os.makedirs('models')
        print("✓ Created 'models' directory")
    
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "HEALTH ASSISTANT ML PIPELINE" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    
    # Train disease model
    disease_model, disease_encoder, symptoms = train_disease_model()
    
    # Train cancer model
    cancer_model, cancer_scaler, features = train_cancer_model()
    
    print("\n" + "="*60)
    print("ALL MODELS TRAINED SUCCESSFULLY!")
    print("="*60)
    print("\nYou can now run the Flask API server with:")
    print("  python app.py")
    print("\nOr deploy with:")
    print("  gunicorn app:app")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
