import re
import random
import language_tool_python
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from utilities import stopwords, repeat_patterns, yes_patterns, no_patterns, closeness_mappings, repeat_statements, ask_more_symptoms_questions, add_more_symptoms_statements, open_messages, goodbye_messages, generic_responses, sympathetic_responses, yes_or_no, answer_statements, symptom_keywords
from questions import questions
import pyttsx3



class ChatBot:
    def __init__(self):
        self.symptoms = set()
        self.language_tool = language_tool_python.LanguageTool('en-US')
        self.last_response = ""
        self.engine = pyttsx3.init()
        
        
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
        
    def start(self):
        self.last_response = random.choice(open_messages)
        print(f"Doctor: {self.last_response}")
        self.speak(self.last_response)
        
        while True:
            user_input = input("Patient: ")
            if self.is_stopword(user_input):
                self.last_response = random.choice(goodbye_messages)
                print(f"Doctor: {self.last_response}")
                self.speak(self.last_response)
                
                break
                
            elif self.is_repeat_request(user_input):
                print(f"Doctor: {self.last_response}")
                self.speak(self.last_response)
                
            else:
                self.process_input(user_input)

            if self.symptoms:
                if self.ask_more_symptoms():
                    self.add_more_symptoms()

                self.ask_yes_no_questions()
                self.predict_disease()
                break


                    
    def is_stopword(self, user_input):
        return user_input.lower() in stopwords

    def is_repeat_request(self, user_input):
        return any(re.search(pattern, user_input, re.IGNORECASE) for pattern in repeat_patterns)

    def repeat_last_response(self):
        if self.symptoms:
            print("Doctor: Last time you mentioned the following symptoms:", ', '.join(self.symptoms))
        else:
            print(f"Doctor: {random.choice(repeat_statements)}")




    def process_input(self, user_input):
        if not self.is_grammatically_correct(user_input):
            print(f"Doctor: {random.choice(repeat_statements)}")
            self.speak(random.choice(repeat_statements))
            return

        symptoms_found = self.extract_symptoms(user_input)
        self.add_unique_symptoms(symptoms_found)
        
        self.last_response = random.choice(sympathetic_responses)
        print(f"Doctor: {self.last_response}")
        self.speak(self.last_response)
        
            
           
        
            
    def is_grammatically_correct(self, user_input):
        # Remove trailing punctuation
        user_input = user_input.rstrip('.!?')
        matches = self.language_tool.check(user_input)
        return not matches
    

    def extract_symptoms(self, user_input):
        symptoms = set()
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        input_words = user_input.lower().split()

        # First, check for multi-word symptoms
        for symptom in symptom_keywords:
            if "_" in symptom:  # Check if it's a multi-word symptom
                if symptom.replace("_", " ") in user_input.lower():  # If full symptom found in user input
                    symptoms.add(symptom)

        # Then check for single-word symptoms
        for symptom in symptom_keywords:
            if symptom not in symptoms:  # If it's not already found
                modified_pattern = symptom.replace("_", " ")
                pattern_words = modified_pattern.lower().split()

                for word in input_words:
                    # Check for exact match
                    if word in pattern_words:
                        symptoms.add(symptom)
                        break

                    # Lemmatization check for root word match
                    lemma = lemmatizer.lemmatize(word)
                    if lemma in pattern_words:
                        symptoms.add(symptom)
                        break

                    # Check for semantic similarity using synsets
                    stemmed_word = stemmer.stem(word)
                    max_similarity_score = 0.0
                    for pattern_word in pattern_words:
                        synsets_stemmed = wordnet.synsets(stemmed_word)
                        synsets_pattern = wordnet.synsets(pattern_word)
                        for synset_stemmed in synsets_stemmed:
                            for synset_pattern in synsets_pattern:
                                similarity_score = synset_stemmed.path_similarity(synset_pattern)
                                if similarity_score and similarity_score > max_similarity_score:
                                    max_similarity_score = similarity_score
                
                    if max_similarity_score > 0.8:
                        symptoms.add(symptom)
                        break

                # Check for symptom-related phrases in user input (e.g., "head aches")
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
        
        while True:
            print(f"Doctor: {self.last_response} ")
            self.speak(self.last_response)
            
            response = input(f"Patient: ")
            response_lower = response.lower().strip()

            if any(re.match(pattern, response_lower) for pattern in yes_patterns):
                return True
            elif any(re.match(pattern, response_lower) for pattern in no_patterns):
                return False
            else:
                print("Doctor: Kindly answer with 'yes' or 'no'.")
                self.speak("Kindly answer with 'yes' or 'no'.")


    
    

    def add_more_symptoms(self):
        self.last_response = random.choice(add_more_symptoms_statements)
        
        while True:

            print(f"Doctor: {self.last_response}")
            self.speak(self.last_response)

            user_response = input("Patient: ")
            

            if self.is_repeat_request(user_response):
                continue  # If a repeat request, the loop will restart, repeating the last response.

            elif not self.is_grammatically_correct(user_response):
                repeat = random.choice(repeat_statements)
                print(f"Doctor: {repeat}")
                self.speak(repeat)
                continue  # Ask for additional symptoms again

            additional_symptoms = self.extract_symptoms(user_response)
            self.add_unique_symptoms(additional_symptoms)

            message = random.choice(generic_responses)
            print(f"Doctor: {message}")
            self.speak(message)
            break

            
            
    def ask_yes_no_questions(self):
        self.last_response = random.choice(answer_statements)
        print(f"Doctor: {self.last_response}")
        self.speak(self.last_response)
        
        
        random.shuffle(questions)
        for question in questions[:5]:
            
            while True:
                print(f"Doctor: {question}")
                self.speak(question)
                response = input(f"Patient: ")

                # Check if the user has requested for repetition
                if self.is_repeat_request(response):
                    continue

                closeness_to_yes = self.measure_response_closeness_to_yes(response)
                if closeness_to_yes > 50:  # Adjust threshold if necessary
                    symptoms_from_question = self.extract_symptoms(question)
                    self.add_unique_symptoms(symptoms_from_question)
                break

                
                
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

        
    def predict_disease(self):
        print(list(self.symptoms))
        print("Predicting diseases...")
        self.speak("Predicting diseases...")
        # Disease prediction logic should be implemented here.
        message = random.choice(goodbye_messages)
        print(f"Doctor: {message}")
        self.speak(message)


# Create an instance of the ChatBot class
chatbot = ChatBot()
# Start the conversation
chatbot.start()