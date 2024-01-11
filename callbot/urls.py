# from django import views
from django.urls import path
from . import views

app_name = 'callbot'


urlpatterns = [
    path('handle-call/', views.handle_call, name='handle_call'),
    path('process-speech-usercode/', views.process_speech_usercode, name='process_speech_usercode'),
    path('process-speech-initial/', views.process_speech_initial, name='process_speech_initial'),

    # Additional URLs for the added steps in the flow
    path('process-speech-additional-symptoms/', views.process_speech_additional_symptoms, name='process_speech_additional_symptoms'),
    path('process-speech-additional-symptoms-list/', views.process_speech_additional_symptoms_list, name='process_speech_additional_symptoms_list'),
    path('process-speech-questions/', views.process_speech_questions, name='process_speech_questions'),
    path('process-speech-appointment/', views.process_speech_appointment, name='process_speech_appointment'),

]

