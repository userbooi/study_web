from django import forms
from .models import Feedback, MathMain, PhysicsMain, ChemMain, CompSciMain, MathUnit, MathSubUnit, PhysicsUnit, \
    PhysicsSubUnit, ChemUnit, ChemSubUnit, CompSciUnit, CompSciSubUnit, MultipleChoiceQuiz, MultipleChoiceQuestion, \
    MultipleChoiceChoice

class MainsForms(forms.Form):
    title = forms.CharField(max_length=250)
    image = forms.ImageField()


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["feedback"]
        labels = {"feedback": ""}
        widgets = {'feedback': forms.Textarea(attrs={'rows': 1})}


class MathMainForm(forms.ModelForm):
    class Meta:
        model = MathMain
        fields = ["title", "image"]


class MathUnitForm(forms.ModelForm):
    class Meta:
        model = MathUnit
        fields = ["title"]


class MathSubUnitForm(forms.ModelForm):
    class Meta:
        model = MathSubUnit
        fields = ["title", "description", "unit"]
    image = forms.ImageField(required=False)


class PhysicsMainForm(forms.ModelForm):
    class Meta:
        model = PhysicsMain
        fields = ["title", "image"]


class PhysicsUnitForm(forms.ModelForm):
    class Meta:
        model = PhysicsUnit
        fields = ["title"]


class PhysicsSubUnitForm(forms.ModelForm):
    class Meta:
        model = PhysicsSubUnit
        fields = ["title", "description", "unit"]
    image = forms.ImageField(required=False)


class ChemMainForm(forms.ModelForm):
    class Meta:
        model = ChemMain
        fields = ["title", "image"]


class ChemUnitForm(forms.ModelForm):
    class Meta:
        model = ChemUnit
        fields = ["title"]


class ChemSubUnitForm(forms.ModelForm):
    class Meta:
        model = ChemSubUnit
        fields = ["title", "description", "unit"]
    image = forms.ImageField(required=False)


class CompSciMainForm(forms.ModelForm):
    class Meta:
        model = CompSciMain
        fields = ["title", "image"]


class CompSciUnitForm(forms.ModelForm):
    class Meta:
        model = CompSciUnit
        fields = ["title"]


class CompSciSubUnitForm(forms.ModelForm):
    class Meta:
        model = CompSciSubUnit
        fields = ["title", "description", "unit"]
    image = forms.ImageField(required=False)


class MultipleChoiceQuizForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuiz
        fields = ["unit", "number_of_questions", "required_score_to_pass"]


class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ["quiz", "title"]
    image = forms.ImageField(label="solution")


class MultipleChoiceChoiceForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceChoice
        fields = ["question", "choice", "correct"]
