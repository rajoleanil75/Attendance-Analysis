from django import forms

class NameForm(forms.Form):
    tname = forms.CharField(label='tname', max_length=40)
	designation=forms.CharField(label='designation', max_length=20)
	contact_res=forms.IntegerField(label='rescontact')
	contact_mob=forms.IntegerField(label='mobileno')
	email=forms.CharField(label='emailid',max_length=30)