from django.db import models
from fernet_fields import EncryptedTextField
from fernet_fields import EncryptedEmailField
from fernet_fields import EncryptedIntegerField
from django.utils import timezone

class admin(models.Model):
	uid=models.AutoField(primary_key=True)
	uname=models.TextField()
	upass=EncryptedTextField()
	lastlogin=models.DateTimeField(blank=True, null=True)

class teacher(models.Model):
	tid=models.IntegerField(primary_key=True)
	tname = EncryptedTextField()
	designation = EncryptedTextField()
	contact_mob=EncryptedIntegerField(default="")
	email=EncryptedEmailField(default="")
	tpassword=EncryptedTextField(default="")
	lastlogin=models.DateTimeField(blank=True, null=True)

class course(models.Model):
	coid=models.AutoField(primary_key=True)
	coname=models.TextField()
	copattern=models.IntegerField()
	
class classes(models.Model):
	clid=models.AutoField(primary_key=True)
	clname=models.TextField()
	course=models.ForeignKey(course, on_delete=models.CASCADE)

class division(models.Model):
	did=models.AutoField(primary_key=True)
	dname=models.TextField()
	dcapacity=models.IntegerField()
	classes=models.ForeignKey(classes, on_delete=models.CASCADE)
	
class subject(models.Model):
	sid=models.AutoField(primary_key=True)
	scode=EncryptedTextField()
	sname=EncryptedTextField()
	max_lacture=EncryptedIntegerField(default="")
	teacher=models.ForeignKey(teacher, on_delete=models.CASCADE)
	classes=models.ForeignKey(classes, on_delete=models.CASCADE)
	
class student(models.Model):
	sid=models.AutoField(primary_key=True)
	roll=EncryptedIntegerField(default="")
	sname=EncryptedTextField()
	smobile=EncryptedIntegerField(default="")
	semail=EncryptedTextField(default="")
	spassword=EncryptedTextField(default="")
	division=models.ForeignKey(division, on_delete=models.CASCADE)
	lastlogin=models.DateTimeField(blank=True, null=True)
	
class attendence(models.Model):
	aid=models.AutoField(primary_key=True)
	adate= models.DateField()
	atime=models.TimeField()
	student=models.ForeignKey(student, on_delete=models.CASCADE)
	subject=models.ForeignKey(subject, on_delete=models.CASCADE)
	division=models.ForeignKey(division, on_delete=models.CASCADE)
	
class lab(models.Model):
	slid=models.AutoField(primary_key=True)
	slname=EncryptedTextField()
	slstart=EncryptedIntegerField()
	slend=EncryptedIntegerField()
	division=models.ForeignKey(division, on_delete=models.CASCADE)

class lattendence(models.Model):
	laid=models.AutoField(primary_key=True)
	adate= models.DateField()
	atime=models.TimeField()
	student=models.ForeignKey(student, on_delete=models.CASCADE)
	lab=models.ForeignKey(lab, on_delete=models.CASCADE)
	
class divtimetable(models.Model):
	dtmid=models.AutoField(primary_key=True)
	slot_no=EncryptedIntegerField()
	slot_day=EncryptedIntegerField()
	slot_s_time= models.TimeField()
	slot_e_time= models.TimeField()
	subject=models.ForeignKey(subject, on_delete=models.CASCADE)
	division=models.ForeignKey(division, on_delete=models.CASCADE)
	
class labtimetable(models.Model):
	ltmid=models.AutoField(primary_key=True)
	slot_day=EncryptedIntegerField()
	slot_s_time= models.TimeField()
	slot_e_time= models.TimeField()
	lab=models.ForeignKey(lab, on_delete=models.CASCADE)
	
class mail(models.Model):
	mid=models.AutoField(primary_key=True)
	sender=EncryptedTextField()
	to=EncryptedTextField()
	subject=EncryptedTextField(default="")
	message=EncryptedTextField()
	mdate= models.DateField()
	mtime=models.TimeField()
	
