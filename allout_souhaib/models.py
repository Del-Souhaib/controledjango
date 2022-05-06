from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Patient(models.Model):
    nom = models.CharField(max_length=45)
    prenom = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    dateNaissance = models.DateField(null=True)

    def __str__(self):
        return self.nom+" "+self.prenom


class Medecin(models.Model):
    nom = models.CharField(max_length=45)
    prenom = models.CharField(max_length=45)
    specialite_choices = [
        ('General', 'General'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Dermatology', 'Dermatology'),
        ('Diagnostic radiology', 'Diagnostic radiology'),
        ('Medical genetics', 'Medical genetics'),
        ('Internal medicine', 'Internal medicine'),
    ]
    specialite = models.CharField(max_length=45, choices=specialite_choices)
    def __str__(self):
        return self.nom+" "+self.prenom


class RenderVous(models.Model):
    date = models.DateField(null=True)
    anuuler = models.BooleanField(default=False,null=True)
    medecin = models.ForeignKey('Medecin', on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    consultation = models.ForeignKey('Consultation', on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.nom


class Consultation(models.Model):
    consultation_choices = [
        ('Présentielle', 'Présentielle'),
        ('Distantielle', 'Distantielle'),
    ]
    type = models.CharField(max_length=45, choices=consultation_choices)
    description = models.CharField(max_length=300)
    traitement = models.CharField(max_length=100)
    def __str__(self):
        return self.type+" "+self.traitement

