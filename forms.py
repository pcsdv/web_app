from django import forms
from . models import *

class PatientForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(),required=True,max_length=100)
	dated = forms.DateTimeField()
	remedy=forms.CharField(widget=forms.TextInput(),required=True,max_length=255)

	class Meta():
		model = Patient
		fields = ['name','code','dated','remedy','pic']
