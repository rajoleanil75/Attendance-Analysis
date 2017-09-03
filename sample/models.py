from django.db import models
from fernet_fields import EncryptedTextField
from fernet_fields import EncryptedEmailField
from fernet_fields import EncryptedIntegerField

class teacher(models.Model):
	tname = EncryptedTextField()
	designation = EncryptedTextField()
	contact_res=EncryptedIntegerField()
	contact_mob=EncryptedIntegerField()
	email=EncryptedEmailField()
	
# Create your models here.
