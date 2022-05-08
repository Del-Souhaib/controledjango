from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from allout_souhaib.forms import *
from allout_souhaib.models import *


######################"# Home page ###############################
def dashboard(request):
    if request.user.is_authenticated:
        dates = RenderVous.objects.filter(date=datetime.date.today()).order_by('-id')
        nbdocteur=Medecin.objects.count()
        nbpatients=Patient.objects.count()
        nbadmins=User.objects.count()
        nbrndezvous=RenderVous.objects.count()

        p = Paginator(dates, 10)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        context = {'page_obj': page_obj, 'title': 'index','nbdocteur':nbdocteur,'nbpatients':nbpatients,
                   'nbadmins':nbadmins,'nbrndezvous':nbrndezvous}

        return render(request, "index.html",context)
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
    if request.user.is_authenticated==False:
        return redirect('/login')
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
    if request.user.is_authenticated==False:
        return redirect('/login')

    pateint = Patient.objects.get(id=id)
    context = {'patient': pateint}
    return render(request, 'patients/details.html', context)


def patientsdelete(request, id):
    if request.user.is_authenticated==False:
        return redirect('/login')

    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return redirect('/patients')
    patient.delete()
    return redirect('/patients')


def addPatient(request):
    if request.user.is_authenticated==False:
        return redirect('/login')

    if request.method == 'POST':
        form=PatientForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.create(nom=form.cleaned_data['nom'], prenom=form.cleaned_data['prenom'],
                                             email=form.cleaned_data['email'],
                                             dateNaissance=form.cleaned_data['dateNaissance'])
            patient.save()
            return HttpResponseRedirect("/patients")
        else:
            return render(request, "patients/add.html", {'form': form})
    else:
        form = PatientForm()
        return render(request, "patients/add.html", {'form': form})


def editPatient(request, id):
    if request.user.is_authenticated==False:
        return redirect('/login')

    patient = Patient.objects.get(id=id)
    if request.method == 'POST':
        form=PatientForm(request.POST)
        if form.is_valid():
            patient.nom = form.cleaned_data['nom']
            patient.prenom = form.cleaned_data['prenom']
            patient.email = form.cleaned_data['email']
            patient.dateNaissance = form.cleaned_data['dateNaissance']
            patient.save()
            return redirect('/patients')
        else:
            context = {"form": form}
            return render(request, "patients/edit.html", context)

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
    if request.user.is_authenticated==False:
        return redirect('/login')

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
    if request.user.is_authenticated==False:
        return redirect('/login')

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
    if request.user.is_authenticated==False:
        return redirect('/login')

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
    if request.user.is_authenticated==False:
        return redirect('/login')

    medecine = Medecin.objects.get(id=id)
    form = MedecinForm()
    form['id'].initial = medecine.id
    form['nom'].initial = medecine.nom
    form['prenom'].initial = medecine.prenom
    form['specialite'].initial = medecine.specialite
    context = {'medecine': medecine}
    return render(request, 'medecines/details.html', context)


def docteursdelete(request, id):
    if request.user.is_authenticated==False:
        return redirect('/login')

    try:
        medecine = Medecin.objects.get(id=id)
    except Medecin.DoesNotExist:
        return redirect('/medecines')
    medecine.delete()
    return redirect('/medecines')


def adddocteur(request):
    if request.user.is_authenticated==False:
        return redirect('/login')

    if request.method == 'POST':
        form=MedecinForm(request.POST)
        if form.is_valid():
            medecine = Medecin.objects.create(nom=form.cleaned_data['nom'], prenom=form.cleaned_data['prenom'],
                                             specialite=form.cleaned_data['specialite'])
            medecine.save()
            return redirect("/medecines")
        else:
            return render(request, "medecines/add.html", {'form': form})

    else:
        form = MedecinForm()
        return render(request, "medecines/add.html", {'form': form})


def editdocteur(request, id):
    if request.user.is_authenticated==False:
        return redirect('/login')

    medecine = Medecin.objects.get(id=id)
    if request.method == 'POST':
        form=MedecinForm(request.POST)
        if form.is_valid():
            medecine.nom = form.cleaned_data['nom']
            medecine.prenom = form.cleaned_data['prenom']
            medecine.specialite = form.cleaned_data['specialite']
            medecine.save()
            return redirect('/medecines')
        else:
            context = {"form": form}
            return render(request, "medecines/edit.html", context)

    else:
        form = MedecinForm()
        form['id'].initial = medecine.id
        form['nom'].initial = medecine.nom
        form['prenom'].initial = medecine.prenom
        form['specialite'].initial = medecine.specialite

        context = {"form": form}
        return render(request, "medecines/edit.html", context)


def docteurssearch(request):
    if request.user.is_authenticated==False:
        return redirect('/login')

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
    if request.user.is_authenticated==False:
        return redirect('/login')

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
    if request.user.is_authenticated==False:
        return redirect('/login')

    date = RenderVous.objects.get(id=id)
    form = MedecinForm()
    context = {'date': date}
    return render(request, 'dates/details.html', context)


def datesdelete(request, id):
    if request.user.is_authenticated==False:
        return redirect('/login')

    try:
        date = RenderVous.objects.get(id=id)
    except Medecin.DoesNotExist:
        return redirect('/dates')
    date.delete()
    return redirect('/dates')


def adddates(request):
    if request.user.is_authenticated==False:
        return redirect('/login')

    if request.method == 'POST':
        form=DateForm(request.POST)
        if form.is_valid():
            rendzevous = RenderVous.objects.create(patient=form.cleaned_data['patient'],
                                                   medecin=form.cleaned_data['medecin'],
                                                   date=form.cleaned_data['date'],
                                                   consultation=form.cleaned_data['consultation'], anuuler=False)
            rendzevous.save()

            return redirect("/dates")
        else:
            return render(request, "dates/add.html", {'form': form})



    else:
        form = DateForm()
        return render(request, "dates/add.html", {'form': form})


def editdates(request, id):
    if request.user.is_authenticated==False:
        return redirect('/login')

    date = RenderVous.objects.get(id=id)
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            date.patient = form.cleaned_data['patient']
            date.medecin = form.cleaned_data['medecin']
            date.consultation = form.cleaned_data['consultation']
            date.date = form.cleaned_data['date']
            if form.cleaned_data["anuuler"]:
                date.anuuler = 1
            else:
                date.annuler = 0

            date.save()

            return redirect('/dates')
        else:
            context = {"form": form}
            return render(request, "dates/edit.html", context)

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
    if request.user.is_authenticated==False:
        return redirect('/login')

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
