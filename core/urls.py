from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

path('', views.home, name='home'),
# path('register/', views.registerView, name='reg'),
path('register/', views.registerUser, name='register'),
path('login/', views.loginView, name='login'),




# Patient Paths
path('patient/dashboard', views.patient_home, name='patient_home'),
path('patient/profile', views.patient_profile, name='patient_profile'),
path('patient/diagnosis', views.diagnosis, name='diagnosis'),
path('patient/result', views.patient_result, name='result'),
path('patient/appointments', views.patient_appointments, name='patient_appointments'),
path('patient/delete-result/<int:id>', views.patient_delete_result, name='patient_delete_result'),
# path('delete-fee-type/<int:id>', views.deleteFeeType, name='deleteFeeType'),




path('diagnosis/predict', views.MakePredict, name='predict'),

path('result/request-appointment', views.request_appointment, name='request_appointment'),

path('logout/', views.logoutView, name='logout'),

# Doctor Paths
path('doctor/dashboard', views.doctor_home, name='doctor_home'),
path('doctor/profile', views.doctor_profile, name='doctor_profile'),
path('doctor/recommendations', views.doctor_commend, name='commend'),
path('doctor/recommend', views.doctor_recommend, name='doctor_recommend'),
path('doctor/appointments', views.doctor_appointments, name='meet_list'),


# path('commend/predict', views.MakeMend, name='mend'),
path('meet/save/', views.SaveMent, name='savement'),
path('doctors/', views.doctor_list, name='dr_list'),
path('about/', views.about, name='about'),










path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html',  success_url = reverse_lazy('user_accounts:password_reset_done')), name='password_reset'),

path('password-change/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),

#re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='user_accounts/password_reset_confirm.html'), name='password_reset_confirm'),

path('password-change/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url = reverse_lazy('user_accounts:password_reset_complete')), name='password_reset_confirm'),

path('password-change/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete')







]