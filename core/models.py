from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.username



class Medical(models.Model):
    s1 = models.CharField(max_length=200)
    s2 = models.CharField(max_length=200)
    s3 = models.CharField(max_length=200)
    s4 = models.CharField(max_length=200)
    s5 = models.CharField(max_length=200)
    disease = models.CharField(max_length=200)
    medicine = models.CharField(max_length=200)
    patient = models.ForeignKey(User, related_name="patient", on_delete= models.CASCADE)
    doctor = models.ForeignKey(User, related_name="doctor", on_delete= models.CASCADE, null=True)
    requested_appointment = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient} performed a diagnosis on {self.created_on}'



class Appointment(models.Model):
    approved = models.BooleanField(default=False)
    time = models.CharField(max_length=200, null=True)
    patient = models.ForeignKey(User, related_name="pat", on_delete= models.CASCADE)
    doctor = models.ForeignKey(User, related_name="dor", on_delete= models.CASCADE, null=True)
    appointment_day = models.DateTimeField(null=True)
    medical = models.ForeignKey(Medical, related_name="medical", on_delete= models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient.username} requested an appointment on {self.created_on}'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usercode = models.CharField(max_length=10, default='ABC12345')
    profile = models.ImageField(upload_to = 'profile-uploads/', default = '', blank=True)
    birth_date = models.DateField(default='None')
    contact = models.CharField(max_length=255, default='1234567890')
    gender = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='Ghana')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



