from django.db import models
class teacher(models.Model):
	tname = models.CharField(max_length=40)
	designation = models.CharField(max_length=20)
	contact_res=models.IntegerField()
	contact_mob=models.IntegerField()
	email=models.CharField(max_length=30)
	
# Create your models here.
