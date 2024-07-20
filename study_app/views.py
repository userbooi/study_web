from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Feedback, MathMain, PhysicsMain, ChemMain, CompSciMain, MathUnit, MathSubUnit, \
    PhysicsUnit, PhysicsSubUnit, ChemUnit, ChemSubUnit, CompSciUnit, CompSciSubUnit, MultipleChoiceQuestion, \
    MultipleChoiceQuiz, MultipleChoiceChoice
from .forms import FeedbackForm, MathUnitForm, MathSubUnitForm, PhysicsUnitForm, PhysicsSubUnitForm, ChemUnitForm, \
    ChemSubUnitForm, CompSciSubUnitForm, CompSciUnitForm, MultipleChoiceQuizForm, MultipleChoiceQuestionForm, \
    MultipleChoiceChoiceForm, MainsForms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import base64

import json, random

# Create your views here.
def home(request):
    math_grades = MathMain.objects.all().order_by('date_added')
    physics_grades = PhysicsMain.objects.all().order_by('date_added')
    chem_grades = ChemMain.objects.all().order_by('date_added')
    compsci_grades = CompSciMain.objects.all().order_by('date_added')

    feedback_form = FeedbackForm()

    context = {
        "feedback_form": feedback_form,
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,
    }
    return render(request, "home.html", context)

def math(request):
    if request.method != "POST":
        math = []
        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')

        for main in MathMain.objects.all().order_by('date_added'):
            math.append([main.title, base64.b64encode(bytes(main.image)).decode('utf-8'), main.id])

        feedback_form = FeedbackForm()
        math_main_form = MainsForms()
    else:
        math_main_form = MainsForms(request.POST, request.FILES)
        if math_main_form.is_valid():
            title = math_main_form.cleaned_data["title"]
            image = math_main_form.cleaned_data["image"]
            MathMain.objects.create(title=title, image=image.read())
            messages.success(request, "successfully added")
            return redirect("main:math")
        messages.success(request, "something went wrong")
        return redirect("main:math")

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "math": math,

        "feedback_form": feedback_form,
        "math_main_form": math_main_form
    }
    return render(request, "math.html", context)

def study_math(request, id):
    if request.method != "POST":
        current_url = request.resolver_match.view_name

        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')
        grade = MathMain.objects.get(pk=id)

        units = grade.mathunit_set.order_by("id")
        subunits = MathSubUnit.objects.all().order_by("id")
        subs = []
        for subunit in subunits:
            if subunit.image:
                subs.append([subunit.title,
                             subunit.unit,
                             subunit.description,
                             base64.b64encode(bytes(subunit.image)).decode('utf-8'),
                             subunit.id])
            else:
                subs.append([subunit.title,
                             subunit.unit,
                             subunit.description,
                             None,
                             subunit.id])

        feedback_form = FeedbackForm()
        unit_form = MathUnitForm()
        subunit_form = MathSubUnitForm()
    else:
        if "unit" in request.POST and "subunit" not in request.POST:
            grade = MathMain.objects.get(pk=id)

            unit_form = MathUnitForm(data=request.POST)
            if unit_form.is_valid():
                new_unit = unit_form.save(commit=False)
                new_unit.id = MathUnit.objects.count() + 1
                new_unit.subject = grade
                new_unit.save()
                messages.success(request, "successfully added")
                return redirect("main:study_math", id=id)
        else:
            subunit_form = MathSubUnitForm(request.POST, request.FILES)
            if subunit_form.is_valid():
                new_subunit = subunit_form.save(commit=False)
                new_subunit.id = MathSubUnit.objects.count() + 1
                if request.FILES:
                    new_subunit.image = subunit_form.cleaned_data["image"].read()
                new_subunit.save()
                messages.success(request, "successfully added")
                return redirect("main:study_math", id=id)
        messages.error(request, "something went wrong")
        return redirect("main:study_math", id=id)

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "grade": grade,
        "feedback_form": feedback_form,
        "unit_form": unit_form,
        "subunit_form": subunit_form,

        "units": units,
        "subunits": subs,

        "current_url": current_url
    }

    return render(request, 'study.html', context)

def test(request, subject, unit):
    u = unit.replace("%20", " ")
    s = subject.replace("%20", " ")
    if request.method != "POST":
        current_url = request.resolver_match.view_name

        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')

        feedback_form = FeedbackForm()
        if not MultipleChoiceQuiz.objects.filter(unit=u):
            multiple_choice_quiz_form = MultipleChoiceQuizForm(initial={"unit": u})
        else:
            multiple_choice_quiz_form = None
            quiz = MultipleChoiceQuiz.objects.get(unit=u)
            questions = list(quiz.questions.all())
            choices = list(MultipleChoiceChoice.objects.all())

            js_data = []
            for question in questions:
                a = []
                for choice in question.choices.all():
                    a.append(choice.choice)
                js_data.append({question.title: a})
            random.shuffle(js_data)
            js_data = js_data[:quiz.number_of_questions]
            # print(js_data)

        multiple_choice_question_form = MultipleChoiceQuestionForm()
        multiple_choice_choice_form = MultipleChoiceChoiceForm()
    else:
        if "quiz" in request.POST and "question" not in request.POST:
            multiple_choice_quiz_form = MultipleChoiceQuizForm(data=request.POST)
            if multiple_choice_quiz_form.is_valid():
                multiple_choice_quiz_form.save()
                messages.success(request, "successfully added")
                return redirect("main:test", subject=s , unit=u)
        elif "question" in request.POST and "choice" not in request.POST:
            multiple_choice_question_form = MultipleChoiceQuestionForm(data=request.POST)
            if multiple_choice_question_form.is_valid():
                multiple_choice_question_form.save()
                messages.success(request, "successfully added")
                return redirect("main:test", subject=s, unit=u)
        else:
            multiple_choice_choice_form = MultipleChoiceChoiceForm(data=request.POST)
            if multiple_choice_choice_form.is_valid():
                multiple_choice_choice_form.save()
                messages.success(request, "successfully added")
                return redirect("main:test", subject=s, unit=u)
        messages.error(request, "something went wrong")
        return redirect("main:test", subject=s, unit=u)

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "feedback_form": feedback_form,
        "multiple_choice_quiz_form": multiple_choice_quiz_form,
        "multiple_choice_question_form": multiple_choice_question_form,
        "multiple_choice_choice_form": multiple_choice_choice_form,

        "current_url": current_url,
        "unit": u,
        "subject": s
    }

    if MultipleChoiceQuiz.objects.filter(unit=u):
        context = context | {
                             'quiz':quiz,
                             'questions':questions,
                             'choices':choices,
                             'js_data': json.dumps(js_data),
                            }

    return render(request, "test.html", context)

def test_check(request, subject, unit):
    u = unit.replace("%20", " ")
    data = dict(request.POST)
    correct = False
    correct_answer = None
    for k, v in data.items():
        if k == "csrfmiddlewaretoken":
            continue
        else:
            correct_answer = MultipleChoiceQuiz.objects.get(unit=u).questions.get(title=k).choices.get(correct=True)
            if v == ['']:
                break
            answer = MultipleChoiceQuiz.objects.get(unit=u).questions.get(title=k).choices.get(choice=v[-1])
            correct = answer.correct
    return JsonResponse({"status": correct, "correct_answer": correct_answer.choice})
    # return JsonResponse({"it": "worked"})

def physics(request):
    if request.method != "POST":
        physics = []
        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')

        for main in PhysicsMain.objects.all().order_by('date_added'):
            physics.append([main.title, base64.b64encode(bytes(main.image)).decode('utf-8'), main.id])

        feedback_form = FeedbackForm()
        physics_main_form = MainsForms()
    else:
        physics_main_form = MainsForms(request.POST, request.FILES)
        if physics_main_form.is_valid():
            title = physics_main_form.cleaned_data["title"]
            image = physics_main_form.cleaned_data["image"]
            PhysicsMain.objects.create(title=title, image=image.read())
            messages.success(request, "successfully added")
            return redirect("main:physics")
        messages.success(request, "something went wrong")
        return redirect("main:physics")

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "physics": physics,

        "feedback_form": feedback_form,
        "physics_main_form": physics_main_form
    }
    return render(request, "physics.html", context)

def study_physics(request, id):
    if request.method != "POST":
        current_url = request.resolver_match.view_name

        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')
        grade = PhysicsMain.objects.get(pk=id)

        units = grade.physicsunit_set.order_by("id")
        subunits = PhysicsSubUnit.objects.all().order_by("id")
        subs = []
        for subunit in subunits:
            if subunit.image:
                subs.append([subunit.title,
                             subunit.unit,
                             subunit.description,
                             base64.b64encode(bytes(subunit.image)).decode('utf-8'),
                             subunit.id])
            else:
                subs.append([subunit.title,
                             subunit.unit,
                             subunit.description,
                             None,
                             subunit.id])

        feedback_form = FeedbackForm()
        unit_form = PhysicsUnitForm()
        subunit_form = PhysicsSubUnitForm()
    else:
        if "unit" in request.POST and "subunit" not in request.POST:
            grade = PhysicsMain.objects.get(pk=id)

            unit_form = PhysicsUnitForm(data=request.POST)
            if unit_form.is_valid():
                new_unit = unit_form.save(commit=False)
                new_unit.id = PhysicsUnit.objects.count() + 1
                new_unit.subject = grade
                new_unit.save()
                messages.success(request, "successfully added")
                return redirect("main:study_physics", id=id)
            messages.error(request, "something went wrong")
            return redirect("main:study_physics", id=id)
        else:
            subunit_form = PhysicsSubUnitForm(request.POST, request.FILES)
            if subunit_form.is_valid():
                new_subunit = subunit_form.save(commit=False)
                new_subunit.id = PhysicsSubUnit.objects.count() + 1
                if request.FILES:
                    new_subunit.image = subunit_form.cleaned_data["image"].read()
                # print(subunit_form.cleaned_data["description"])
                new_subunit.save()
                messages.success(request, "successfully added")
                return redirect("main:study_physics", id=id)
            messages.error(request, "something went wrong")
            return redirect("main:study_physics", id=id)

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "grade": grade,
        "feedback_form": feedback_form,
        "unit_form": unit_form,
        "subunit_form": subunit_form,

        "units": units,
        "subunits": subs,

        "current_url": current_url
    }

    return render(request, 'study.html', context)

def chemistry(request):
    if request.method != "POST":
        chem = []
        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')

        for main in ChemMain.objects.all().order_by('date_added'):
            chem.append([main.title, base64.b64encode(bytes(main.image)).decode('utf-8'), main.id])

        feedback_form = FeedbackForm()
        chem_main_form = MainsForms()
    else:
        chem_main_form = MainsForms(request.POST, request.FILES)
        if chem_main_form.is_valid():
            title = chem_main_form.cleaned_data["title"]
            image = chem_main_form.cleaned_data["image"]
            ChemMain.objects.create(title=title, image=image.read())
            messages.success(request, "successfully added")
            return redirect("main:chemistry")
        messages.success(request, "something went wrong")
        return redirect("main:chemistry")

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "chem": chem,

        "feedback_form": feedback_form,
        "chem_main_form": chem_main_form
    }
    return render(request, "chemistry.html", context)

def study_chemistry(request, id):
    if request.method != "POST":
        current_url = request.resolver_match.view_name

        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')
        grade = ChemMain.objects.get(pk=id)

        units = grade.chemunit_set.order_by("id")
        subunits = ChemSubUnit.objects.all().order_by("id")
        subs = []
        for subunit in subunits:
            if subunit.image:
                subs.append([subunit.title,
                             subunit.unit,
                             subunit.description,
                             base64.b64encode(bytes(subunit.image)).decode('utf-8'),
                             subunit.id])
            else:
                subs.append([subunit.title,
                             subunit.unit,
                             subunit.description,
                             None,
                             subunit.id])

        feedback_form = FeedbackForm()
        unit_form = ChemUnitForm()
        subunit_form = ChemSubUnitForm()
    else:
        if "unit" in request.POST and "subunit" not in request.POST:
            grade = ChemMain.objects.get(pk=id)

            unit_form = ChemUnitForm(data=request.POST)
            if unit_form.is_valid():
                new_unit = unit_form.save(commit=False)
                new_unit.id = ChemUnit.objects.count() + 1
                new_unit.subject = grade
                new_unit.save()
                messages.success(request, "successfully added")
                return redirect("main:study_chemistry", id=id)
            messages.error(request, "something went wrong")
            return redirect("main:study_chemistry", id=id)
        else:
            subunit_form = ChemSubUnitForm(request.POST, request.FILES)
            if subunit_form.is_valid():
                new_subunit = subunit_form.save(commit=False)
                new_subunit.id = ChemSubUnit.objects.count() + 1
                if request.FILES:
                    new_subunit.image = subunit_form.cleaned_data["image"].read()
                new_subunit.save()
                messages.success(request, "successfully added")
                return redirect("main:study_chemistry", id=id)
            messages.error(request, "something went wrong")
            return redirect("main:study_chemistry", id=id)

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "grade": grade,
        "feedback_form": feedback_form,
        "unit_form": unit_form,
        "subunit_form": subunit_form,

        "units": units,
        "subunits": subs,

        "current_url": current_url
    }

    return render(request, 'study.html', context)

def compsci(request):
    if request.method != "POST":
        compsci = []
        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')

        for main in CompSciMain.objects.all().order_by('date_added'):
            compsci.append([main.title, base64.b64encode(bytes(main.image)).decode('utf-8'), main.id])

        feedback_form = FeedbackForm()
        compsci_main_form = MainsForms()
    else:
        compsci_main_form = MainsForms(request.POST, request.FILES)
        if compsci_main_form.is_valid():
            title = compsci_main_form.cleaned_data["title"]
            image = compsci_main_form.cleaned_data["image"]
            CompSciMain.objects.create(title=title, image=image.read())
            messages.success(request, "successfully added")
            return redirect("main:compsci")
        messages.success(request, "something went wrong")
        return redirect("main:compsci")

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "compsci": compsci,

        "feedback_form": feedback_form,
        "compsci_main_form": compsci_main_form
    }
    return render(request, "compsci.html", context)

def study_compsci(request, id):
    if request.method != "POST":
        current_url = request.resolver_match.view_name

        math_grades = MathMain.objects.all().order_by('date_added')
        physics_grades = PhysicsMain.objects.all().order_by('date_added')
        chem_grades = ChemMain.objects.all().order_by('date_added')
        compsci_grades = CompSciMain.objects.all().order_by('date_added')
        grade = CompSciMain.objects.get(pk=id)

        units = grade.compsciunit_set.order_by("id")
        subunits = CompSciSubUnit.objects.all().order_by("id")
        subs = []
        for subunit in subunits:
            if subunit.image:
                subs.append([subunit.title,
                             subunit.unit,
                             subunit.description,
                             base64.b64encode(bytes(subunit.image)).decode('utf-8'),
                             subunit.id])
            else:
                subs.append([subunit.title,
                             subunit.unit,
                             subunit.description,
                             None,
                             subunit.id])

        feedback_form = FeedbackForm()
        unit_form = CompSciUnitForm()
        subunit_form = CompSciSubUnitForm()
    else:
        if "unit" in request.POST and "subunit" not in request.POST:
            grade = CompSciMain.objects.get(pk=id)

            unit_form = CompSciUnitForm(data=request.POST)
            if unit_form.is_valid():
                new_unit = unit_form.save(commit=False)
                new_unit.id = CompSciUnit.objects.count() + 1
                new_unit.subject = grade
                new_unit.save()
                messages.success(request, "successfully added")
                return redirect("main:study_compsci", id=id)
            messages.error(request, "something went wrong")
            return redirect("main:study_compsci", id=id)
        else:
            subunit_form = CompSciSubUnitForm(request.POST, request.FILES)
            if subunit_form.is_valid():
                new_subunit = subunit_form.save(commit=False)
                new_subunit.id = CompSciSubUnit.objects.count() + 1
                if request.FILES:
                    new_subunit.image = subunit_form.cleaned_data["image"].read()
                new_subunit.save()
                messages.success(request, "successfully added")
                return redirect("main:study_compsci", id=id)
            messages.error(request, "something went wrong")
            return redirect("main:study_compsci", id=id)

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "grade": grade,
        "feedback_form": feedback_form,
        "unit_form": unit_form,
        "subunit_form": subunit_form,

        "units": units,
        "subunits": subs,

        "current_url": current_url
    }

    return render(request, 'study.html', context)

def feedback(request):
    math_grades = MathMain.objects.all().order_by('date_added')
    physics_grades = PhysicsMain.objects.all().order_by('date_added')
    chem_grades = ChemMain.objects.all().order_by('date_added')
    compsci_grades = CompSciMain.objects.all().order_by('date_added')
    feedback_form = FeedbackForm()

    feedbacks = Feedback.objects.all()
    feedbacks = feedbacks.order_by('date_added')
    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "feedbacks": feedbacks,
        "feedback_form": feedback_form,
    }

    return render(request, "feedback.html", context)

def add_feedback(request):
    # print(request.POST)
    form = FeedbackForm(data=request.POST)
    referer = request.META.get("HTTP_REFERER")
    if form.is_valid():
        feedback_object = form.save(commit=False)
        if request.user.is_authenticated:
            feedback_object.owner = request.user.username
        else:
            feedback_object.owner = "anonymous"
        feedback_object.save()
        messages.success(request, "Thanks for The Feedback")
        return HttpResponseRedirect(referer)
    return HttpResponseRedirect(referer)

def feedback_delete(request, id):
    feedback_ = Feedback.objects.get(pk=id)
    feedback_.delete()

    return redirect("main:feedback")

def game(request):
    math_grades = MathMain.objects.all().order_by('date_added')
    physics_grades = PhysicsMain.objects.all().order_by('date_added')
    chem_grades = ChemMain.objects.all().order_by('date_added')
    compsci_grades = CompSciMain.objects.all().order_by('date_added')
    feedback_form = FeedbackForm()

    context = {
        "math_grades": math_grades,
        "physics_grades": physics_grades,
        "chem_grades": chem_grades,
        "compsci_grades": compsci_grades,

        "feedback_form": feedback_form
    }
    return render(request, "game.html", context)

@login_required
def testing(request):
    feedback_form = FeedbackForm()

    context = {
        "hi":"hi",
        "feedback_form": feedback_form
    }
    return render(request, "testing.html", context)

# def get_data(request, unit):

