from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from study_app.forms import FeedbackForm
from study_app.models import MathMain, PhysicsMain, ChemMain, CompSciMain

# Create your views here.
def login_user(request):
    math_grades = MathMain.objects.all().order_by('date_added')
    physics_grades = PhysicsMain.objects.all().order_by('date_added')
    chem_grades = ChemMain.objects.all().order_by('date_added')
    compsci_grades = CompSciMain.objects.all().order_by('date_added')

    feedback_form = FeedbackForm()

    if request.method == "GET":
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "you have logged in")
            return redirect("main:home")
        messages.error(request, "Something was wrong with your information")

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "form":form,
        'feedback_form':feedback_form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    referer = request.META.get("HTTP_REFERER")
    logout(request)
    messages.success(request, "You have Logged Out")

    return HttpResponseRedirect(referer)

def register(request):
    math_grades = MathMain.objects.all().order_by('date_added')
    physics_grades = PhysicsMain.objects.all().order_by('date_added')
    chem_grades = ChemMain.objects.all().order_by('date_added')
    compsci_grades = CompSciMain.objects.all().order_by('date_added')

    feedback_form = FeedbackForm
    if request.method != "POST":
        form = UserCreationForm
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, "you have created an account")
            return redirect("main:home")
        messages.error(request, "Something was wrong with your information")

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "form":form,
        "feedback_form": feedback_form,
    }
    return render(request, "register.html", context)
