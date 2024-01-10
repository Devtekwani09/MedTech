from django.db import models

# Create your models here.
class doctor(models.Model):
    doctor_username = models.CharField(max_length=50)
    doctor_name = models.CharField(max_length=60)
    doctor_speciality = models.CharField(max_length=100)
    experience = models.IntegerField()
    doctor_fee = models.IntegerField()
    doctor_image = models.ImageField(upload_to="user/images")

    def __str__(self):
        return self.doctor_name