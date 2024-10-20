import datetime
import random
import string
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Medical, User, Appointment, Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
import numpy as np
import os
from django.contrib import messages
import joblib as joblib
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string





def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))


def registerUser(request):
	template_name = 'register.html'
	page = "Register"	


	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		password = make_password(password)
		birth_date = request.POST.get('birth_date')

		country = request.POST.get('country')
		gender = request.POST.get('gender')
		contact = request.POST.get('contact')
		

		try:
			profile = request.FILES.get('profile')
		except:
			profile = None   


		codex = random.randint(10000, 99999)
		chars = random_char(3)
		usercode = f'108{codex}'

		try:
			a = User.objects.get(username=username)
			messages.error(request, 'User with username already exists.') 
			return redirect(registerUser)
		
		except:

			a = User.objects.create(username=username, email=email, password=password, is_patient=True)
			a.save()
			user_id = a.id

			Profile.objects.filter(id=user_id).create(user_id=user_id, birth_date=birth_date, gender=gender, profile=profile, country=country, usercode=usercode, contact=contact)

			messages.success(request, 'Account was Created Successfully')
			return redirect(loginView)
	
	else:               
		return render(request,  template_name, {
			'page': page
		})


# messages.success(request, 'Login Successful') 
#                     return redirect('superuser:index') 
# messages.error(request, 'Invalid login credentials. Please contact admin') 
#                     return HttpResponseRedirect(reverse('login:login'))


def loginView(request):
	template_name = 'login.html'
	page = "Login"
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			if user.is_patient:
				return redirect('patient_home')
			elif user.is_doctor:
				return redirect('doctor_home')
			else:
				return redirect('login')
		else:
			messages.info(request, "Invalid Username Or Password")
			return redirect('login')
	else:
		return render(request, template_name, {
		'page':page
		})					





def patient_home(request):
	template_name = 'patient/home.html'
	page = 'Patient Dashboard'
	user_id=request.user.id

	doctor = User.objects.filter(is_doctor=True).count()
	patient = User.objects.filter(is_patient=True, id=user_id).count()
	appointment = Appointment.objects.filter(approved=True, patient=user_id).count()
	medical1 = Medical.objects.filter(medicine='See Doctor', patient_id=user_id).count()
	medical2 = Medical.objects.filter(patient_id=user_id).count()
	medical3 = int(medical2) - int(medical1)

	user = request.user
	profile = Profile.objects.get(user=user)

	return render(request, template_name, {
		'status':'1', 
		'doctor':doctor, 
		'appointment':appointment, 
		'patient':patient, 
		'drug':medical3,
		'page': page,
		'profile':profile
		})

def patient_profile(request):
	template_name = 'patient/profile.html'
	user = request.user
	profile = Profile.objects.get(user=user)
	return render(request, template_name, {
		'profile': profile
	})




def diagnosis(request):
	template_name = 'patient/diagnosis.html'
	page = "Patient Diagnosis"
	symptoms = ['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain','stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination','fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy','patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating','dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes','back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine','yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach','swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation','redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs','fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails','swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips','slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints','movement_stiffness','spinning_movements','loss_of_balance','unsteadiness','weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine','continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)','depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain','abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling','silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze']
	new_symptoms = [symptom.replace('_', ' ').title() for symptom in symptoms]

	# Sort both lists
	symptoms.sort()
	new_symptoms.sort()

	# Create a dictionary
	symptom_dict = dict(zip(symptoms, new_symptoms))

	user = request.user
	profile = Profile.objects.get(user=user)

	return render(request, template_name, {
		'symptom_dict': symptom_dict,
		'profile': profile,
		'page':page

	})

def convert(name):
    return name.lower().replace(' ','_')


@csrf_exempt
def MakePredict(request):
	print("Predicting")
	userid = request.user.id

	s1 = convert(request.POST.get('s1'))
	s2 = convert(request.POST.get('s2'))
	s3 = convert(request.POST.get('s3'))
	s4 = convert(request.POST.get('s4'))
	s5 = convert(request.POST.get('s5'))
	id = request.POST.get('id')
	
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
	print("Finished predicting")

	drug = recommend_drug(request, disease, userid)
	medicine = drug['drug']
	status = drug['status']


	a = Medical.objects.create(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, disease=disease, patient_id=id, medicine=medicine, recommended=True)
	a.save()

	return JsonResponse({'disease': disease, 'medicine': medicine, 'status': status})			



# usercode = 'IVM72205'
# username = Profile.objects.get(usercode=usercode).user.username
# userid = Profile.objects.get(usercode=usercode).user.id
# print(userid)
# print(username)



# IVM72205
@csrf_exempt
def predict_disease(request, usercode, symptoms):
	print("Predicting")

	s1 = symptoms[0] if symptoms[0] else ''
	s2 = symptoms[1] if symptoms[1] else ''
	s3 = symptoms[2] if symptoms[2] else ''
	s4 = symptoms[3] if symptoms[3] else ''
	s5 = symptoms[4] if symptoms[4] else ''

	userid = Profile.objects.get(usercode=usercode).user.id
	

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
	print("Finished Predicting")

	drug = recommend_drug(request, disease, userid)
	medicine = drug['drug']
	status = drug['status']


	a = Medical.objects.create(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, disease=disease, patient_id=userid, medicine=medicine, recommended=True)
	a.save()

	return JsonResponse({'disease': disease, 'medicine': medicine, 'status': status})			



def recommend_drug(request, disease, userid):
    	
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




def patient_result(request):
	template_name = 'patient/result.html'
	page = "Patient Results"
	user_id = request.user.id
	disease = Medical.objects.filter(patient_id=user_id)
	appointments = Appointment.objects.filter(patient_id=user_id)

	user = request.user
	profile = Profile.objects.get(user=user)


	context = {'disease':disease, 'appointments':appointments, 'profile': profile, 'page':page}
	return render(request, template_name, context)




def patient_delete_result(request, id, *args, **kwargs):

	if request.method == "POST":
		medical = Medical.objects.get(id=id)
		medical.delete()

	messages.success(request, 'Medical deleted successfully!')
	return redirect('result')



@csrf_exempt
def request_appointment(request):
	disease = request.POST.get('disease')
	userid = request.POST.get('userid')

	try:
		check_medical = Appointment.objects.filter(medical_id=disease).exists()
		if(check_medical == False):
			a = Appointment(medical_id=disease, patient_id=userid)
			a.save()

			medical = Medical.objects.get(id=disease)
			medical.requested_appointment = True
			medical.save()

			messages.success(request, 'Appointment requested successfully')

	except Exception as e:
		messages.error(request, 'Something went wrong')

	return redirect(patient_result)
		




def patient_appointments(request):
	user_id = request.user.id
	appointment = Appointment.objects.all().filter(patient_id=user_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	return render(request, 'patient/appointments.html', {
		'ment':appointment, 
		'status':'1', 
		'profile': profile
	})





def doctor_home(request):
	template_name = 'doctor/home.html'
	page = "Doctor Dashboard"

	doctor = User.objects.filter(is_doctor=True).count()
	patient = User.objects.filter(is_patient=True).count()
	appointment = Appointment.objects.filter(approved=True).count()
	medical1 = Medical.objects.filter(medicine='See Doctor').count()
	medical2 = Medical.objects.all().count()
	medical3 = int(medical2) - int(medical1)

	user = request.user
	profile = Profile.objects.get(user=user)
	
	info = [patient, doctor, appointment, medical3]
	context = {'doctor':doctor, 'appointment':appointment, 'patient':patient, 'drug':medical3, 'profile': profile, 'page':page, 'info': info}

	return render(request, template_name, context)


def doctor_commend(request):
	template_name = 'doctor/result.html'
	page = "Doctor Recommendations"
	disease = Medical.objects.all()

	user = request.user
	profile = Profile.objects.get(user=user)

	return render(request, template_name, {
	'disease':disease, 
	'profile': profile,
	'page':page
	})


def doctor_profile(request):
	template_name = 'doctor/profile.html'
	page = "Doctor Profile"
	user = request.user
	profile = Profile.objects.get(user=user)
	return render(request, template_name, {
		'profile': profile,
		'page':page
	})


@login_required
def doctor_appointments(request):
	template_name = 'doctor/appointments.html'
	page = "Doctor Appointments"
	user_id = request.user.id
	appointments = Appointment.objects.all()
	user = request.user
	profile = Profile.objects.get(user=user)

	context = {
		'appointments':appointments,
		'profile': profile,
		'page':page
		}
	
	return render(request, template_name, context)





def ordinal(number):
    """Return number with ordinal suffix."""
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme. 
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a fallback.
        suffix = suffixes.get(number % 10, 'th')
    return str(number) + suffix



@login_required
@csrf_exempt
def SaveMent(request):
	
	pk = request.POST.get('pk')
	day = request.POST.get('day')
	time = request.POST.get('time')
	user_id = request.POST.get('user_id')


	# Convert the string to a datetime object
	date_object = datetime.datetime.strptime(day, '%Y-%m-%d')
	appointment_date = ordinal(int(date_object.strftime('%d'))) + date_object.strftime(' %B, %Y')


	time_object = datetime.datetime.strptime(time, '%H:%M')
	appointment_time = time_object.strftime('%I:%M %p')



	doctor_id = request.user.id
	doctor_name = User.objects.get(id=doctor_id).username


	disease = Appointment.objects.filter(pk=pk).exists()

	email = User.objects.get(id=user_id).email
	print(email)
	username = User.objects.get(id=user_id).username


	subject = 'Appointment Confirmation'
	from_email = settings.EMAIL_HOST_USER  # Change this to your desired sender
	print(from_email)
	recipient_list = [email]

	# Render email content from template
	message = render_to_string('doctor/appointment_email.html', {
	    'username': username,
		'doctor_name': doctor_name,
		'appointment_date': appointment_date,
		'appointment_time': appointment_time,
	})

	try:
		send_mail(subject, '', from_email, recipient_list, html_message=message)
	except:
		print("Server error")	

	approved = Appointment.objects.filter(id=pk).update(approved=True, appointment_day=day, time=appointment_time, doctor_id=doctor_id)

	return redirect(doctor_appointments)


@login_required
@csrf_exempt
def doctor_recommend(request):
	pk = request.POST.get('pk')
	drug = request.POST.get('drug')
	
	diagnosis = Medical.objects.get(id=pk)
	diagnosis.medicine = drug
	diagnosis.recommended = True
	diagnosis.save()
	
	return redirect(doctor_commend)


def logoutView(request):
	logout(request)
	return redirect('login')

