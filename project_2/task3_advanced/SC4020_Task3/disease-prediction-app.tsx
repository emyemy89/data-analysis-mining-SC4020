import React, { useState, useEffect } from 'react';
import { Activity, AlertCircle, Heart, Stethoscope, Shield, Search, X, ChevronRight, Info } from 'lucide-react';

// Disease-Symptom Data
const diseaseSymptoms = {
  "Fungal infection": ["itching", "skin_rash", "nodal_skin_eruptions", "dischromic_patches"],
  "Allergy": ["continuous_sneezing", "shivering", "chills", "watering_from_eyes"],
  "GERD": ["stomach_pain", "acidity", "ulcers_on_tongue", "vomiting", "cough", "chest_pain"],
  "Chronic cholestasis": ["itching", "vomiting", "yellowish_skin", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes"],
  "Drug Reaction": ["itching", "skin_rash", "stomach_pain", "burning_micturition", "spotting_urination"],
  "Peptic ulcer diseae": ["vomiting", "loss_of_appetite", "abdominal_pain", "passage_of_gases", "internal_itching", "indigestion"],
  "AIDS": ["muscle_wasting", "patches_in_throat", "high_fever", "extra_marital_contacts"],
  "Diabetes": ["fatigue", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level", "blurred_and_distorted_vision", "obesity", "excessive_hunger", "increased_appetite", "polyuria"],
  "Gastroenteritis": ["vomiting", "sunken_eyes", "dehydration", "diarrhoea"],
  "Bronchial Asthma": ["fatigue", "cough", "high_fever", "breathlessness", "family_history", "mucoid_sputum"],
  "Hypertension": ["headache", "chest_pain", "dizziness", "loss_of_balance", "lack_of_concentration"],
  "Migraine": ["acidity", "indigestion", "headache", "blurred_and_distorted_vision", "excessive_hunger", "stiff_neck", "depression", "irritability", "visual_disturbances"],
  "Cervical spondylosis": ["back_pain", "weakness_in_limbs", "neck_pain", "dizziness", "loss_of_balance"],
  "Paralysis (brain hemorrhage)": ["vomiting", "headache", "weakness_of_one_body_side", "altered_sensorium"],
  "Jaundice": ["itching", "vomiting", "fatigue", "weight_loss", "high_fever", "yellowish_skin", "dark_urine", "abdominal_pain"],
  "Malaria": ["chills", "vomiting", "high_fever", "sweating", "headache", "nausea", "diarrhoea", "muscle_pain"],
  "Chicken pox": ["itching", "skin_rash", "fatigue", "lethargy", "high_fever", "headache", "loss_of_appetite", "mild_fever", "swelled_lymph_nodes", "malaise", "red_spots_over_body"],
  "Dengue": ["skin_rash", "chills", "joint_pain", "vomiting", "fatigue", "high_fever", "headache", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "malaise", "muscle_pain", "red_spots_over_body"],
  "Typhoid": ["chills", "vomiting", "fatigue", "high_fever", "headache", "nausea", "constipation", "abdominal_pain", "diarrhoea", "toxic_look_(typhos)", "belly_pain"],
  "hepatitis A": ["joint_pain", "vomiting", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "diarrhoea", "mild_fever", "yellowing_of_eyes", "muscle_pain"],
  "Hepatitis B": ["itching", "fatigue", "lethargy", "yellowish_skin", "dark_urine", "loss_of_appetite", "abdominal_pain", "yellow_urine", "yellowing_of_eyes", "malaise", "receiving_blood_transfusion", "receiving_unsterile_injections"],
  "Hepatitis C": ["fatigue", "yellowish_skin", "nausea", "loss_of_appetite", "yellowing_of_eyes", "family_history"],
  "Hepatitis D": ["joint_pain", "vomiting", "fatigue", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes"],
  "Hepatitis E": ["joint_pain", "vomiting", "fatigue", "high_fever", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes", "acute_liver_failure", "coma", "stomach_bleeding"],
  "Alcoholic hepatitis": ["vomiting", "yellowish_skin", "abdominal_pain", "swelling_of_stomach", "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload"],
  "Tuberculosis": ["chills", "vomiting", "fatigue", "weight_loss", "cough", "high_fever", "breathlessness", "sweating", "loss_of_appetite", "mild_fever", "yellowing_of_eyes", "swelled_lymph_nodes", "malaise", "phlegm", "chest_pain", "blood_in_sputum"],
  "Common Cold": ["continuous_sneezing", "chills", "fatigue", "cough", "high_fever", "headache", "swelled_lymph_nodes", "malaise", "phlegm", "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "chest_pain", "loss_of_smell", "muscle_pain"],
  "Pneumonia": ["chills", "fatigue", "cough", "high_fever", "breathlessness", "sweating", "malaise", "phlegm", "chest_pain", "fast_heart_rate", "rusty_sputum"],
  "Dimorphic hemmorhoids(piles)": ["constipation", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus"],
  "Heart attack": ["vomiting", "breathlessness", "sweating", "chest_pain"],
  "Varicose veins": ["fatigue", "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels", "prominent_veins_on_calf"],
  "Hypothyroidism": ["fatigue", "weight_gain", "cold_hands_and_feets", "mood_swings", "lethargy", "dizziness", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "depression", "irritability", "abnormal_menstruation"],
  "Hyperthyroidism": ["fatigue", "mood_swings", "weight_loss", "restlessness", "sweating", "diarrhoea", "fast_heart_rate", "excessive_hunger", "muscle_weakness", "irritability", "abnormal_menstruation"],
  "Hypoglycemia": ["vomiting", "fatigue", "anxiety", "sweating", "headache", "nausea", "blurred_and_distorted_vision", "excessive_hunger", "drying_and_tingling_lips", "slurred_speech", "irritability", "palpitations"],
  "Osteoarthristis": ["joint_pain", "neck_pain", "knee_pain", "hip_joint_pain", "swelling_joints", "painful_walking"],
  "Arthritis": ["muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", "painful_walking"],
  "(vertigo) Paroymsal Positional Vertigo": ["vomiting", "headache", "nausea", "spinning_movements", "loss_of_balance", "unsteadiness"],
  "Acne": ["skin_rash", "pus_filled_pimples", "blackheads", "scurring"],
  "Urinary tract infection": ["burning_micturition", "bladder_discomfort", "foul_smell_of_urine", "continuous_feel_of_urine"],
  "Psoriasis": ["skin_rash", "joint_pain", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails"],
  "Impetigo": ["skin_rash", "high_fever", "blister", "red_sore_around_nose", "yellow_crust_ooze"]
};

const diseaseDescriptions = {
  "Drug Reaction": "An adverse drug reaction (ADR) is an injury caused by taking medication. ADRs may occur following a single dose or prolonged administration of a drug.",
  "Malaria": "An infectious disease caused by protozoan parasites from the Plasmodium family that can be transmitted by the bite of the Anopheles mosquito.",
  "Allergy": "An immune system response to a foreign substance that's not typically harmful to your body, such as certain foods, pollen, or pet dander.",
  "Hypothyroidism": "A disorder of the endocrine system in which the thyroid gland does not produce enough thyroid hormone.",
  "Psoriasis": "A common skin disorder that forms thick, red, bumpy patches covered with silvery scales.",
  "GERD": "Gastroesophageal reflux disease affects the lower esophageal sphincter, causing heartburn or acid indigestion.",
  "Chronic cholestasis": "Characterized by defective bile acid transport from the liver to the intestine.",
  "hepatitis A": "A highly contagious liver infection caused by the hepatitis A virus.",
  "Osteoarthristis": "The most common form of arthritis, occurring when protective cartilage cushions wear down over time.",
  "(vertigo) Paroymsal Positional Vertigo": "One of the most common causes of vertigo, causing brief episodes of mild to intense dizziness.",
  "Hypoglycemia": "A condition in which blood sugar (glucose) level is lower than normal.",
  "Acne": "Formation of comedones, papules, pustules, nodules, and/or cysts due to obstruction and inflammation of hair follicles.",
  "Diabetes": "A disease that occurs when blood glucose is too high, affecting how the body uses glucose for energy.",
  "Impetigo": "A common and highly contagious skin infection that mainly affects infants and children.",
  "Hypertension": "Also known as high blood pressure, a long-term medical condition with persistently elevated blood pressure.",
  "Peptic ulcer diseae": "A break in the inner lining of the stomach, small intestine, or lower esophagus.",
  "Dimorphic hemmorhoids(piles)": "Vascular structures in the anal canal that can become swollen and inflamed.",
  "Common Cold": "A viral infection of the nose and throat (upper respiratory tract).",
  "Chicken pox": "A highly contagious disease caused by the varicella-zoster virus, causing an itchy, blister-like rash.",
  "Cervical spondylosis": "Age-related wear and tear affecting the spinal disks in the neck.",
  "Hyperthyroidism": "Occurs when the thyroid gland produces too much thyroxine hormone.",
  "Urinary tract infection": "An infection of the kidney, ureter, bladder, or urethra.",
  "Varicose veins": "Enlarged and twisted veins, often appearing as bulging, blue blood vessels.",
  "AIDS": "A chronic condition caused by HIV that damages the immune system.",
  "Paralysis (brain hemorrhage)": "When blood suddenly bursts into brain tissue, causing damage and symptoms like paralysis.",
  "Typhoid": "An acute illness characterized by fever caused by infection with Salmonella typhi bacteria.",
  "Hepatitis B": "A liver infection that can cause scarring, liver failure, and cancer.",
  "Fungal infection": "Occurs when an invading fungus takes over an area of the body.",
  "Hepatitis C": "Inflammation of the liver due to the hepatitis C virus.",
  "Migraine": "Severe throbbing pain or pulsing sensation, usually on one side of the head.",
  "Bronchial Asthma": "A condition causing the airway path of the lungs to swell and narrow.",
  "Alcoholic hepatitis": "A diseased, inflammatory condition of the liver caused by heavy alcohol consumption.",
  "Jaundice": "Yellow staining of the skin and eyes by abnormally high blood levels of bilirubin.",
  "Hepatitis E": "A rare form of liver inflammation caused by infection with the hepatitis E virus.",
  "Dengue": "An acute infectious disease caused by a flavivirus, transmitted by aedes mosquitoes.",
  "Hepatitis D": "An infection that causes the liver to become inflamed, caused by the hepatitis D virus.",
  "Heart attack": "The death of heart muscle due to loss of blood supply.",
  "Pneumonia": "An infection in one or both lungs causing inflammation in the air sacs.",
  "Arthritis": "Swelling and tenderness of one or more joints.",
  "Gastroenteritis": "Inflammation of the digestive tract, particularly the stomach and intestines.",
  "Tuberculosis": "An infectious disease usually caused by Mycobacterium tuberculosis bacteria."
};

const diseasePrecautions = {
  "Drug Reaction": ["Stop irritation", "Consult nearest hospital", "Stop taking drug", "Follow up"],
  "Malaria": ["Consult nearest hospital", "Avoid oily food", "Avoid non-veg food", "Keep mosquitos out"],
  "Allergy": ["Apply calamine", "Cover area with bandage", "Use ice to compress itching"],
  "Hypothyroidism": ["Reduce stress", "Exercise", "Eat healthy", "Get proper sleep"],
  "Psoriasis": ["Wash hands with warm soapy water", "Stop bleeding using pressure", "Consult doctor", "Salt baths"],
  "GERD": ["Avoid fatty spicy food", "Avoid lying down after eating", "Maintain healthy weight", "Exercise"],
  "Chronic cholestasis": ["Cold baths", "Anti-itch medicine", "Consult doctor", "Eat healthy"],
  "hepatitis A": ["Consult nearest hospital", "Wash hands thoroughly", "Avoid fatty spicy food", "Medication"],
  "Osteoarthristis": ["Acetaminophen", "Consult nearest hospital", "Follow up", "Salt baths"],
  "(vertigo) Paroymsal Positional Vertigo": ["Lie down", "Avoid sudden changes in body position", "Avoid abrupt head movement", "Relax"],
  "Hypoglycemia": ["Lie down on side", "Check pulse", "Drink sugary drinks", "Consult doctor"],
  "Acne": ["Bath twice", "Avoid fatty spicy food", "Drink plenty of water", "Avoid too many products"],
  "Diabetes": ["Have balanced diet", "Exercise", "Consult doctor", "Follow up"],
  "Impetigo": ["Soak affected area in warm water", "Use antibiotics", "Remove scabs with wet compressed cloth", "Consult doctor"],
  "Hypertension": ["Meditation", "Salt baths", "Reduce stress", "Get proper sleep"],
  "Peptic ulcer diseae": ["Avoid fatty spicy food", "Consume probiotic food", "Eliminate milk", "Limit alcohol"],
  "Dimorphic hemmorhoids(piles)": ["Avoid fatty spicy food", "Consume witch hazel", "Warm bath with epsom salt", "Consume aloe vera juice"],
  "Common Cold": ["Drink vitamin C rich drinks", "Take vapour", "Avoid cold food", "Keep fever in check"],
  "Chicken pox": ["Use neem in bathing", "Consume neem leaves", "Take vaccine", "Avoid public places"],
  "Cervical spondylosis": ["Use heating pad or cold pack", "Exercise", "Take OTC pain reliever", "Consult doctor"],
  "Hyperthyroidism": ["Eat healthy", "Massage", "Use lemon balm", "Take radioactive iodine treatment"],
  "Urinary tract infection": ["Drink plenty of water", "Increase vitamin C intake", "Drink cranberry juice", "Take probiotics"],
  "Varicose veins": ["Lie down flat and raise the leg high", "Use ointments", "Use vein compression", "Don't stand still for long"],
  "AIDS": ["Avoid open cuts", "Wear PPE if possible", "Consult doctor", "Follow up"],
  "Paralysis (brain hemorrhage)": ["Massage", "Eat healthy", "Exercise", "Consult doctor"],
  "Typhoid": ["Eat high calorie vegetables", "Antibiotic therapy", "Consult doctor", "Medication"],
  "Hepatitis B": ["Consult nearest hospital", "Vaccination", "Eat healthy", "Medication"],
  "Fungal infection": ["Bath twice", "Use Dettol or neem in bathing water", "Keep infected area dry", "Use clean cloths"],
  "Hepatitis C": ["Consult nearest hospital", "Vaccination", "Eat healthy", "Medication"],
  "Migraine": ["Meditation", "Reduce stress", "Use polaroid glasses in sun", "Consult doctor"],
  "Bronchial Asthma": ["Switch to loose clothing", "Take deep breaths", "Get away from trigger", "Seek help"],
  "Alcoholic hepatitis": ["Stop alcohol consumption", "Consult doctor", "Medication", "Follow up"],
  "Jaundice": ["Drink plenty of water", "Consume milk thistle", "Eat fruits and high fibrous food", "Medication"],
  "Hepatitis E": ["Stop alcohol consumption", "Rest", "Consult doctor", "Medication"],
  "Dengue": ["Drink papaya leaf juice", "Avoid fatty spicy food", "Keep mosquitos away", "Keep hydrated"],
  "Hepatitis D": ["Consult doctor", "Medication", "Eat healthy", "Follow up"],
  "Heart attack": ["Call ambulance", "Chew or swallow aspirin", "Keep calm"],
  "Pneumonia": ["Consult doctor", "Medication", "Rest", "Follow up"],
  "Arthritis": ["Exercise", "Use hot and cold therapy", "Try acupuncture", "Massage"],
  "Gastroenteritis": ["Stop eating solid food for a while", "Try taking small sips of water", "Rest", "Ease back into eating"],
  "Tuberculosis": ["Cover mouth", "Consult doctor", "Medication", "Rest"]
};

// All unique symptoms
const allSymptoms = [...new Set(Object.values(diseaseSymptoms).flat())].sort();

const App = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [activeTab, setActiveTab] = useState('predictor');

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

  const predictDisease = () => {
    if (selectedSymptoms.length === 0) {
      setPrediction({ error: "Please select at least one symptom" });
      return;
    }

    const scores = {};
    
    Object.entries(diseaseSymptoms).forEach(([disease, symptoms]) => {
      const matchingSymptoms = selectedSymptoms.filter(s => symptoms.includes(s));
      const matchScore = matchingSymptoms.length;
      const totalSymptoms = symptoms.length;
      const percentage = (matchScore / totalSymptoms) * 100;
      
      if (matchScore > 0) {
        scores[disease] = {
          matchingSymptoms,
          matchScore,
          totalSymptoms,
          percentage: percentage.toFixed(1)
        };
      }
    });

    const sortedDiseases = Object.entries(scores)
      .sort((a, b) => b[1].matchScore - a[1].matchScore)
      .slice(0, 5);

    setPrediction({
      results: sortedDiseases,
      selectedCount: selectedSymptoms.length
    });
  };

  const resetForm = () => {
    setSelectedSymptoms([]);
    setPrediction(null);
    setSearchTerm('');
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
                  Health Assistant
                </h1>
                <p className="text-sm text-gray-500">AI-Powered Disease Prediction</p>
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
                Predictor
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
            {/* Left Panel - Symptom Selection */}
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

                {/* Search Bar */}
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

                {/* Selected Symptoms */}
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

                {/* Symptom Grid */}
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

                {/* Action Buttons */}
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={predictDisease}
                    disabled={selectedSymptoms.length === 0}
                    className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-xl font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    <Heart className="w-5 h-5" />
                    Predict Disease
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

            {/* Right Panel - Results */}
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
                    {prediction.results.map(([disease, data], index) => (
                      <div
                        key={disease}
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
                              <h3 className="font-bold text-gray-800">{disease}</h3>
                            </div>
                            <p className="text-xs text-gray-500 mb-2">
                              {diseaseDescriptions[disease]?.substring(0, 100)}...
                            </p>
                          </div>
                        </div>

                        <div className="mb-3">
                          <div className="flex justify-between text-xs text-gray-600 mb-1">
                            <span>Match Confidence</span>
                            <span className="font-bold">{data.percentage}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all"
                              style={{ width: `${data.percentage}%` }}
                            />
                          </div>
                        </div>

                        <div className="text-xs text-gray-600">
                          <span className="font-medium">Matching: </span>
                          {data.matchScore} of {data.totalSymptoms} symptoms
                        </div>

                        {diseasePrecautions[disease] && (
                          <div className="mt-3 pt-3 border-t border-gray-200">
                            <div className="flex items-center gap-1 mb-2">
                              <Shield className="w-4 h-4 text-green-600" />
                              <span className="text-xs font-semibold text-gray-700">Precautions:</span>
                            </div>
                            <ul className="space-y-1">
                              {diseasePrecautions[disease].slice(0, 2).map((precaution, i) => (
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

                    {prediction.results.length === 0 && (
                      <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4">
                        <p className="text-yellow-800 text-sm">
                          No matching diseases found. Please try selecting different symptoms.
                        </p>
                      </div>
                    )}

                    <div className="mt-4 p-3 bg-blue-50 rounded-xl">
                      <p className="text-xs text-blue-900">
                        <strong>Disclaimer:</strong> This is an AI prediction tool and should not replace professional medical advice. Please consult a healthcare provider for accurate diagnosis.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : (
          // About Tab
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-6">About Health Assistant</h2>
              
              <div className="space-y-6 text-gray-700">
                <div>
                  <h3 className="text-xl font-semibold text-blue-600 mb-3">What is this?</h3>
                  <p className="leading-relaxed">
                    Health Assistant is an AI-powered disease prediction system that analyzes your symptoms 
                    to suggest possible medical conditions. Using a comprehensive database of diseases and 
                    their associated symptoms, our system provides quick preliminary assessments.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-purple-600 mb-3">How it works</h3>
                  <ol className="list-decimal list-inside space-y-2">
                    <li>Select one or more symptoms you're experiencing</li>
                    <li>Click "Predict Disease" to analyze your symptoms</li>
                    <li>Review the top matching diseases with confidence scores</li>
                    <li>Read precautionary measures for each condition</li>
                    <li>Consult a healthcare professional for proper diagnosis</li>
                  </ol>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-green-600 mb-3">Features</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex items-start gap-3">
                      <div className="bg-blue-100 p-2 rounded-lg">
                        <Activity className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold">Smart Prediction</h4>
                        <p className="text-sm text-gray-600">AI-powered disease matching algorithm</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="bg-purple-100 p-2 rounded-lg">
                        <Shield className="w-5 h-5 text-purple-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold">Precautions</h4>
                        <p className="text-sm text-gray-600">Detailed safety measures for each condition</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="bg-green-100 p-2 rounded-lg">
                        <Heart className="w-5 h-5 text-green-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold">Comprehensive Database</h4>
                        <p className="text-sm text-gray-600">40+ diseases and 130+ symptoms</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="bg-orange-100 p-2 rounded-lg">
                        <Stethoscope className="w-5 h-5 text-orange-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold">Easy to Use</h4>
                        <p className="text-sm text-gray-600">Simple, intuitive interface</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
                  <h3 className="text-xl font-semibold text-red-700 mb-2 flex items-center gap-2">
                    <AlertCircle className="w-5 h-5" />
                    Important Disclaimer
                  </h3>
                  <p className="text-red-800 text-sm leading-relaxed">
                    This tool is for informational purposes only and should NOT be used as a substitute 
                    for professional medical advice, diagnosis, or treatment. Always seek the advice of 
                    your physician or other qualified health provider with any questions you may have 
                    regarding a medical condition. Never disregard professional medical advice or delay 
                    in seeking it because of something you have read on this application.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-3">Data Sources</h3>
                  <p className="text-sm text-gray-600">
                    This system uses curated medical datasets including disease-symptom mappings, 
                    symptom severity weights, disease descriptions, and recommended precautionary measures.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>Health Assistant &copy; 2024 | Built with React & AI | For Educational Purposes Only</p>
        </div>
      </div>
    </div>
  );
};

export default App;