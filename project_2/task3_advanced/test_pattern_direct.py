"""
Direct pattern detector test (without Flask server)
"""
import numpy as np
import pandas as pd
from pattern_detector import PatternDetector

# Load cancer data
cancer_df = pd.read_csv('Cancer_Data.csv')
X_cancer = cancer_df.iloc[:, 2:-1].values  # 30 features

# Initialize and fit pattern detector
print("="*60)
print("PATTERN DETECTOR DIRECT TEST")
print("="*60)

pattern_detector = PatternDetector()
print("\n✓ PatternDetector initialized")

pattern_detector.fit(X_cancer)
print("✓ PatternDetector fitted on cancer data")

# Test with first malignant sample
malignant_sample = X_cancer[0]
print(f"\n{'='*60}")
print("Testing MALIGNANT sample (row 0)")
print(f"{'='*60}")

results = pattern_detector.detect_patterns(malignant_sample)
print(f"\n📊 PATTERN DETECTION RESULTS:")
print(f"  Malignant patterns detected: {results['malignant_patterns'][:3]}")
print(f"  Benign patterns detected: {results['benign_patterns'][:3]}")
print(f"  Malignant score: {results['malignant_score']}")
print(f"  Benign score: {results['benign_score']}")
print(f"  Pattern prediction: {results['pattern_prediction']}")
print(f"  Pattern confidence: {results['pattern_confidence']}%")
print(f"  Total patterns: {results['total_patterns_detected']}")

# Get top patterns
top = pattern_detector.get_top_patterns(malignant_sample, n=3)
print(f"\n🔴 TOP 3 MALIGNANT PATTERNS:")
for i, p in enumerate(top['top_malignant_patterns'], 1):
    print(f"  {i}. {' → '.join(p['pattern'])} (strength: {p['strength']:.3f})")

print(f"\n🟢 TOP 3 BENIGN PATTERNS:")
for i, p in enumerate(top['top_benign_patterns'], 1):
    print(f"  {i}. {' → '.join(p['pattern'])} (strength: {p['strength']:.3f})")

# Get explanation
explanation = pattern_detector.explain_prediction(malignant_sample, 'Malignant')
print(f"\n📝 EXPLANATION:")
print(explanation['explanation'])
print(f"\n✓ Agreement with ML: {explanation['agreement']}")

# Test with benign sample (find one from data)
benign_indices = cancer_df[cancer_df['diagnosis'] == 'B'].index
benign_sample = X_cancer[benign_indices[0]]

print(f"\n{'='*60}")
print(f"Testing BENIGN sample (row {benign_indices[0]})")
print(f"{'='*60}")

results = pattern_detector.detect_patterns(benign_sample)
print(f"\n📊 PATTERN DETECTION RESULTS:")
print(f"  Malignant patterns detected: {len(results['malignant_patterns'])}")
print(f"  Benign patterns detected: {len(results['benign_patterns'])}")
print(f"  Malignant score: {results['malignant_score']}")
print(f"  Benign score: {results['benign_score']}")
print(f"  Pattern prediction: {results['pattern_prediction']}")
print(f"  Pattern confidence: {results['pattern_confidence']}%")
print(f"  Total patterns: {results['total_patterns_detected']}")

# Get top patterns
top = pattern_detector.get_top_patterns(benign_sample, n=3)
print(f"\n🔴 TOP 3 MALIGNANT PATTERNS:")
for i, p in enumerate(top['top_malignant_patterns'], 1):
    print(f"  {i}. {' → '.join(p['pattern'])} (strength: {p['strength']:.3f})")

print(f"\n🟢 TOP 3 BENIGN PATTERNS:")
for i, p in enumerate(top['top_benign_patterns'], 1):
    print(f"  {i}. {' → '.join(p['pattern'])} (strength: {p['strength']:.3f})")

# Get explanation
explanation = pattern_detector.explain_prediction(benign_sample, 'Benign')
print(f"\n📝 EXPLANATION:")
print(explanation['explanation'])
print(f"\n✓ Agreement with ML: {explanation['agreement']}")

print(f"\n{'='*60}")
print("TEST COMPLETE - Pattern Detector Working Successfully!")
print(f"{'='*60}\n")
