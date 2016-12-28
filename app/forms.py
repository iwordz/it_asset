__author__ = 'fanghouguo'
#coding=utf-8
from django import forms

class RackForm(forms.Form):
    idc_name = forms.CharField()
    rack_number = forms.IntegerField()
    start_time = forms.IntegerField()
    end_time = forms.IntegerField()
    provider_service = forms.CharField()



class LoginForm(forms.Form):
    user_name = forms.CharField()
    passs_word = forms.PasswordInput()

