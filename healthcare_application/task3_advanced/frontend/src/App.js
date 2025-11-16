import React, { useState, useEffect } from 'react';
import { Activity, AlertCircle, Heart, Stethoscope, Shield, Search, X, ChevronRight, Info, Loader } from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const App = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [activeTab, setActiveTab] = useState('predictor');
  const [loading, setLoading] = useState(false);
  const [allSymptoms, setAllSymptoms] = useState([]);
  const [cancerFeatures, setCancerFeatures] = useState(Array(30).fill(''));
  const [cancerPrediction, setCancerPrediction] = useState(null);
  const [selectedDisease, setSelectedDisease] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [symptomSuggestions, setSymptomSuggestions] = useState([]);

  // Cancer feature names
  const featureNames = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
    'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se', 'fractal_dimension_se',
    'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst',
    'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
  ];

  const featureDescriptions = {
    'radius': 'Distance from center to perimeter points',
    'texture': 'Standard deviation of gray-scale values',
    'perimeter': 'Size of the core tumor',
    'area': 'Area of the tumor',
    'smoothness': 'Local variation in radius lengths',
    'compactness': 'Perimeter² / area - 1.0',
    'concavity': 'Severity of concave portions',
    'concave points': 'Number of concave portions',
    'symmetry': 'Symmetry of the tumor',
    'fractal_dimension': 'Coastline approximation - 1'
  };

  useEffect(() => {
    fetchSymptoms();
  }, []);

  const fetchSymptoms = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/symptoms`);
      const data = await response.json();
      setAllSymptoms(data.symptoms || []);
    } catch (error) {
      console.error('Error fetching symptoms:', error);
      setAllSymptoms(['fever', 'cough', 'headache', 'fatigue', 'nausea']);
    }
  };

  const filteredSymptoms = allSymptoms.filter(symptom =>
    symptom.toLowerCase().replace(/_/g, ' ').includes(searchTerm.toLowerCase())
  );

  const handleSymptomToggle = (symptom) => {
    setSelectedSymptoms(prev =>
      prev.includes(symptom)
        ? prev.filter(s => s !== symptom)
        : [...prev, symptom]
    );
  };

  const toggleSymptom = handleSymptomToggle;

  const predictDisease = async () => {
    if (selectedSymptoms.length === 0) {
      setPrediction({ error: "Please select at least one symptom" });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/predict-disease`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms: selectedSymptoms }),
      });

      const data = await response.json();
      
      if (data.success) {
        setPrediction({ results: data.predictions, selectedCount: data.symptoms_provided });
        
        // Store symptom suggestions from Apriori
        if (data.symptom_suggestions && data.symptom_suggestions.length > 0) {
          setSymptomSuggestions(data.symptom_suggestions);
        } else {
          setSymptomSuggestions([]);
        }
      } else {
        setPrediction({ error: data.error || 'Prediction failed' });
        setSymptomSuggestions([]);
      }
    } catch (error) {
      console.error('Error predicting disease:', error);
      setPrediction({ error: 'Failed to connect to API. Please ensure the backend server is running.' });
    } finally {
      setLoading(false);
    }
  };

  const predictCancer = async () => {
    const features = cancerFeatures.map(f => parseFloat(f) || 0);
    
    if (features.every(f => f === 0)) {
      setCancerPrediction({ error: "Please enter at least some feature values" });
      return;
    }

    await predictCancerWithFeatures(features);
  };

  const handleCancerFeatureChange = (index, value) => {
    const newFeatures = [...cancerFeatures];
    newFeatures[index] = value;
    setCancerFeatures(newFeatures);
  };

  const loadSampleCancerData = (type) => {
    const malignantSample = [17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189];
    const benignSample = [13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766, 0.2699, 0.7886, 2.058, 23.56, 0.008462, 0.0146, 0.02387, 0.01315, 0.0198, 0.0023, 15.11, 19.26, 99.7, 711.2, 0.144, 0.1773, 0.239, 0.1288, 0.2977, 0.07259];
    
    const sampleData = type === 'malignant' ? malignantSample : benignSample;
    setCancerFeatures(sampleData.map(String));
    
    // Automatically predict after loading sample data
    setTimeout(() => {
      predictCancerWithFeatures(sampleData);
    }, 100);
  };

  const handleCSVUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target.result;
        const lines = text.trim().split('\n');
        
        if (lines.length < 2) {
          alert('CSV file must contain a header row and at least one data row');
          return;
        }

        // Parse header and data
        const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
        const values = lines[1].split(',').map(v => v.trim());

        // Create a map of header to value
        const dataMap = {};
        headers.forEach((header, idx) => {
          dataMap[header] = values[idx];
        });

        // Fill in the features based on the feature names
        const newFeatures = featureNames.map(name => {
          const normalizedName = name.toLowerCase().replace(/ /g, '_');
          return dataMap[normalizedName] || dataMap[name.toLowerCase()] || '';
        });

        // Check if we got valid data
        const validCount = newFeatures.filter(f => f !== '').length;
        if (validCount === 0) {
          alert('No matching features found in CSV. Please ensure column names match the feature names (e.g., radius_mean, texture_mean, etc.)');
          return;
        }

        setCancerFeatures(newFeatures);
        alert(`Successfully loaded ${validCount} out of 30 features from CSV`);
        
        // Automatically predict after successful upload
        setTimeout(() => {
          const features = newFeatures.map(f => parseFloat(f) || 0);
          if (!features.every(f => f === 0)) {
            predictCancerWithFeatures(features);
          }
        }, 100);
      } catch (error) {
        console.error('Error parsing CSV:', error);
        alert('Error parsing CSV file. Please ensure it is properly formatted.');
      }
    };

    reader.readAsText(file);
    // Reset file input
    event.target.value = '';
  };

  const predictCancerWithFeatures = async (features) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/predict-cancer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features }),
      });

      const data = await response.json();
      
      if (data.success) {
        setCancerPrediction(data);
      } else {
        setCancerPrediction({ error: data.error || 'Prediction failed' });
      }
    } catch (error) {
      console.error('Error predicting cancer:', error);
      setCancerPrediction({ error: 'Failed to connect to API' });
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setSelectedSymptoms([]);
    setPrediction(null);
    setSearchTerm('');
  };

  const resetCancerForm = () => {
    setCancerFeatures(Array(30).fill(''));
    setCancerPrediction(null);
  };

  const openDiseaseModal = (disease) => {
    setSelectedDisease(disease);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedDisease(null);
  };

  return (
    <div className="min-h-screen bg-gray-50" style={{fontFamily: 'system-ui, -apple-system, sans-serif'}}>
      {/* Header */}
      <div className="bg-white border-b-2 border-gray-300">
        <div className="max-w-7xl mx-auto px-4 py-5">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 p-2.5 rounded-lg" style={{transform: 'rotate(-2deg)'}}>
                <Activity className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Medical Symptom Checker
                </h1>
                <p className="text-sm text-gray-600">Quick diagnosis helper</p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setActiveTab('predictor')}
                className={`px-4 py-2 rounded border-2 font-medium ${
                  activeTab === 'predictor'
                    ? 'bg-blue-600 text-white border-blue-700'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-blue-400'
                }`}
              >
                Disease Checker
              </button>
              <button
                onClick={() => setActiveTab('cancer')}
                className={`px-4 py-2 rounded border-2 font-medium ${
                  activeTab === 'cancer'
                    ? 'bg-blue-600 text-white border-blue-700'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-blue-400'
                }`}
              >
                Cancer Analysis
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'predictor' ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Disease Prediction Interface */}
            <div className="lg:col-span-2">
              <div className="bg-white border-2 border-gray-300 rounded-lg p-5">
                <div className="flex items-center justify-between mb-5">
                  <h2 className="text-lg font-bold text-gray-900">
                    What symptoms do you have?
                  </h2>
                  <span className="bg-gray-200 text-gray-700 px-2.5 py-1 rounded text-sm">
                    {selectedSymptoms.length} selected
                  </span>
                </div>

                <div className="relative mb-4">
                  <input
                    type="text"
                    placeholder="Type to search symptoms"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full px-3 py-2.5 border-2 border-gray-300 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>

                {selectedSymptoms.length > 0 && (
                  <div className="mb-4 p-3 bg-yellow-50 border-l-4 border-yellow-400">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-semibold text-gray-800">Selected:</span>
                      <button
                        onClick={() => setSelectedSymptoms([])}
                        className="text-xs text-gray-600 hover:text-gray-900 underline"
                      >
                        clear all
                      </button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {selectedSymptoms.map(symptom => (
                        <span
                          key={symptom}
                          className="bg-white border border-gray-300 px-2.5 py-1 rounded text-sm text-gray-800 flex items-center gap-1.5"
                        >
                          {symptom.replace(/_/g, ' ')}
                          <button
                            onClick={() => toggleSymptom(symptom)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="max-h-96 overflow-y-auto pr-2">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {filteredSymptoms.map(symptom => (
                      <button
                        key={symptom}
                        onClick={() => toggleSymptom(symptom)}
                        className={`p-2.5 rounded border-2 text-left transition-colors ${
                          selectedSymptoms.includes(symptom)
                            ? 'bg-blue-600 text-white border-blue-700'
                            : 'bg-white hover:bg-gray-50 text-gray-700 border-gray-300'
                        }`}
                      >
                        <span className="text-sm">
                          {symptom.replace(/_/g, ' ')}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex gap-2 mt-5">
                  <button
                    onClick={predictDisease}
                    disabled={selectedSymptoms.length === 0 || loading}
                    className="flex-1 bg-blue-600 text-white py-2.5 rounded font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 border-b-4 border-blue-800 disabled:border-gray-500"
                  >
                    {loading ? (
                      <>
                        <Loader className="w-4 h-4 animate-spin" />
                        Checking...
                      </>
                    ) : (
                      'Check Symptoms'
                    )}
                  </button>
                  <button
                    onClick={resetForm}
                    className="px-5 py-2.5 bg-white border-2 border-gray-300 text-gray-700 rounded font-semibold hover:border-gray-400"
                  >
                    Reset
                  </button>
                </div>
              </div>
            </div>

            {/* Results Panel */}
            <div className="lg:col-span-1">
              <div className="bg-white border-2 border-gray-300 rounded-lg p-5 sticky top-6">
                <h2 className="text-lg font-bold text-gray-900 mb-4 pb-2 border-b-2 border-gray-200">
                  Results
                </h2>

                {!prediction ? (
                  <div className="text-center py-10">
                    <div className="text-5xl mb-3">🩺</div>
                    <p className="text-gray-600 text-sm">
                      Select symptoms and check to see possible conditions
                    </p>
                  </div>
                ) : prediction.error ? (
                  <div className="bg-red-50 border-l-4 border-red-500 p-3">
                    <p className="text-red-700 text-sm font-medium">{prediction.error}</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {/* Symptom Suggestions from Apriori */}
                    {symptomSuggestions.length > 0 && (
                      <div className="bg-green-50 border-2 border-green-200 rounded-xl p-4 mb-4">
                        <h3 className="text-sm font-bold text-green-900 mb-2 flex items-center gap-2">
                          <Search className="w-4 h-4" />
                          Related Symptoms
                        </h3>
                        <p className="text-xs text-green-700 mb-2">
                          Based on your selected symptoms, you may also experience:
                        </p>
                        <div className="space-y-2">
                          {symptomSuggestions.map((suggestion, idx) => (
                            <div key={idx} className="flex items-center justify-between bg-white rounded-lg p-2">
                              <div>
                                <div className="text-sm font-medium text-gray-800">{suggestion.symptom}</div>
                                <div className="text-xs text-gray-500">
                                  Confidence: {(suggestion.confidence * 100).toFixed(1)}%
                                </div>
                              </div>
                              {!selectedSymptoms.includes(suggestion.symptom) && (
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleSymptomToggle(suggestion.symptom);
                                  }}
                                  className="text-xs bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600"
                                >
                                  Add
                                </button>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <div className="max-h-[600px] overflow-y-auto space-y-4">
                    {prediction.results?.map((result, index) => (
                      <div
                        key={result.disease}
                        onClick={() => openDiseaseModal(result)}
                        className="border-2 border-gray-300 rounded p-3 hover:border-blue-500 hover:bg-gray-50 cursor-pointer"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              {index === 0 && (
                                <span className="bg-yellow-400 text-black text-xs px-1.5 py-0.5 rounded font-bold">
                                  #1
                                </span>
                              )}
                              <h3 className="font-bold text-gray-900">{result.disease}</h3>
                            </div>
                            <p className="text-xs text-gray-600 mb-2 line-clamp-2">
                              {result.description?.substring(0, 100)}...
                            </p>
                          </div>
                          <span className="text-gray-400 text-sm ml-2">→</span>
                        </div>

                        <div className="mb-2">
                          <div className="flex justify-between text-xs text-gray-600 mb-1">
                            <span>Match</span>
                            <span className="font-bold">{result.confidence}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded h-2">
                            <div
                              className="bg-blue-600 h-2 rounded"
                              style={{ width: `${result.confidence}%` }}
                            />
                          </div>
                        </div>

                        <div className="text-xs text-blue-600 font-medium">
                          Click for details
                        </div>
                      </div>
                    ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : activeTab === 'cancer' ? (
          // Cancer Prediction Interface
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Heart className="w-6 h-6 text-red-500" />
                Cancer Diagnosis Prediction
              </h2>
              
              <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4 mb-6">
                <p className="text-sm text-yellow-800 mb-3">
                  Enter 30 tumor feature measurements from medical imaging. Use the sample buttons or upload a CSV file.
                </p>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => loadSampleCancerData('malignant')}
                    className="px-3 py-1.5 bg-red-100 text-red-700 rounded-lg text-sm font-medium hover:bg-red-200"
                  >
                    Load Malignant Sample
                  </button>
                  <button
                    onClick={() => loadSampleCancerData('benign')}
                    className="px-3 py-1.5 bg-green-100 text-green-700 rounded-lg text-sm font-medium hover:bg-green-200"
                  >
                    Load Benign Sample
                  </button>
                  <label className="px-3 py-1.5 bg-blue-100 text-blue-700 rounded-lg text-sm font-medium hover:bg-blue-200 cursor-pointer inline-flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    Upload CSV
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleCSVUpload}
                      className="hidden"
                    />
                  </label>
                </div>
                <p className="text-xs text-gray-600 mt-2">
                  CSV format: First row = column names (radius_mean, texture_mean, etc.), Second row = values
                </p>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6 max-h-96 overflow-y-auto p-2">
                {featureNames.map((name, i) => (
                  <div key={i}>
                    <label className="text-xs font-medium text-gray-700 mb-1 block" title={name}>
                      {name.replace(/_/g, ' ')}
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={cancerFeatures[i]}
                      onChange={(e) => handleCancerFeatureChange(i, e.target.value)}
                      className="w-full px-3 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none text-sm"
                      placeholder="0.00"
                    />
                  </div>
                ))}
              </div>

              {/* Feature Legend */}
              <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-xl">
                <h3 className="text-sm font-bold text-blue-900 mb-3 flex items-center gap-2">
                  <Info className="w-4 h-4" />
                  Feature Descriptions
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                  {Object.entries(featureDescriptions).map(([key, desc]) => (
                    <div key={key} className="flex gap-2">
                      <span className="font-semibold text-blue-800 min-w-[120px]">{key}:</span>
                      <span className="text-gray-700">{desc}</span>
                    </div>
                  ))}
                </div>
                <div className="mt-3 pt-3 border-t border-blue-200 text-xs text-gray-600">
                  <strong>Note:</strong> Features are grouped as: <span className="font-mono bg-white px-1 rounded">_mean</span> (average values), 
                  <span className="font-mono bg-white px-1 rounded ml-1">_se</span> (standard errors), 
                  <span className="font-mono bg-white px-1 rounded ml-1">_worst</span> (largest/worst values)
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={predictCancer}
                  disabled={loading}
                  className="flex-1 bg-red-600 text-white py-3 rounded font-semibold hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 border-b-4 border-red-800 disabled:border-gray-500"
                >
                  {loading ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Heart className="w-5 h-5" />
                      Predict Diagnosis
                    </>
                  )}
                </button>
                <button
                  onClick={resetCancerForm}
                  className="px-6 py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-all"
                >
                  Reset
                </button>
              </div>

              {cancerPrediction && !cancerPrediction.error && (
                <div className="mt-6 p-5 bg-gray-50 rounded border-2 border-gray-300">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">Diagnosis Result</h3>
                  
                  <div className={`p-4 rounded-lg mb-4 ${
                    cancerPrediction.diagnosis === 'Malignant' 
                      ? 'bg-red-100 border-2 border-red-300' 
                      : 'bg-green-100 border-2 border-green-300'
                  }`}>
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-bold">
                        {cancerPrediction.diagnosis}
                      </span>
                      <span className="text-sm font-semibold">
                        {cancerPrediction.confidence}% confidence
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="p-3 bg-white rounded-lg">
                      <div className="text-xs text-gray-600 mb-1">Benign Probability</div>
                      <div className="text-lg font-bold text-green-600">
                        {cancerPrediction.probabilities?.benign}%
                      </div>
                    </div>
                    <div className="p-3 bg-white rounded-lg">
                      <div className="text-xs text-gray-600 mb-1">Malignant Probability</div>
                      <div className="text-lg font-bold text-red-600">
                        {cancerPrediction.probabilities?.malignant}%
                      </div>
                    </div>
                  </div>

                  {/* Pattern Analysis Section */}
                  {cancerPrediction.pattern_analysis && (
                    <div className="mt-4 border-t-2 border-blue-200 pt-4">
                      <h4 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                        <Activity className="w-5 h-5 text-purple-600" />
                        Sequential Pattern Analysis
                      </h4>
                      
                      {/* Pattern Detection Summary */}
                      <div className="grid grid-cols-3 gap-3 mb-4">
                        <div className="p-3 bg-red-50 rounded-lg border border-red-200">
                          <div className="text-xs text-red-600 font-medium mb-1">Malignant Patterns</div>
                          <div className="text-2xl font-bold text-red-700">
                            {cancerPrediction.pattern_analysis.malignant_patterns_detected}
                          </div>
                        </div>
                        <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                          <div className="text-xs text-green-600 font-medium mb-1">Benign Patterns</div>
                          <div className="text-2xl font-bold text-green-700">
                            {cancerPrediction.pattern_analysis.benign_patterns_detected}
                          </div>
                        </div>
                        <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                          <div className="text-xs text-purple-600 font-medium mb-1">Agreement</div>
                          <div className="text-xl font-bold text-purple-700">
                            {cancerPrediction.pattern_analysis.agreement_with_model ? '✓ Yes' : '✗ No'}
                          </div>
                        </div>
                      </div>

                      {/* Pattern Scores */}
                      <div className="mb-4 p-3 bg-white rounded-lg border border-gray-200">
                        <div className="text-sm font-medium text-gray-700 mb-2">Pattern Risk Scores</div>
                        <div className="flex items-center gap-4">
                          <div className="flex-1">
                            <div className="flex justify-between text-xs mb-1">
                              <span className="text-red-600 font-medium">Malignant</span>
                              <span className="font-bold">{cancerPrediction.pattern_analysis.malignant_score}</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-red-500 h-2 rounded-full transition-all"
                                style={{width: `${Math.min(100, cancerPrediction.pattern_analysis.malignant_score * 200)}%`}}
                              ></div>
                            </div>
                          </div>
                          <div className="flex-1">
                            <div className="flex justify-between text-xs mb-1">
                              <span className="text-green-600 font-medium">Benign</span>
                              <span className="font-bold">{cancerPrediction.pattern_analysis.benign_score}</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-green-500 h-2 rounded-full transition-all"
                                style={{width: `${Math.min(100, cancerPrediction.pattern_analysis.benign_score * 200)}%`}}
                              ></div>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Explanation */}
                      <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                        <pre className="text-xs font-mono whitespace-pre-wrap text-gray-700 leading-relaxed">
                          {cancerPrediction.pattern_analysis.explanation}
                        </pre>
                      </div>

                      {/* Top Patterns Detected */}
                      {cancerPrediction.top_patterns && (
                        <div className="mt-4">
                          <div className="text-sm font-bold text-gray-700 mb-2">Top Detected Patterns:</div>
                          
                          {cancerPrediction.top_patterns.top_malignant_patterns?.length > 0 && (
                            <div className="mb-3">
                              <div className="text-xs font-semibold text-red-600 mb-1">🔴 Malignant Indicators:</div>
                              <div className="space-y-1">
                                {cancerPrediction.top_patterns.top_malignant_patterns.map((p, idx) => (
                                  <div key={idx} className="text-xs bg-red-50 px-2 py-1 rounded border border-red-200">
                                    {p.pattern.join(' → ')} (strength: {p.strength.toFixed(3)})
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {cancerPrediction.top_patterns.top_benign_patterns?.length > 0 && (
                            <div>
                              <div className="text-xs font-semibold text-green-600 mb-1">🟢 Benign Indicators:</div>
                              <div className="space-y-1">
                                {cancerPrediction.top_patterns.top_benign_patterns.map((p, idx) => (
                                  <div key={idx} className="text-xs bg-green-50 px-2 py-1 rounded border border-green-200">
                                    {p.pattern.join(' → ')} (strength: {p.strength.toFixed(3)})
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}

              {cancerPrediction?.error && (
                <div className="mt-6 bg-red-50 border-2 border-red-200 rounded-xl p-4">
                  <p className="text-red-700 text-sm">{cancerPrediction.error}</p>
                </div>
              )}
            </div>
          </div>
        ) : (
          // About Tab
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-6">About Health Assistant Pro</h2>
              
              <div className="space-y-6 text-gray-700">
                <div>
                  <h3 className="text-xl font-semibold text-blue-600 mb-3">What is this?</h3>
                  <p className="leading-relaxed">
                    Health Assistant Pro is an AI-powered medical analysis system that predicts diseases from symptoms and analyzes tumor features for cancer diagnosis. It combines machine learning with healthcare data mining.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-purple-600 mb-3">Features</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex items-start gap-3">
                      <div className="bg-blue-100 p-2 rounded-lg">
                        <Activity className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold">Disease Prediction</h4>
                        <p className="text-sm text-gray-600">Predict from 130+ symptoms, 40+ diseases</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="bg-purple-100 p-2 rounded-lg">
                        <Heart className="w-5 h-5 text-purple-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold">Cancer Diagnosis</h4>
                        <p className="text-sm text-gray-600">Breast cancer classification with 96%+ accuracy</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-3">Technology Stack</h3>
                  <ul className="list-disc list-inside space-y-2 text-sm">
                    <li>Backend: Flask REST API with Python</li>
                    <li>Frontend: React with Tailwind CSS</li>
                    <li>ML Models: Random Forest, Gradient Boosting</li>
                    <li>Datasets: Wisconsin Breast Cancer, Disease-Symptom Database</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>Medical Symptom Checker © 2025</p>
        </div>
      </div>

      {/* Disease Details Modal */}
      {showModal && selectedDisease && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={closeModal}>
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className="sticky top-0 bg-blue-600 text-white p-5 rounded-t-lg border-b-2 border-blue-700">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Stethoscope className="w-6 h-6" />
                    <h2 className="text-2xl font-bold">{selectedDisease.disease}</h2>
                  </div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <div className="bg-white bg-opacity-20 px-3 py-1 rounded-full text-sm font-medium">
                      Confidence: {selectedDisease.confidence}%
                    </div>
                    {selectedDisease.apriori_boost > 0 && (
                      <div className="bg-green-500 bg-opacity-30 px-3 py-1 rounded-full text-sm font-medium">
                        +{selectedDisease.apriori_boost}% Pattern Match
                      </div>
                    )}
                  </div>
                </div>
                <button
                  onClick={closeModal}
                  className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2 transition-all"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
            </div>

            {/* Modal Body */}
            <div className="p-6 space-y-6">
              {/* Confidence Bar with Apriori Breakdown */}
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span className="font-semibold">Prediction Confidence</span>
                  <span className="font-bold text-blue-600">{selectedDisease.confidence}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-blue-600 h-3 rounded"
                    style={{ width: `${selectedDisease.confidence}%` }}
                  />
                </div>
                {selectedDisease.base_confidence && selectedDisease.apriori_boost !== undefined && (
                  <div className="mt-2 text-xs text-gray-600 space-y-1">
                    <div>Base Model: {selectedDisease.base_confidence}%</div>
                    <div className="text-green-600">Apriori Pattern Boost: +{selectedDisease.apriori_boost}%</div>
                    <div className="text-blue-600 font-medium">Enhanced Score: {selectedDisease.confidence}%</div>
                  </div>
                )}
              </div>

              {/* Description */}
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
                <h3 className="text-lg font-bold text-gray-800 mb-2 flex items-center gap-2">
                  <Info className="w-5 h-5 text-blue-600" />
                  Description
                </h3>
                <p className="text-gray-700 leading-relaxed">
                  {selectedDisease.description || 'No description available.'}
                </p>
              </div>

              {/* Precautions */}
              {selectedDisease.precautions && selectedDisease.precautions.length > 0 && (
                <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded-r-lg">
                  <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                    <Shield className="w-5 h-5 text-green-600" />
                    Recommended Precautions
                  </h3>
                  <ul className="space-y-2">
                    {selectedDisease.precautions.map((precaution, i) => (
                      <li key={i} className="flex items-start gap-3 text-gray-700">
                        <div className="bg-green-500 text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5 font-bold text-sm">
                          {i + 1}
                        </div>
                        <span className="flex-1">{precaution}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Warning */}
              <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded-r-lg">
                <h3 className="text-lg font-bold text-gray-800 mb-2 flex items-center gap-2">
                  <AlertCircle className="w-5 h-5 text-yellow-600" />
                  Important Notice
                </h3>
                <p className="text-gray-700 text-sm">
                  This is an AI-generated prediction for informational purposes only. It is NOT a medical diagnosis. 
                  Please consult with a qualified healthcare professional for proper diagnosis and treatment.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 pt-4 border-t">
                <button
                  onClick={closeModal}
                  className="flex-1 bg-blue-600 text-white py-3 rounded font-semibold hover:bg-blue-700 border-b-4 border-blue-800"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
