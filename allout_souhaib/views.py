from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from allout_souhaib.forms import *
from allout_souhaib.models import *


######################"# Home page ###############################
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return redirect('/login')


######################"# Auth ###############################


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, "auth/login.html")


def loginclick(request):
    if (request.method == 'POST'):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'username our mot de passe est inccorect')
            # messages.error(request,request.POST['username']+" "+request.POST['password'])
            return redirect('/login')
    else:
        messages.error(request, 'login again')

        return redirect('/login')


def logoutclick(request):
    if (request.user.is_authenticated and request.method == 'POST'):
        logout(request)
        return redirect('/login')
    else:
        return redirect('/')


######################"# Patients ###############################


def patientsindex(request):
    patients = Patient.objects.order_by('-id').all()

    p = Paginator(patients, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'title': 'liste des patients'}
    return render(request, "patients/index.html", context)


def patientsdetails(request, id):
    pateint = Patient.objects.get(id=id)
    context = {'patient': pateint}
    return render(request, 'patients/details.html', context)


def patientsdelete(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return redirect('/patients')
    patient.delete()
    return redirect('/patients')


def addPatient(request):
    if request.method == 'POST':
        nom = request.POST.get("nom", "").capitalize()
        prenom = request.POST.get("prenom", "")
        email = request.POST.get("email", "")
        dateNaissance = request.POST.get("dateNaissance")
        patient = Patient.objects.create(nom=nom, prenom=prenom, email=email, dateNaissance=dateNaissance)
        patient.save()
        return redirect("/patients")
    else:
        form = PatientForm()
        return render(request, "patients/add.html", {'form': form})


def editPatient(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == 'POST':
        nom = request.POST.get("nom", "").capitalize()
        prenom = request.POST.get("prenom", "")
        email = request.POST.get("email", "")
        dateNaissance = request.POST.get("dateNaissance")

        patient.nom = nom
        patient.prenom = prenom
        patient.email = email
        patient.dateNaissance = dateNaissance
        patient.save()
        return redirect('/patients')
    else:
        form = PatientForm()
        form['id'].initial = patient.id
        form['nom'].initial = patient.nom
        form['prenom'].initial = patient.prenom
        form['dateNaissance'].initial = patient.dateNaissance
        form['email'].initial = patient.email

        context = {"form": form}
        return render(request, "patients/edit.html", context)


def patientsupdate(request):
    id = request.POST.get("id", "")
    nom = request.POST.get("nom", "").capitalize()
    prenom = request.POST.get("prenom", "")
    email = request.POST.get("email", "")
    dateNaissance = request.POST.get("dateNaissance")

    patient = Patient.objects.get(id=id)
    patient.nom = nom
    patient.prenom = prenom
    patient.email = email
    patient.dateNaissance = dateNaissance
    patient.save()
    return redirect('/patients')


def patientssearch(request):
    # on récupere les données du model Patient
    search = request.GET.get('search_text')
    patients = Patient.objects.filter(nom__contains=search)
    p = Paginator(patients, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'title': search}
    return render(request, "patients/index.html", context)


######################"# Docteurs ###############################


def docteursindex(request):
    medecines = Medecin.objects.order_by('-id').all()

    p = Paginator(medecines, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'title': 'liste des medecines'}
    return render(request, "medecines/index.html", context)


def docteursdetails(request, id):
    medecine = Medecin.objects.get(id=id)
    form = MedecinForm()
    form['id'].initial = medecine.id
    form['nom'].initial = medecine.nom
    form['prenom'].initial = medecine.prenom
    form['specialite'].initial = medecine.specialite
    context = {'medecine': medecine}
    return render(request, 'medecines/details.html', context)


def docteursdelete(request, id):
    try:
        medecine = Medecin.objects.get(id=id)
    except Medecin.DoesNotExist:
        return redirect('/medecines')
    medecine.delete()
    return redirect('/medecines')


def adddocteur(request):
    if request.method == 'POST':
        nom = request.POST.get("nom", "").capitalize()
        prenom = request.POST.get("prenom", "")
        specialite = request.POST.get("specialite", "")
        medecine = Medecin.objects.create(nom=nom, prenom=prenom, specialite=specialite)
        medecine.save()
        return redirect("/medecines")
    else:
        form = MedecinForm()
        return render(request, "medecines/add.html", {'form': form})


def editdocteur(request, id):
    medecine = Medecin.objects.get(id=id)
    if request.method == 'POST':
        nom = request.POST.get("nom", "").capitalize()
        prenom = request.POST.get("prenom", "")
        specialite = request.POST.get("specialite", "")

        medecine.nom = nom
        medecine.prenom = prenom
        medecine.specialite = specialite
        medecine.save()
        return redirect('/medecines')
    else:
        form = MedecinForm()
        form['id'].initial = medecine.id
        form['nom'].initial = medecine.nom
        form['prenom'].initial = medecine.prenom
        form['specialite'].initial = medecine.specialite

        context = {"form": form}
        return render(request, "medecines/edit.html", context)


def docteurssearch(request):
    # on récupere les données du model Patient
    search = request.GET.get('search_text')
    medecines = Medecin.objects.filter(nom__contains=search)
    p = Paginator(medecines, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'title': search}
    return render(request, "medecines/index.html", context)


######################"# Rendez-vous ###############################


def datesindex(request):
    dates = RenderVous.objects.order_by('-id').all()
    p = Paginator(dates, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'title': 'liste des dates'}
    return render(request, "dates/index.html", context)


def datesdetails(request, id):
    date = RenderVous.objects.get(id=id)
    form = MedecinForm()
    # form['id'].initial = date.id
    # form['nom'].initial = medecine.nom
    # form['prenom'].initial = medecine.prenom
    # form['specialite'].initial = medecine.specialite
    context = {'date': date}
    return render(request, 'dates/details.html', context)


def datesdelete(request, id):
    try:
        date = RenderVous.objects.get(id=id)
    except Medecin.DoesNotExist:
        return redirect('/dates')
    date.delete()
    return redirect('/dates')


def adddates(request):
    if request.method == 'POST':
        patient = Patient.objects.get(id=request.POST.get("patient", "").capitalize())
        medecine = Medecin.objects.get(id=request.POST.get("medecin", ""))
        consultation = Consultation.objects.get(id=request.POST.get("consultation", ""))
        date = request.POST.get("date", "")

        rendzevous = RenderVous.objects.create(patient=patient, medecin=medecine,date=date,
                                               consultation=consultation, anuuler=False)
        rendzevous.save()
        return redirect("/dates")
    else:
        form = DateForm()
        return render(request, "dates/add.html", {'form': form})


def editdates(request, id):
    date = RenderVous.objects.get(id=id)
    if request.method == 'POST':
        patient = Patient.objects.get(id=request.POST.get("patient", "").capitalize())
        medecine = Medecin.objects.get(id=request.POST.get("medecin", ""))
        consultation = Consultation.objects.get(id=request.POST.get("consultation", ""))
        date_re = request.POST.get("date", "")
        annuler = request.POST.get("anuuler", "")
        if annuler=='on':
            date.anuuler = True
        else:
            date.anuuler = False

        date.patient = patient
        date.medecin = medecine
        date.consultation = consultation
        date.date = date_re

        date.save()
        return redirect('/dates')
    else:
        form = DateForm()
        form['id'].initial = date.id
        form['date'].initial = date.date
        form['anuuler'].initial = date.anuuler
        form['medecin'].initial = date.medecin
        form['patient'].initial = date.patient
        form['consultation'].initial = date.consultation

        context = {"form": form}
        return render(request, "dates/edit.html", context)


def datessearch(request):
    # on récupere les données du model Patient
    search = request.GET.get('search_text')
    dates = RenderVous.objects.filter(date=search)
    p = Paginator(dates, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'title': search}
    return render(request, "dates/index.html", context)
