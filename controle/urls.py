"""controle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from allout_souhaib import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.dashboard),

    # ##################### auth #####################

    path('login', views.loginpage),
    path('loginclick', views.loginclick),
    path('logoutclick', views.logoutclick),

    # ##################### patients #####################
    path('patients/', views.patientsindex),
    path('patients/details/<int:id>', views.patientsdetails),

    path('patients/create', views.addPatient),

    path('patients/edit/<int:id>', views.editPatient),
    path('patients/delete/<int:id>', views.patientsdelete),
    path('patients/search', views.patientssearch),

    ############### Docteurs #####################

    path('medecines/', views.docteursindex),
    path('medecines/details/<int:id>', views.docteursdetails),

    path('medecines/create', views.adddocteur),

    path('medecines/edit/<int:id>', views.editdocteur),
    path('medecines/delete/<int:id>', views.docteursdelete),
    path('medecines/search', views.docteurssearch),

    ############### Rendez-vous #####################

    path('dates/', views.datesindex),
    path('dates/details/<int:id>', views.datesdetails),

    path('dates/add', views.adddates),

    path('dates/edit/<int:id>', views.editdates),
    path('dates/delete/<int:id>', views.datesdelete),
    path('dates/search', views.datessearch),

]
