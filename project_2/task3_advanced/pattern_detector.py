"""
Sequential Pattern Detection Module for Cancer Diagnosis
Uses GSP (Generalized Sequential Pattern) mining results from Task 2
"""

import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
import pandas as pd

# Cancer feature names (30 features from Cancer_Data.csv)
CANCER_FEATURES = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
    'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se', 'fractal_dimension_se',
    'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst',
    'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

# Top discriminative patterns from Task 2 GSP (quantile binning)
# Format: (pattern_items, benign_support, malignant_support)

MALIGNANT_PATTERNS = [
    # Strong malignant indicators (M >> B)
    (['high_area_mean', 'high_perimeter_mean'], 0.00, 0.23),
    (['high_radius_worst', 'high_perimeter_mean'], 0.00, 0.20),
    (['high_area_worst', 'high_perimeter_mean'], 0.00, 0.18),
    (['high_area_mean', 'high_radius_mean'], 0.00, 0.17),
    (['high_area_mean', 'high_radius_worst'], 0.00, 0.17),
    (['high_radius_se', 'high_area_se'], 0.00, 0.16),
    (['high_area_worst', 'high_radius_mean'], 0.00, 0.16),
    (['high_perimeter_worst', 'high_perimeter_mean'], 0.00, 0.14),
    (['high_area_worst', 'high_radius_worst'], 0.00, 0.14),
    (['high_concavity_mean', 'high_concave points_mean'], 0.00, 0.13),
    (['high_concave points_mean', 'high_perimeter_worst'], 0.00, 0.12),
    (['high_perimeter_worst', 'high_radius_mean'], 0.00, 0.12),
    (['high_area_worst', 'high_radius_mean', 'high_perimeter_mean'], 0.00, 0.11),
    (['high_concave points_mean', 'high_perimeter_mean'], 0.00, 0.11),
    (['high_perimeter_worst', 'high_concave points_worst'], 0.00, 0.11),
    (['high_symmetry_worst', 'high_symmetry_mean'], 0.00, 0.11),
    (['high_area_mean', 'high_radius_mean', 'high_perimeter_mean'], 0.00, 0.11),
    (['high_concave points_mean', 'high_radius_worst'], 0.00, 0.11),
]

BENIGN_PATTERNS = [
    # Strong benign indicators (B >> M)
    (['high_radius_mean', 'high_perimeter_worst'], 0.14, 0.00),
    (['high_perimeter_mean', 'high_perimeter_worst'], 0.13, 0.00),
    (['high_perimeter_mean', 'high_radius_worst'], 0.13, 0.00),
    (['high_texture_mean', 'high_texture_worst'], 0.12, 0.00),
    (['high_perimeter_mean', 'high_area_mean'], 0.12, 0.00),
    (['high_radius_mean', 'high_area_mean'], 0.12, 0.00),
    (['high_smoothness_worst', 'high_compactness_mean'], 0.12, 0.00),
    (['high_radius_worst', 'high_area_mean'], 0.11, 0.00),
    (['high_texture_worst', 'high_texture_se'], 0.11, 0.00),
    (['high_concave points_worst', 'high_concave points_mean'], 0.10, 0.00),
    (['high_texture_mean', 'high_texture_se'], 0.10, 0.00),
    (['high_radius_mean', 'high_perimeter_mean', 'high_radius_worst'], 0.10, 0.00),
    (['high_radius_mean', 'high_perimeter_mean', 'high_perimeter_worst'], 0.10, 0.00),
    (['high_concavity_worst', 'high_concavity_mean'], 0.10, 0.00),
]

class PatternDetector:
    """Detects sequential patterns in cancer feature data"""
    
    def __init__(self):
        # Initialize KBinsDiscretizer with quantile strategy (same as Task 2)
        self.discretizer = KBinsDiscretizer(
            n_bins=3, 
            encode='ordinal', 
            strategy='quantile'
        )
        self.bin_labels = {0: "low", 1: "medium", 2: "high"}
        self.is_fitted = False
        
    def fit(self, X):
        """Fit the discretizer on training data
        
        Args:
            X: numpy array of shape (n_samples, 30) with cancer features
        """
        self.discretizer.fit(X)
        self.is_fitted = True
        
    def discretize_features(self, features):
        """Convert continuous features to discrete bins
        
        Args:
            features: array of 30 continuous cancer feature values
            
        Returns:
            dict mapping feature names to bin labels (low/medium/high)
        """
        if not self.is_fitted:
            raise ValueError("PatternDetector must be fitted before use")
            
        # Reshape to 2D array for sklearn
        features_array = np.array(features).reshape(1, -1)
        
        # Discretize
        binned = self.discretizer.transform(features_array)[0]
        
        # Create labeled feature dictionary
        labeled_features = {}
        for i, feature_name in enumerate(CANCER_FEATURES):
            bin_idx = int(binned[i])
            bin_label = self.bin_labels[bin_idx]
            labeled_features[feature_name] = f"{bin_label}_{feature_name}"
            
        return labeled_features
        
    def detect_patterns(self, features):
        """Detect malignant and benign patterns in feature data
        
        Args:
            features: array of 30 continuous cancer feature values
            
        Returns:
            dict with pattern detection results
        """
        # Discretize features
        labeled_features = self.discretize_features(features)
        feature_set = set(labeled_features.values())
        
        # Check for malignant patterns
        malignant_matches = []
        for pattern, b_sup, m_sup in MALIGNANT_PATTERNS:
            if all(item in feature_set for item in pattern):
                malignant_matches.append({
                    'pattern': pattern,
                    'support_benign': b_sup,
                    'support_malignant': m_sup,
                    'strength': m_sup - b_sup
                })
        
        # Check for benign patterns
        benign_matches = []
        for pattern, b_sup, m_sup in BENIGN_PATTERNS:
            if all(item in feature_set for item in pattern):
                benign_matches.append({
                    'pattern': pattern,
                    'support_benign': b_sup,
                    'support_malignant': m_sup,
                    'strength': b_sup - m_sup
                })
        
        # Calculate pattern-based risk scores
        malignant_score = sum(m['strength'] for m in malignant_matches)
        benign_score = sum(b['strength'] for b in benign_matches)
        
        # Pattern-based prediction
        pattern_prediction = 'Malignant' if malignant_score > benign_score else 'Benign'
        pattern_confidence = max(malignant_score, benign_score) / (malignant_score + benign_score + 1e-6)
        
        return {
            'malignant_patterns': malignant_matches,
            'benign_patterns': benign_matches,
            'malignant_score': round(float(malignant_score), 3),
            'benign_score': round(float(benign_score), 3),
            'pattern_prediction': pattern_prediction,
            'pattern_confidence': round(float(pattern_confidence * 100), 2),
            'total_patterns_detected': len(malignant_matches) + len(benign_matches),
            'discretized_features': labeled_features
        }
    
    def get_top_patterns(self, features, n=5):
        """Get top N most significant patterns detected
        
        Args:
            features: array of 30 continuous cancer feature values
            n: number of top patterns to return
            
        Returns:
            dict with top patterns for both categories
        """
        results = self.detect_patterns(features)
        
        # Sort by strength
        top_malignant = sorted(
            results['malignant_patterns'], 
            key=lambda x: x['strength'], 
            reverse=True
        )[:n]
        
        top_benign = sorted(
            results['benign_patterns'], 
            key=lambda x: x['strength'], 
            reverse=True
        )[:n]
        
        return {
            'top_malignant_patterns': top_malignant,
            'top_benign_patterns': top_benign,
            'malignant_score': results['malignant_score'],
            'benign_score': results['benign_score'],
            'dominant_category': results['pattern_prediction']
        }
    
    def explain_prediction(self, features, model_prediction):
        """Generate human-readable explanation of pattern analysis
        
        Args:
            features: array of 30 continuous cancer feature values
            model_prediction: prediction from the ML model ('Malignant' or 'Benign')
            
        Returns:
            dict with explanation text and agreement status
        """
        pattern_results = self.detect_patterns(features)
        pattern_pred = pattern_results['pattern_prediction']
        
        agreement = (model_prediction == pattern_pred)
        
        explanation = []
        
        if pattern_results['total_patterns_detected'] == 0:
            explanation.append("⚠️ No strong discriminative patterns detected.")
            explanation.append("Prediction relies primarily on ML model.")
        else:
            explanation.append(f"📊 Detected {pattern_results['total_patterns_detected']} sequential patterns:")
            explanation.append(f"   • {len(pattern_results['malignant_patterns'])} malignant indicators")
            explanation.append(f"   • {len(pattern_results['benign_patterns'])} benign indicators")
            
            explanation.append(f"\n🔍 Pattern Analysis:")
            explanation.append(f"   • Malignant risk score: {pattern_results['malignant_score']:.3f}")
            explanation.append(f"   • Benign risk score: {pattern_results['benign_score']:.3f}")
            explanation.append(f"   • Pattern-based prediction: {pattern_pred}")
            
            if agreement:
                explanation.append(f"\n✅ Pattern analysis AGREES with ML model prediction ({model_prediction})")
            else:
                explanation.append(f"\n⚠️ Pattern analysis DISAGREES with ML model:")
                explanation.append(f"   • ML Model: {model_prediction}")
                explanation.append(f"   • Patterns suggest: {pattern_pred}")
                explanation.append("   • Consider additional clinical evaluation")
        
        return {
            'agreement': agreement,
            'explanation': '\n'.join(explanation),
            'pattern_prediction': pattern_pred,
            'model_prediction': model_prediction
        }
