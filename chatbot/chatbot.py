import datetime
import re
import random
from django.http import JsonResponse
import joblib
# import language_tool_python
# from spellchecker import SpellChecker

import numpy as np


from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn

wn.ensure_loaded()

from core.models import Appointment, Medical, Profile
from .utilities import (stopwords, repeat_patterns, yes_patterns, no_patterns,
                       closeness_mappings, repeat_statements, ask_more_symptoms_questions,
                       add_more_symptoms_statements, open_messages, goodbye_messages,
                       generic_responses, sympathetic_responses, yes_or_no, answer_statements, invalid_repeat_statements,
                       symptom_keywords, invalid_goodbye_statements, disease_messages, no_disease_messages, medicine_messages, no_medicine_messages, appointment_messages)
from .questions import questions

# import wordnet as wn  # Ensure you have imported wordnet from nltk.corpus
import re





class ChatBot:

    def __init__(self):
        self.symptoms = set()
        # self.language_tool = language_tool_python.LanguageTool('en-US')
        # self.spell = SpellChecker()
        self.asked_questions = set()
        self.usercode = ''
        self.username = ''
        self.attempts = 5
        self.medical_id = 0


    def check_usercode(self, text):
        # Remove all non-numeric characters except for periods
        cleaned_text = re.sub(r'[^0-9.]', ' ', text)
        
        # Extract number strings from the cleaned text
        number_strings = re.findall(r'\d+(?:\.\d+)?', cleaned_text)
        
        # Join the extracted number strings together
        usercode = ''.join(number_strings)

        print(usercode)
        
        try:
            profile = Profile.objects.get(usercode=usercode)
            self.username = profile.user.username

            return True, usercode
        except:
            return False, usercode


    def process_usercode(self, user_input):

        if self.is_stopword(user_input):
            response_message = random.choice(goodbye_messages)
        elif self.is_repeat_request(user_input):
            response_message = self.last_response
        else:
            valid_code, usercode = self.check_usercode(user_input)

            if not valid_code: 
                if self.attempts > 0:
                    self.attempts -= 1
                    response_message = random.choice(invalid_repeat_statements)
                else:
                    response_message = random.choice(invalid_goodbye_statements)    
            else:
                self.usercode = usercode
                response_message = random.choice(open_messages).format(self.username)
        
        return response_message, valid_code, self.attempts



    def process_input(self, user_input):

        print(user_input)

        response_message = ""
        extracted_symptoms = set()
        grammar_correct = True

        # if self.is_stopword(user_input):
        #     response_message = random.choice(goodbye_messages)
        # elif self.is_repeat_request(user_input):
        #     response_message = self.last_response

        grammar_correct = self.is_grammatically_correct(user_input)

        if not grammar_correct:
            response_message = random.choice(repeat_statements)
        else:
            extracted_symptoms = self.extract_symptoms(user_input)
            print(extracted_symptoms)
            print("Symptoms extracted")
            self.add_unique_symptoms(extracted_symptoms)
            print("Symptoms added")
            response_message = random.choice(sympathetic_responses)

        return response_message, grammar_correct



    def is_stopword(self, user_input):
        return user_input.lower() in stopwords

    def is_repeat_request(self, user_input):
        return any(re.search(pattern, user_input, re.IGNORECASE) for pattern in repeat_patterns)


    def is_grammatically_correct(self, user_input):
        user_input = user_input.rstrip('.!?')
        misspelled = self.spell.unknown(user_input.split())
        return not misspelled


    def extract_symptoms(self, user_input):
        symptoms = set()
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        input_words = user_input.replace('.', '').lower().split()

        # First, check for multi-word symptoms
        for symptom in symptom_keywords:
            if "_" in symptom and symptom.replace("_", " ") in user_input.lower():
                symptoms.add(symptom)

        # Then check for single-word symptoms
        for word in input_words:
            # Lemmatization check for root word match
            lemma = lemmatizer.lemmatize(word)
            if lemma in symptom_keywords:
                symptoms.add(lemma)

            # Check for semantic similarity using synsets
            stemmed_word = stemmer.stem(word)
            for symptom in symptom_keywords:
                synsets_stemmed = wn.synsets(stemmed_word)
                synsets_symptom = wn.synsets(symptom)
                for synset_stemmed in synsets_stemmed:
                    for synset_symptom in synsets_symptom:
                        similarity_score = synset_stemmed.path_similarity(synset_symptom)
                        if similarity_score and similarity_score > 0.8:
                            symptoms.add(symptom)

        # Check for symptom-related phrases in user input
        ache_related_parts = ["head", "stomach", "back", "tooth", "ear", "throat", "muscle", "joint", "chest"]

        for part in ache_related_parts:
            pattern = r'\b' + part + r'\b.*?\b(?:aches|pain|ache)\b'
            if re.search(pattern, user_input, re.IGNORECASE): 
                combined_symptom = f"{part}ache"
                if combined_symptom in symptom_keywords:
                    symptoms.add(combined_symptom)

        return symptoms


    def ask_more_symptoms(self):
        self.last_response = random.choice(ask_more_symptoms_questions)
        return self.last_response


    def process_ask_more_symptoms_response(self, response):
        response_lower = response.lower().rstrip('.!?')

        if any(re.match(pattern, response_lower) for pattern in yes_patterns):
            return True
        elif any(re.match(pattern, response_lower) for pattern in no_patterns):
            return False
        else:
            self.last_response = "Kindly answer with 'yes' or 'no'."
            return None  # This will trigger a reprompt in the calling function.




    def add_more_symptoms(self):
        self.last_response = random.choice(add_more_symptoms_statements)
        return self.last_response

    def process_add_more_symptoms_response(self, user_response):
        grammar_correct = True
        if self.is_repeat_request(user_response):
            return self.last_response, grammar_correct

        grammar_correct = self.is_grammatically_correct(user_response)
        if not grammar_correct:
            return random.choice(repeat_statements), grammar_correct

        additional_symptoms = self.extract_symptoms(user_response)
        self.add_unique_symptoms(additional_symptoms)

        return random.choice(generic_responses), grammar_correct






    def ask_yes_no_questions(self):
        # Reset the asked_questions set when starting to ask questions
        self.asked_questions = set()
        self.last_response = self.get_new_question()
        return self.last_response


    def get_new_question(self):
        # Ensure that the same question is not asked again by choosing from the questions that haven't been asked yet
        available_questions = set(questions) - self.asked_questions
        if available_questions:
            new_question = random.choice(list(available_questions))
            self.asked_questions.add(new_question)
            return new_question
        return None


    def process_yes_no_question_response(self, response):

        if self.is_repeat_request(response):
            return self.last_response

        closeness_to_yes = self.measure_response_closeness_to_yes(response)
        if closeness_to_yes > 50:  # Adjust threshold if necessary
            symptoms_from_question = self.extract_symptoms(self.last_response)
            self.add_unique_symptoms(symptoms_from_question)

        self.last_response = self.get_new_question()
        return self.last_response
    


    def measure_response_closeness_to_yes(self, response):
        """Measure the percentage of closeness of a response to 'yes'."""

        response = response.lower().strip()

        if "yes" in response:
            return 100
        if "no" in response:
            return 0


        # Check for the presence of each phrase in the user's response and return the closeness of the first matching phrase
        for phrase in closeness_mappings.keys():
            if phrase in response:
                return closeness_mappings[phrase]

        # Default value for phrases not in the mappings
        default_closeness = 50  # Neutral responses

        return default_closeness



    def add_unique_symptoms(self, new_symptoms):
        self.symptoms.update(new_symptoms)
        print(self.symptoms)



    def recommend_drug(self, disease, userid):
            
        year = datetime.datetime.now().year	

        dob = Profile.objects.filter(user_id=userid).values_list('birth_date', flat=True)
        dob = int(str(list(dob)[0])[0:4])

        age = int(year) - dob

        gender = Profile.objects.filter(user_id=userid).values_list('gender', flat=True)
        gender = list(gender)
        gender = gender[0]


        if gender == 'Male' or gender == 'male':
            sex = 1
        else:
            sex = 0


        disease_list = ['Allergy', 'Urinary tract infection', 'Malaria', 'Diabetes', 'Fungal infection', 'AIDS', 'Acne', 'Hepatitis B', 'Psoriasis', 'Hypertension', 'Osteoarthritis', 'Migraine', 'Pneumonia', 'GERD']
        
        disease_dict = {'Allergy':0, 'Urinary tract infection':1, 'Malaria':2, 'Diabetes':3,
        'Fungal infection':4, 'AIDS':5, 'Acne':6, 'Hepatitis B':7, 'Psoriasis':8,
        'Hypertension':9, 'Osteoarthritis':10, 'Migraine':11, 'Pneumonia':12, 'GERD':13}

        if disease in disease_list:
            new_sick = disease_dict.get(disease)

            test = [new_sick,sex,age]
            test = np.array(test)
            test = np.array(test).reshape(1,-1)
            
            clf = joblib.load('model/medical_nb.pkl')
            prediction = clf.predict(test)
            drug = prediction[0]

            return {
                'status': True,
                'drug': drug
            }

        else:
            
            return {
                'status': False,
                'drug': 'See Doctor'
                }



    def predict_disease(self):
        
        symptoms_list = list(self.symptoms)
        
        try:
            s1 = symptoms_list[0]
        except IndexError:
            s1 = ''

        try:
            s2 = symptoms_list[1]
        except IndexError:
            s2 = ''

        try:
            s3 = symptoms_list[2]
        except IndexError:
            s3 = ''

        try:
            s4 = symptoms_list[3]
        except IndexError:
            s4 = ''

        try:
            s5 = symptoms_list[4]
        except IndexError:
            s5 = ''    


        userid = Profile.objects.get(usercode=self.usercode).user.id
        

        list_b = [s1,s2,s3,s4,s5]

        list_a = ['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain','stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination','fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy','patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating','dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes','back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine','yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach','swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation','redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs','fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails','swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips','slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints','movement_stiffness','spinning_movements','loss_of_balance','unsteadiness','weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine','continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)','depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain','abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling','silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze']
        

        # Loop to convert all symptoms into 0's
        list_c = [] # EMpty list to store disease symptoms converted into 0's and 1's
        for x in range(0,len(list_a)):
            list_c.append(0)


        # For all matched specific disease symptoms in general put 1 and unmatched put 0
        for z in range(0,len(list_a)):
            for k in list_b:
                if(k==list_a[z]):
                    list_c[z]=1

        test = list_c
        test = np.array(test)
        test = np.array(test).reshape(1,-1)

        clf = joblib.load('model/naive_bayes.pkl')

        prediction = clf.predict(test)
        disease = prediction[0]
        medicine = ''


        if disease:
            disease_message = random.choice(disease_messages).format(disease)

            drug = self.recommend_drug(disease, userid)
            status = drug['status']

            if status:
                medicine = drug['drug']
                medicine_message = random.choice(medicine_messages).format(medicine)
            else:
                medicine_message = random.choice(no_medicine_messages)

            a = Medical.objects.create(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, disease=disease, patient_id=userid, medicine=medicine, recommended=True)
            a.save()

            self.medical_id = a.id

        else:
            disease_message = random.choice(no_disease_messages)
            medicine_message = no_medicine_messages[0]
            medicine = ''


        return disease, disease_message, medicine, medicine_message



    def contains_yes(self, sentence):
        words = sentence.lower().split()
        return 'yes' in words


    def book_appointment(self):
        
        userid = Profile.objects.get(usercode=self.usercode).user.id
        
        check_medical = Appointment.objects.filter(medical_id=self.medical_id).exists()

        if check_medical == False:
            a = Appointment(medical_id=self.medical_id, patient_id=userid)
            a.save()

            medical = Medical.objects.get(id=self.medical_id)
            medical.requested_appointment = True
            medical.save()


        appointment_message = random.choice(appointment_messages)
        return appointment_message


