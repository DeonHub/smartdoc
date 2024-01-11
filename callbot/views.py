from django.http import HttpResponse
from twilio.twiml.voice_response import Gather, VoiceResponse, Hangup
from django.views.decorators.csrf import csrf_exempt
from chatbot.chatbot import ChatBot 
from chatbot.utilities import ask_more_symptoms_questions, start_messages, identification_messages, answer_statements, generic_responses, hold_on_messages, book_appointment_messages, goodbye_messages

import random



chatbot = ChatBot()

@csrf_exempt
def handle_call(request):
    response = VoiceResponse()
    response.say(random.choice(start_messages))

    gather = Gather(input="speech", action="/callbot/process-speech-usercode/", timeout=5)
    gather.say(random.choice(identification_messages))
    response.append(gather)
    return HttpResponse(str(response))



@csrf_exempt
def process_speech_usercode(request):
    user_speech = request.POST.get('SpeechResult')
    response = VoiceResponse()

    # Check if user has provided any input
    if not user_speech:
        response.say("Sorry, I couldn't hear you. Please speak again.")
        # response.redirect("/callbot/process-speech-usercode/")
        gather = Gather(input="speech", action="/callbot/process-speech-usercode/", timeout=5)
        response.append(gather)
        return HttpResponse(str(response))

    bot_response, valid_code, attempts = chatbot.process_usercode(user_speech)

    if not valid_code:
        response.say(bot_response)
        if int(attempts) == 0:
            response.append(Hangup())
            return HttpResponse(str(response))
        else:
            response.say(f'You have {attempts} attempts. Please try again.')
            gather = Gather(input="speech", action="/callbot/process-speech-usercode/", timeout=5)
            response.append(gather)
            return HttpResponse(str(response))

    response.say(bot_response)

    gather = Gather(input="speech", action="/callbot/process-speech-initial/", timeout=5)
    response.append(gather)

    return HttpResponse(str(response))



@csrf_exempt
def process_speech_initial(request):
    user_speech = request.POST.get('SpeechResult')
    response = VoiceResponse()

    # Check if user has provided any input
    # if not user_speech:
    #     response.say("Sorry, I couldn't hear you. Please speak again.")
    #     response.redirect("/callbot/process-speech-initial/")
    #     return HttpResponse(str(response))

    bot_response, grammar_correct = chatbot.process_input(user_speech)

    if not grammar_correct:
        response.say(bot_response) # This should play the repeat instruction
        response.append(Gather(input="speech", action="/callbot/process-speech-initial/", timeout=5))
        return HttpResponse(str(response))

    # current_session_symptoms = set(request.session.get('symptoms', []))
    # current_session_symptoms.update(extracted_symptoms)
    # request.session['symptoms'] = list(current_session_symptoms)

    # if extracted_symptoms:
    #     response.say(f"I've noted the following symptoms: {', '.join(extracted_symptoms)}.")

    response.say(bot_response)
    response.say(random.choice(ask_more_symptoms_questions))

    gather = Gather(input="speech", action="/callbot/process-speech-additional-symptoms/", timeout=5)
    response.append(gather)

    return HttpResponse(str(response))



@csrf_exempt
def process_speech_additional_symptoms(request):
    user_speech = request.POST.get('SpeechResult')
    response = VoiceResponse()


    # Checking if the user wants to add more symptoms
    if chatbot.process_ask_more_symptoms_response(user_speech):
        response.say(chatbot.add_more_symptoms())
        gather = Gather(input="speech", action="/callbot/process-speech-additional-symptoms-list/", timeout=5)
        response.append(gather)
    else:
        response.say(random.choice(answer_statements))
        response.say(chatbot.ask_yes_no_questions())
        gather = Gather(input="speech", action="/callbot/process-speech-questions/", timeout=5)
        response.append(gather)

    return HttpResponse(str(response))



@csrf_exempt
def process_speech_additional_symptoms_list(request):
    user_speech = request.POST.get('SpeechResult')
    response = VoiceResponse()

    bot_response, grammar_correct = chatbot.process_add_more_symptoms_response(user_speech)

    if not grammar_correct:
        response.say(bot_response) # This should play the repeat instruction
        response.append(Gather(input="speech", action="/callbot/process-speech-additional-symptoms-list/", timeout=5))
        return HttpResponse(str(response))

    response.say(bot_response)
    response.say(chatbot.ask_yes_no_questions())

    gather = Gather(input="speech", action="/callbot/process-speech-questions/", timeout=5)
    response.append(gather)

    return HttpResponse(str(response))




@csrf_exempt
def process_speech_questions(request):
    user_speech = request.POST.get('SpeechResult')
    response = VoiceResponse()

    next_question = chatbot.process_yes_no_question_response(user_speech)

    if len(chatbot.asked_questions) == 5:  # If 5 questions have been asked
        response.say(random.choice(generic_responses))

        # Directly integrating process_speech_prediction logic here.
        response.say(random.choice(hold_on_messages))

        # Adding a pause of 5 seconds
        response.pause(length=5)

        disease, disease_message, medicine, medicine_message = chatbot.predict_disease()

        response.say(disease_message)
        response.say(medicine_message)
        
        if disease:
            response.say(random.choice(book_appointment_messages))
            gather = Gather(input="speech", action="/callbot/process-speech-appointment/", timeout=5)
            response.append(gather)
        else:
            response.say(random.choice(goodbye_messages))
            response.append(Hangup())
    else:
        response.say(next_question)
        gather = Gather(input="speech", action="/callbot/process-speech-questions/", timeout=5)
        response.append(gather)

    return HttpResponse(str(response))



@csrf_exempt
def process_speech_appointment(request):
    user_speech = request.POST.get('SpeechResult')
    response = VoiceResponse()


    if chatbot.contains_yes(user_speech):
        bot_response = chatbot.book_appointment()
        response.say(bot_response)

    response.say(random.choice(goodbye_messages))
    response.append(Hangup())
    return HttpResponse(str(response))


