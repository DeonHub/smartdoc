stopwords = {"stop", "exit", "goodbye", "quit", "pause", "bye", "later", "end"}
repeat_patterns = {
                        "could you say that again?",
                        "could you repeat that for me?",
                        "I'm sorry, what was that?",
                        "come again?",
                        "pardon?",
                        "pardon me?",
                        "I beg your pardon?",
                        "repeat that, please.",
                        "repeat, please.",
                        "what did you say?",
                        "I didn't catch that.",
                        "can you say it again?",
                        "didn't quite get that.",
                        "one more time, please.",
                        "once again?",
                        "I didn't understand.",
                        "could you speak up?",
                        "I couldn't hear you.",
                        "that went over my head, can you repeat?",
                        "say that one more time?",
                        "can you clarify?",
                        "I'm not sure I followed, can you say that again?",
                        "mind repeating that?",
                        "I missed what you just said.",
                        "I was lost, can you go over that again?",
                        "I didn't hear you clearly.",
                        "that wasn't clear, can you please repeat?",
                    }

yes_patterns = ["^y(?:ea)?h?$", "^y[ea]*s$", "affirmative", "certainly", "definitely", "surely", "yup", "yep", "ok", "yes", "Yes", "ok sure", "alright sure", "ok sure no problem"]
no_patterns = ["^n(?:a)?h?$", "^no?p?$", "negative", "nay", "nope", "certainly not", "no please", "not interested"]



closeness_mappings = {
    # Negative responses
    "no": 0,
    "not at all": 5,
    "never": 10,
    "not really": 20,
    "doubtful": 15,
    "hardly": 20,
    "seldom": 25,
    "rarely": 25,
    "not often": 30,
    "infrequently": 35,

    # Neutral responses
    "sometimes": 50,  
    "occasionally": 55,
    "maybe": 50,
    "possibly": 55,
    "not sure": 50,
    "unsure": 50,

    # Positive responses
    "probably": 60,
    "likely": 65,
    "frequently": 70,
    "often": 75,
    "quite often": 80,
    "a lot": 85,
    "always": 90,
    "definitely": 95,
    "yes": 100
}


repeat_statements = [
    "My apologies, I didn't quite understand that. Could you rephrase?",
    "I'm sorry, could you say that in a different way?",
    "I didn't catch your last statement. Would you mind repeating it?",
    "Could you provide a bit more clarity on that?",
    "I'm trying to understand better. Could you reword that for me?",
    "I'd like to ensure I'm fully grasping your message. Can you explain again?",
    "Could you elaborate a bit more?",
    "I'm sorry, but I'm not entirely clear on what you said. Could you try explaining it again?",
    "I'd appreciate if you could provide a bit more detail on that.",
    "I'm finding it hard to process your words. Could you rephrase that for me?"
]



ask_more_symptoms_questions = [
    "Are there any other symptoms you'd like to discuss?",
    "Is there something else you've noticed about your health lately?",
    "Are there more signs or discomforts you wish to mention?",
    "Is there any other symptom or health change you've recently observed?",
    "Are there additional health concerns you think might be relevant?",
    "Is there something else you'd like to share regarding your well-being?",
    "Are there any other symptoms, however minor, that you've experienced?",
    "Is there any other health-related change that's been bothering you?",
    "Are there more health issues or symptoms you believe are important to discuss?"
]


invalid_repeat_statements = [
    "Invalid user ID. Can you please repeat your user ID?",
    "Sorry, that user ID doesn't seem valid. Could you say it again?",
    "I couldn't recognize that user ID. Please provide it once more.",
    "My apologies, but that doesn't look like a valid user ID. Could you restate it?",
    "Hmm, that didn't seem right. Please share your user ID again.",
    "I must have missed that. Can you repeat your user ID for me?",
    "Seems like there was an error with that user ID. Mind repeating it?",
    "I'm having trouble recognizing that user ID. Can you say it one more time?",
    "That user ID didn't register correctly. Please provide it again.",
    "Please double-check and restate your user ID; it didn't seem valid."
]

invalid_goodbye_statements = [
    "Invalid user ID. Please check your user ID and come back soon. Goodbye.",
    "Sorry, that user ID isn't registering. Double-check and try again later. Farewell.",
    "Unfortunately, I couldn't recognize your user ID. Please verify it and reach out again. Take care.",
    "I'm having difficulty with that user ID. Review it and give us another try. Until then, goodbye.",
    "It seems that user ID didn't work. Do look into it and return when ready. Bye for now.",
    "My apologies, but that user ID isn't valid. Please consult with our helpdesk or try again later. Goodbye.",
    "I'm unable to process that user ID. Ensure it's correct and come back. Wishing you a good day.",
    "That user ID seems off. Check and return whenever convenient. Farewell.",
    "Sorry for the inconvenience. Once you've confirmed your user ID, please reconnect. Goodbye.",
    "That user ID doesn't match our records. After verifying, do come back. Bye for now."
]


add_more_symptoms_statements = [
    "Please share any other symptoms or discomforts you might be experiencing.",
    "It would be helpful to know about any other symptoms you've observed. Please go ahead and share with me.",
    "Don't hesitate to mention any additional symptoms. I'm all ears.",
    "I'd appreciate any more details on other symptoms you've experienced. Please share with me.",
    "I'm here to understand fully. Please share any other symptoms you've noticed.",
    "Every detail helps. Please let me know anything other symptom you may have noticed."
]


open_messages = [
    "Hello, {}! How can I assist you today with your health concerns?",
    "Good day {}! What brings you in today?",
    "Welcome {}! How may I help with your health inquiries?",
    "Greetings {}! What health concerns can I assist with today?",
    "Hello {}! How can I be of service to you regarding your health?",
    "Thank you for reaching out {}. How can I address your health questions?"
]


start_messages = [
    "Hello! I'm Smart Doctor. ",
    "Greetings! You're chatting with Smart Doctor. ",
    "Hi there! Smart Doctor at your service. ",
    "Welcome! I'm the Smart Doctor bot. ",
    "Good day! It's Smart Doctor here. ",
    "Hey! I'm Smart Doctor. ",
    "Thank you for choosing Smart Doctor. ",
    "Hello and welcome! Smart Doctor is ready to help. ",
    "Hi! It's Smart Doctor. "
]



goodbye_messages = [
    "Goodbye! Take care and prioritize your health.",
    "Wishing you all the best. Stay well!",
    "Take care and always prioritize your well-being.",
    "Until our next conversation, stay healthy.",
    "Your health is important. Stay safe and take care!",
    "Remember to always prioritize your health. Goodbye!",
    "Stay positive and proactive about your health. Goodbye!",
    "Always keep your well-being in mind. Take care!",
    "Stay informed and attentive to your health. Goodbye!"
]


generic_responses = [
    "Thank you for opening up and discussing your health concerns with me.",
    "I truly appreciate your willingness to be open and detailed about your symptoms.",
    "Thank you for trusting me with this information; your well-being is my top concern.",
    "Your candidness is much appreciated. I'm here to assist and guide you through any health questions.",
    "I value our communication. Your health is paramount, and I'm here to help.",
    "Opening up about your health is vital. Thank you for providing these insights.",
    "Thank you for your transparency. Your communication is invaluable in providing effective care.",
    "I'm truly grateful for your trust in sharing your health concerns with me.",
    "Thank you for being forthright about your symptoms. I'm committed to understanding and addressing your health needs.",
    "I can't emphasize enough how important your insights are for your care. Thank you for sharing so openly."
]


sympathetic_responses = [
    "I'm genuinely sorry to hear you're feeling this way.",
    "Dealing with such symptoms can indeed be daunting. I'm here to help.",
    "Your well-being is my priority. Let's navigate this together.",
    "It sounds like you've been going through a lot. Let's work on finding a solution.",
    "I truly empathize with your situation. We'll tackle this together.",
    "Thank you for sharing your concerns. I'm here to provide the support you need.",
    "I understand that this is a challenging time for you. We'll address this step by step.",
    "It's important to me that you feel better. I'm dedicated to guiding you on this health journey.",
    "I'm here to listen, understand, and help you through these health concerns.",
    "It's disheartening to see anyone in discomfort. We'll explore every option to alleviate your symptoms.",
    "I want to reassure you that we'll take the necessary steps to improve your health situation.",
    "Please know that you're not alone in this. I'm here to assist and guide you.",
    "Facing health challenges can be tough, but together, we'll work towards a better outcome.",
    "Your health and comfort are crucial to me. We'll do everything we can to address your concerns.",
    "I appreciate your openness in sharing this. I'm committed to helping you get through it."
]


yes_or_no = [
    "Can you please respond with 'yes' or 'no'?",
    "Could you clarify your answer with a simple 'yes' or 'no'?",
    "It would help if you could answer with just 'yes' or 'no'.",
    "For clarity, please let me know with a 'yes' or 'no'.",
    "To ensure I understand correctly, could you reply with 'yes' or 'no'?",
    "To better assist you, please respond with 'yes' or 'no'.",
    "I appreciate your input. Would it be a 'yes' or a 'no'?",
    "It's crucial for our discussion; can you confirm with a 'yes' or 'no'?",
    "In order for me to provide the best care, could you specify 'yes' or 'no'?",
    "Please indicate with a 'yes' or 'no' so I can help further.",
    "Your clear response of 'yes' or 'no' will guide our next steps."
]


answer_statements = [
    "To better assist you, I would need some more information. Please take a moment to provide answers to the next few questions.",
    "Your health and well-being are my priority. Please share more details by answering the following questions.",
    "Every detail can help in understanding your situation better. Kindly provide insights by responding to these questions.",
    "Your detailed responses will enable me to guide you effectively. Let's delve deeper with a few more questions.",
    "To ensure we're on the same page, it would be helpful if you could elaborate on a few points by answering the upcoming questions.",
    "Your feedback is crucial in tailoring the best advice for you. I would appreciate it if you could answer these next questions.",
    "The more I understand about your situation, the better I can assist. Please take a moment to respond to these questions.",
    "Gaining a comprehensive understanding is key. Please help me achieve that by providing more details in response to these questions.",
    "Let's work together to get to the root of this. Please provide more insights by answering the following questions.",
    "To give you the most accurate guidance, I would like to know a bit more. Could you please answer these additional questions?"
]

disease_messages = [
    "Based on the information provided, there are chances you might be dealing with {}",
    "From the symptoms you've described, my diagnosis suggests that you have {}",
    "Taking into account all your symptoms, it appears you might be suffering from {}",
    "Considering the symptoms you've shared, there's a possibility you might have {}",
    "From what you've mentioned, it sounds like you could be experiencing {}",
    "The symptoms you've described align with those of {}",
    "Based on our conversation and the symptoms you've shared, it seems there's a possibility you have {}",
    "Your description suggests a likelihood of {}",
    "Taking everything into account, I'd consider the possibility of {}",
    "Given the symptoms you've shared, I'm leaning towards a diagnosis of {}"
]


no_disease_messages = [
    "I couldn't pinpoint a specific disease based on the symptoms you provided. It's essential to consult with a healthcare professional for a thorough evaluation.",
    "Based on our conversation, I recommend seeking a detailed examination from a doctor to ensure your health is in order.",
    "I'm unable to detect a definitive disease from the symptoms you mentioned. Please see a medical expert for a comprehensive assessment.",
    "Your symptoms require a more in-depth investigation. While I couldn't identify a particular ailment, a face-to-face consultation with a doctor is advised.",
    "Given the information you've shared, I suggest seeing a physician for an accurate diagnosis as I couldn't determine a specific disease.",
    "While I couldn't diagnose a particular condition based on the symptoms you've provided, it's crucial to get a medical professional's opinion.",
    "I recommend consulting with a healthcare expert directly. Your symptoms need a more detailed examination than I can provide.",
    "Your health is important. Though I couldn't pinpoint a disease, I strongly advise seeking medical attention for a precise diagnosis.",
    "I couldn't determine a disease from your described symptoms. It would be best to visit a doctor for an in-depth consultation.",
    "It's essential to consult with a physician if you're feeling unwell. My analysis couldn't detect a disease, but a doctor's examination is irreplaceable."
]


medicine_messages = [
    "I recommend you start taking {} according to the instructions for a swift recovery.",
    "It would be best if you take {}. Please follow the dosage guidelines carefully.",
    "Based on your symptoms, {} should help. Make sure to take it as directed.",
    "For your condition, {} is often prescribed. Please ensure you adhere to the dosage instructions.",
    "It's essential for your recovery that you begin taking {}. Follow the prescribed dose and duration.",
    "I'm prescribing {}. Ensure you read the guidelines and take it accordingly.",
    "Taking {} as per the directions will be beneficial for your recovery.",
    "Please begin your course with {}. It's crucial to take it regularly as directed.",
    "For best results, I'd advise you to take {}. Stick to the dosage recommendations.",
    "{} has been found effective for your condition. Ensure you take it regularly and as directed."
]


no_medicine_messages = [
    "There is no medicine I can recommend at this moment. I strongly suggest you see a doctor.",
    "Based on our conversation, I believe it's best to consult with a medical professional in person.",
    "I cannot prescribe any medication currently. Please consult a doctor for a comprehensive evaluation.",
    "For your specific symptoms, I recommend seeking immediate medical attention rather than relying on over-the-counter medications.",
    "Given the information you've provided, it's crucial to see a doctor for an accurate diagnosis and treatment.",
    "It's important to consult with a healthcare professional about your symptoms. Please prioritize this.",
    "I would advise against self-medication in this instance. Kindly visit a doctor for proper guidance.",
    "Your symptoms require a detailed examination. Please make an appointment with a doctor as soon as possible.",
    "I'm unable to recommend any medications right now. A consultation with a doctor would be the best course of action.",
    "Considering the complexity of your symptoms, it would be prudent to consult a physician directly."
]


book_appointment_messages = [
    "Would you like to book an appointment with the doctor?",
    "Would you consider making an appointment with a doctor?",
    "Would you like to set up an appointment to see the doctor?",
    "Do you wish to book an appointment with the doctor?",
    "Would you like to schedule an appointment with the doctor?"
]

appointment_messages = [
    "Your appointment has been booked. Once it's approved, we will send a confirmation email to you.",
    "I've scheduled your appointment. You'll receive an email once it's been confirmed.",
    "Your appointment is now booked. As soon as it gets approved, you'll be notified via email.",
    "I've set up your appointment. An email confirmation will be sent to you upon approval.",
    "We've successfully booked your appointment. Please wait for our email once it's confirmed.",
    "You're all set! Your appointment has been scheduled, and a confirmation email will be on its way after it's approved.",
    "Your appointment is in the queue. We'll shoot you an email post-approval.",
    "Your appointment has been noted. Expect an email from us once it's greenlit.",
    "All done! Your appointment is now booked. We'll email you after it's officially confirmed.",
    "I've booked your appointment. You'll get an email once everything is finalized."
]


hold_on_messages = [
    "Please hold on while I analyze your symptoms and make a prediction.",
    "Give me a moment to process your symptoms and determine the potential disease.",
    "I'm analyzing the data you provided. Please wait for a moment.",
    "Hold on for a bit. I'm running your symptoms through my database.",
    "Your health is important. Allow me a few seconds to evaluate your symptoms.",
    "I'm now evaluating your symptoms. Please stand by.",
    "Running diagnostics based on your symptoms. Please be patient.",
    "I need a moment to process everything. Please wait.",
    "Reviewing the information you've given me. Hold on, please.",
    "Let me cross-reference your symptoms. Stay on the line."
]


identification_messages = [
    "Please provide your user ID to continue.",
    "Please provide me your user ID to proceed.",
]


symptom_keywords = {
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills",
    "joint_pain", "stomach_pain", "headache", "acidity", "ulcers_on_tongue", "muscle_wasting", "vomiting",
    "burning_micturition", "nausea", "fever", "dizziness", "cold", "cough", "diarrhoea", "appetite"
}