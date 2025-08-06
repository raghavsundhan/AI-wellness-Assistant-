import re
from collections import Counter

# ---------------------------
# 1. Basic NLP Pipeline
# ---------------------------

class SimpleWellnessAssistant:
    def __init__(self):
        # Symptom keywords database
        self.symptom_keywords = {
            'tired': ['tired', 'fatigue', 'exhausted', 'weary', 'drained', 'sleepy', 'lethargic'],
            'dizzy': ['dizzy', 'dizziness', 'lightheaded', 'vertigo', 'spinning', 'unsteady'],
            'headache': ['headache', 'head pain', 'migraine', 'head hurt', 'head ache'],
            'nausea': ['nausea', 'nauseous', 'sick', 'queasy', 'vomiting', 'throw up'],
            'fever': ['fever', 'hot', 'temperature', 'feverish', 'burning up'],
            'cough': ['cough', 'coughing', 'hack', 'throat clearing'],
            'pain': ['pain', 'ache', 'hurt', 'sore', 'tender', 'throbbing']
        }
        
        # Mock CUI (Concept Unique Identifier) mapping
        self.cui_mapping = {
            'tired': 'C0003862',
            'dizzy': 'C0012833', 
            'headache': 'C0018681',
            'nausea': 'C0027497',
            'fever': 'C0015967',
            'cough': 'C0010200',
            'pain': 'C0030193'
        }
        
        # Condition mapping based on symptom combinations
        self.condition_rules = {
            'Fatigue Syndrome': ['tired'],
            'Hypotension': ['dizzy', 'tired'],
            'Dehydration': ['dizzy', 'headache', 'tired'],
            'Anemia': ['tired', 'dizzy'],
            'Tension Headache': ['headache', 'tired'],
            'Gastroenteritis': ['nausea', 'tired'],
            'Common Cold': ['cough', 'tired'],
            'Migraine': ['headache', 'nausea'],
            'Flu': ['fever', 'tired', 'headache']
        }
    
    def extract_symptoms(self, text):
        """Extract symptoms from user input using keyword matching"""
        text_lower = text.lower()
        found_symptoms = []
        
        for symptom, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    cui = self.cui_mapping.get(symptom, 'UNKNOWN')
                    confidence = 0.8 + (len(keyword) * 0.02)  # Longer keywords get higher confidence
                    found_symptoms.append((symptom, cui, confidence))
                    break
        
        return found_symptoms
    
    def classify_intent(self, text):
        """Simple intent classification"""
        symptom_indicators = ['feeling', 'been', 'have', 'experiencing', 'suffering', 'hurts']
        question_indicators = ['what', 'why', 'how', 'when', 'should', '?']
        
        text_lower = text.lower()
        
        if any(indicator in text_lower for indicator in symptom_indicators):
            return {"label": "symptom_check", "confidence": 0.9}
        elif any(indicator in text_lower for indicator in question_indicators):
            return {"label": "health_question", "confidence": 0.8}
        else:
            return {"label": "general_health", "confidence": 0.6}
    
    def match_conditions(self, symptoms):
        """Match symptoms to possible medical conditions"""
        symptom_names = [symptom[0] for symptom in symptoms]
        possible_conditions = []
        
        for condition, required_symptoms in self.condition_rules.items():
            match_count = sum(1 for req_symptom in required_symptoms if req_symptom in symptom_names)
            if match_count > 0:
                confidence = match_count / len(required_symptoms)
                possible_conditions.append((condition, confidence, match_count))
        
        # Sort by confidence and match count
        possible_conditions.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return possible_conditions
    
    def get_recommendations(self, condition):
        """Generate recommendations for a given condition"""
        recommendations = {
            "Fatigue Syndrome": {
                "summary": "You may be experiencing chronic fatigue or energy depletion.",
                "precautions": "Ensure adequate sleep (7-9 hours), avoid excessive caffeine late in day.",
                "yoga": ["Balasana (Child's Pose)", "Viparita Karani (Legs up wall)", "Shavasana"],
                "diet": ["Iron-rich foods (spinach, lentils)", "Complex carbohydrates", "Plenty of water"],
                "medication": "Consider vitamin B12 and iron supplements after medical consultation."
            },
            "Hypotension": {
                "summary": "Your symptoms may relate to low blood pressure.",
                "precautions": "Increase salt intake slightly, avoid sudden position changes, stay hydrated.",
                "yoga": ["Tadasana (Mountain Pose)", "Vrikshasana (Tree Pose)", "Gentle backbends"],
                "diet": ["Salted nuts", "Bananas", "Electrolyte-rich foods", "Small frequent meals"],
                "medication": "Monitor blood pressure and consult physician if symptoms persist."
            },
            "Dehydration": {
                "summary": "You may be experiencing mild to moderate dehydration.",
                "precautions": "Increase fluid intake immediately, rest in cool environment.",
                "yoga": ["Gentle stretches", "Pranayama breathing exercises", "Restorative poses"],
                "diet": ["Water (8-10 glasses daily)", "Coconut water", "Fresh fruits", "Avoid alcohol"],
                "medication": "ORS (Oral Rehydration Solution) if severe. Seek medical help if no improvement."
            },
            "Anemia": {
                "summary": "You may have iron deficiency or other types of anemia.",
                "precautions": "Avoid tea/coffee with meals, eat vitamin C with iron-rich foods.",
                "yoga": ["Gentle inversions", "Balasana", "Supported backbends"],
                "diet": ["Red meat, spinach, lentils", "Beetroot juice", "Vitamin C rich fruits"],
                "medication": "Iron supplements and B12 after blood tests and medical consultation."
            }
        }
        
        return recommendations.get(condition, {
            "summary": "Symptoms require medical evaluation for proper diagnosis.",
            "precautions": "Monitor symptoms and seek healthcare professional advice.",
            "yoga": ["Gentle stretching", "Deep breathing exercises"],
            "diet": ["Balanced nutrition", "Adequate hydration"],
            "medication": "Consult healthcare provider for proper diagnosis and treatment."
        })
    
    def analyze(self, user_input):
        """Main analysis function"""
        print(f"🔍 Analyzing: '{user_input}'\n")
        
        # Step 1: Intent Classification
        intent = self.classify_intent(user_input)
        print(f"📋 Intent: {intent['label']} (confidence: {intent['confidence']:.2f})")
        
        # Step 2: Symptom Extraction
        symptoms = self.extract_symptoms(user_input)
        print(f"🩺 Extracted Symptoms:")
        for symptom, cui, confidence in symptoms:
            print(f"   - {symptom.capitalize()} (CUI: {cui}, confidence: {confidence:.2f})")
        
        if not symptoms:
            print("   - No specific symptoms detected")
            return
        
        # Step 3: Condition Matching
        conditions = self.match_conditions(symptoms)
        print(f"\n🔬 Possible Conditions:")
        
        if not conditions:
            print("   - No specific conditions identified")
            return
        
        # Step 4: Generate Recommendations
        print(f"\n📋 Medical Analysis & Recommendations:\n")
        
        for i, (condition, confidence, match_count) in enumerate(conditions[:3]):  # Top 3 conditions
            rec = self.get_recommendations(condition)
            
            print(f"{'='*60}")
            print(f"🩺 Condition #{i+1}: {condition}")
            print(f"🎯 Match Confidence: {confidence:.2f} ({match_count} symptom matches)")
            print(f"📝 Summary: {rec['summary']}")
            print(f"⚠️ Precautions: {rec['precautions']}")
            print(f"🧘 Yoga Recommendations: {', '.join(rec['yoga'])}")
            print(f"🥗 Diet Recommendations: {', '.join(rec['diet'])}")
            print(f"💊 Medical Advice: {rec['medication']}")
            print()
        
        # Medical Disclaimer
        print(f"{'='*60}")
        print("⚠️ MEDICAL DISCLAIMER:")
        print("This AI assistant provides general wellness information only.")
        print("Always consult qualified healthcare professionals for proper diagnosis.")
        print("In case of emergency, contact emergency services immediately.")

# ---------------------------
# Usage Example
# ---------------------------

if __name__ == "__main__":
    # Initialize the assistant
    assistant = SimpleWellnessAssistant()
    
    # Test cases
    test_inputs = [
        "I've been feeling really tired and dizzy lately. Not sure what's going on.",
        "I have a terrible headache and feel nauseous.",
        "I'm experiencing fatigue and have been coughing for days.",
        "Feel hot and have a fever with body aches."
    ]
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n{'#'*80}")
        print(f"TEST CASE {i}:")
        print(f"{'#'*80}")
        assistant.analyze(test_input)
        print("\n")
    
    # Interactive mode
    print(f"{'='*80}")
    print("INTERACTIVE MODE - Enter your symptoms (type 'quit' to exit):")
    print(f"{'='*80}")
    
    while True:
        try:
            user_input = input("\nDescribe your symptoms: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using AI Wellness Assistant!")
                break
            elif user_input:
                assistant.analyze(user_input)
            else:
                print("Please enter your symptoms or type 'quit' to exit.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
