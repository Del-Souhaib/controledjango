import datetime

from django import forms

from allout_souhaib.models import *


class PatientForm(forms.Form):
    id = forms.IntegerField(label='id', widget=forms.HiddenInput())
    nom = forms.CharField(label='Nom', required=True, max_length=100,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom = forms.CharField(label='Prenom', required=True, max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=True, max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    dateNaissance = forms.CharField(label='Date de naissance', required=True,
                                    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))


class MedecinForm(forms.Form):
    id = forms.IntegerField(label='id', widget=forms.HiddenInput())
    nom = forms.CharField(label='Nom', required=True, max_length=100,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom = forms.CharField(label='Prenom', required=True, max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialite_choices = [
        ('General', 'General'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Dermatology', 'Dermatology'),
        ('Diagnostic radiology', 'Diagnostic radiology'),
        ('Medical genetics', 'Medical genetics'),
        ('Internal medicine', 'Internal medicine'),
    ]

    specialite = forms.ChoiceField(label='Specialite', choices=specialite_choices,
                                   widget=forms.Select(attrs={'class': 'form-select'}))


class DateForm(forms.Form):
    id = forms.IntegerField(label='id', widget=forms.HiddenInput())
    date = forms.DateField(label='Date', required=True,
                           widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date','min':datetime.date.today()}))
    anuuler = forms.BooleanField(label='Annuler',required=False,
                                 widget=forms.CheckboxInput(attrs={'class': 'form-check-input','type':'checkbox'}))
    medecin = forms.ModelChoiceField(queryset=Medecin.objects.all(), label='Medecin', required=True
                                     ,widget=forms.Select(attrs={'class': 'form-select'}))
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), label='Patient', required=True
                                     ,widget=forms.Select(attrs={'class': 'form-select'}))
    consultation = forms.ModelChoiceField(queryset=Consultation.objects.all(), label='Consultation'
                                          ,widget=forms.Select(attrs={'class': 'form-select'}), required=True)
