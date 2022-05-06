from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite

from allout_souhaib.models import *

admin.site.site_header = 'allout clinique'

class AdminPatient(admin.ModelAdmin):
    list_display = ['nom','prenom','email','dateNaissance']
    list_filter = ['dateNaissance']
    search_fields = ['nom','prenom','email']

admin.site.register(Patient,AdminPatient)

class AdminMedecine(admin.ModelAdmin):
    list_display = ['nom','prenom','specialite']
    list_filter = ['specialite']
    search_fields = ['nom','prenom']


admin.site.register(Medecin,AdminMedecine)


class AdminConsultation(admin.ModelAdmin):
    list_display = ['type','description','traitement']
    list_filter = ['type','traitement']
    search_fields = ['description']

admin.site.register(Consultation,AdminConsultation)


class AdminDate(admin.ModelAdmin):
    list_display = ['date','medecin','patient','consultation','anuuler']
    list_filter = ['medecin','anuuler','date']
    search_fields = ['date','medecin','patient','consultation']


admin.site.register(RenderVous,AdminDate)
