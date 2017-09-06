from django.db import models
from fernet_fields import EncryptedTextField
from fernet_fields import EncryptedEmailField
from fernet_fields import EncryptedIntegerField
from django.utils import timezone

class admin(models.Model):
	uid=models.AutoField(primary_key=True)
	uname=EncryptedTextField()
	upass=EncryptedTextField()

class teacher(models.Model):
	tid=models.IntegerField(primary_key=True,default="")
	tname = EncryptedTextField()
	designation = EncryptedTextField()
	contact_mob=EncryptedIntegerField()
	email=EncryptedEmailField()
	tpassword=EncryptedTextField(default="")

class course(models.Model):
	coid=models.AutoField(primary_key=True)
	coname=EncryptedTextField()
	copattern=EncryptedIntegerField()
	
class classes(models.Model):
	clid=models.AutoField(primary_key=True)
	clname=EncryptedTextField()
	course=models.ForeignKey(course, on_delete=models.CASCADE)
	
class division(models.Model):
	did=models.AutoField(primary_key=True)
	dname=EncryptedTextField()
	dcapacity=EncryptedIntegerField()
	classes=models.ForeignKey(classes, on_delete=models.CASCADE)
	
class timetable(models.Model):
	tmid=models.AutoField(primary_key=True)
	slot_no=EncryptedIntegerField()
	slot_day=EncryptedIntegerField()
	slot_s_time= models.TimeField()
	slot_e_time= models.TimeField()
	division=models.ForeignKey(division, on_delete=models.CASCADE)
	
class subject(models.Model):
	sid=models.AutoField(primary_key=True)
	scode=EncryptedIntegerField()
	sname=EncryptedTextField()
	max_lacture=EncryptedIntegerField()
	max_lacture.null=True
	teacher=models.ForeignKey(teacher, on_delete=models.CASCADE)
	course=models.ForeignKey(course, on_delete=models.CASCADE)
	
class student(models.Model):
	adminssion_no=models.IntegerField(primary_key=True)
	roll=EncryptedIntegerField()
	sname=EncryptedTextField()
	smobile=EncryptedIntegerField()
	semail=EncryptedTextField()
	spassword=EncryptedTextField()
	
class attendence(models.Model):
	aid=models.AutoField(primary_key=True)
	adate= models.DateField()
	atime=models.TimeField()
	student=models.ForeignKey(student, on_delete=models.CASCADE)
	subject=models.ForeignKey(subject, on_delete=models.CASCADE)
	division=models.ForeignKey(division, on_delete=models.CASCADE)
	
	
# Create your models here.
