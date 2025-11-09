import React, { useState, useEffect } from 'react';
import { Activity, AlertCircle, Heart, Stethoscope, Shield, Search, X, ChevronRight, Info, Loader } from 'lucide-react';

const API_BASE_URL = 'http://localhost:5000/api';

const App = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [activeTab, setActiveTab] = useState('predictor');
  const [loading, setLoading] = useState(false);
  const [allSymptoms, setAllSymptoms] = useState([]);
  const [cancerFeatures, setCancerFeatures] = useState(Array(30).fill(''));
  const [cancerPrediction, setCancerPrediction] = useState(null);

  // Fetch symptoms from API on mount
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
      // Fallback to some common symptoms if API fails
      setAllSymptoms([
        'fever', 'cough', 'headache', 'fatigue', 'nausea',
        'vomiting', 'diarrhea', 'chest_pain', 'back_pain'
      ]);
    }
  };

  const filteredSymptoms = allSymptoms.filter(symptom =>
    symptom.toLowerCase().replace(/_/g, ' ').includes(searchTerm.toLowerCase())
  );

  const toggleSymptom = (symptom) => {
    setSelectedSymptoms(prev =>
      prev.includes(symptom)
        ? prev.filter(s => s !== symptom)
        : [...prev, symptom]
    );
  };

  const predictDisease = async () => {
    if (selectedSymptoms.length === 0) {
      setPrediction({ error: "Please select at least one symptom" });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/predict-disease`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symptoms: selectedSymptoms }),
      });

      const data = await response.json();
      
      if (data.success) {
        setPrediction({
          results: data.predictions,
          selectedCount: data.symptoms_provided
        });
      } else {
        setPrediction({ error: data.error || 'Prediction failed' });
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

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/predict-cancer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
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

  const handleCancerFeatureChange = (index, value) => {
    const newFeatures = [...cancerFeatures];
    newFeatures[index] = value;
    setCancerFeatures(newFeatures);
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-xl">
                <Activity className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Health Assistant Pro
                </h1>
                <p className="text-sm text-gray-500">AI-Powered Medical Analysis</p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setActiveTab('predictor')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  activeTab === 'predictor'
                    ? 'bg-blue-500 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <Stethoscope className="w-4 h-4 inline mr-2" />
                Disease Predictor
              </button>
              <button
                onClick={() => setActiveTab('cancer')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  activeTab === 'cancer'
                    ? 'bg-blue-500 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <Heart className="w-4 h-4 inline mr-2" />
                Cancer Diagnosis
              </button>
              <button
                onClick={() => setActiveTab('info')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  activeTab === 'info'
                    ? 'bg-blue-500 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <Info className="w-4 h-4 inline mr-2" />
                About
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
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                    <Search className="w-5 h-5 text-blue-500" />
                    Select Your Symptoms
                  </h2>
                  <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">
                    {selectedSymptoms.length} selected
                  </span>
                </div>

                <div className="relative mb-4">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search symptoms..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
                  />
                </div>

                {selectedSymptoms.length > 0 && (
                  <div className="mb-4 p-4 bg-blue-50 rounded-xl">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-blue-900">Selected Symptoms:</span>
                      <button
                        onClick={() => setSelectedSymptoms([])}
                        className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                      >
                        Clear All
                      </button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {selectedSymptoms.map(symptom => (
                        <span
                          key={symptom}
                          className="bg-white px-3 py-1.5 rounded-lg text-sm font-medium text-gray-700 flex items-center gap-2 shadow-sm"
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
                        className={`p-3 rounded-xl text-left transition-all ${
                          selectedSymptoms.includes(symptom)
                            ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-md'
                            : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                        }`}
                      >
                        <span className="text-sm font-medium">
                          {symptom.replace(/_/g, ' ')}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex gap-3 mt-6">
                  <button
                    onClick={predictDisease}
                    disabled={selectedSymptoms.length === 0 || loading}
                    className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-xl font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <>
                        <Loader className="w-5 h-5 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Heart className="w-5 h-5" />
                        Predict Disease
                      </>
                    )}
                  </button>
                  <button
                    onClick={resetForm}
                    className="px-6 py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-all"
                  >
                    Reset
                  </button>
                </div>
              </div>
            </div>

            {/* Results Panel */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <AlertCircle className="w-5 h-5 text-purple-500" />
                  Prediction Results
                </h2>

                {!prediction ? (
                  <div className="text-center py-12">
                    <div className="w-20 h-20 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Stethoscope className="w-10 h-10 text-blue-500" />
                    </div>
                    <p className="text-gray-500 text-sm">
                      Select symptoms and click "Predict Disease" to see results
                    </p>
                  </div>
                ) : prediction.error ? (
                  <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
                    <p className="text-red-700 text-sm">{prediction.error}</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {prediction.results?.map((result, index) => (
                      <div
                        key={result.disease}
                        className="border-2 border-gray-200 rounded-xl p-4 hover:border-blue-300 transition-all"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              {index === 0 && (
                                <span className="bg-gradient-to-r from-yellow-400 to-orange-400 text-white text-xs px-2 py-0.5 rounded-full font-bold">
                                  TOP
                                </span>
                              )}
                              <h3 className="font-bold text-gray-800">{result.disease}</h3>
                            </div>
                            <p className="text-xs text-gray-500 mb-2">
                              {result.description?.substring(0, 100)}...
                            </p>
                          </div>
                        </div>

                        <div className="mb-3">
                          <div className="flex justify-between text-xs text-gray-600 mb-1">
                            <span>Confidence</span>
                            <span className="font-bold">{result.confidence}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all"
                              style={{ width: `${result.confidence}%` }}
                            />
                          </div>
                        </div>

                        {result.precautions && result.precautions.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-gray-200">
                            <div className="flex items-center gap-1 mb-2">
                              <Shield className="w-4 h-4 text-green-600" />
                              <span className="text-xs font-semibold text-gray-700">Precautions:</span>
                            </div>
                            <ul className="space-y-1">
                              {result.precautions.slice(0, 2).map((precaution, i) => (
                                <li key={i} className="text-xs text-gray-600 flex items-start gap-1">
                                  <ChevronRight className="w-3 h-3 text-green-500 mt-0.5 flex-shrink-0" />
                                  <span>{precaution}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}

                    <div className="mt-4 p-3 bg-blue-50 rounded-xl">
                      <p className="text-xs text-blue-900">
                        <strong>Disclaimer:</strong> This is an AI prediction tool. Please consult a healthcare provider for accurate diagnosis.
                      </p>
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
                <p className="text-sm text-yellow-800">
                  Enter tumor measurements. This requires 30 specific numerical features from medical imaging.
                  For testing purposes, you can enter sample values (e.g., radius_mean: 17.99, texture_mean: 10.38).
                </p>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6 max-h-96 overflow-y-auto p-2">
                {[...Array(30)].map((_, i) => (
                  <div key={i}>
                    <label className="text-xs font-medium text-gray-700 mb-1 block">
                      Feature {i + 1}
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

              <div className="flex gap-3">
                <button
                  onClick={predictCancer}
                  disabled={loading}
                  className="flex-1 bg-gradient-to-r from-red-500 to-pink-600 text-white py-3 rounded-xl font-semibold hover:shadow-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
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
                <div className="mt-6 p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl border-2 border-blue-200">
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

                  <div className="p-3 bg-white rounded-lg">
                    <div className="text-xs text-gray-600 mb-1">Risk Level</div>
                    <div className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                      cancerPrediction.risk_level === 'High' 
                        ? 'bg-red-100 text-red-700'
                        : cancerPrediction.risk_level === 'Medium'
                        ? 'bg-yellow-100 text-yellow-700'
                        : 'bg-green-100 text-green-700'
                    }`}>
                      {cancerPrediction.risk_level}
                    </div>
                  </div>
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
          // About Tab (same as before)
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-6">About Health Assistant Pro</h2>
              
              <div className="space-y-6 text-gray-700">
                <div>
                  <h3 className="text-xl font-semibold text-blue