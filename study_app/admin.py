from django.contrib import admin
from .models import Feedback, MathMain, PhysicsMain, ChemMain, CompSciMain, MathUnit, MathSubUnit, \
    PhysicsUnit, PhysicsSubUnit, ChemUnit, ChemSubUnit, CompSciUnit, CompSciSubUnit, MultipleChoiceQuestion, \
    MultipleChoiceChoice, MultipleChoiceQuiz

class AnswerInline(admin.TabularInline):
    model = MultipleChoiceChoice

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

# Register your models here.
admin.site.register(Feedback)
admin.site.register(MathMain)
admin.site.register(PhysicsMain)
admin.site.register(ChemMain)
admin.site.register(CompSciMain)
admin.site.register(MathUnit)
admin.site.register(MathSubUnit)
admin.site.register(PhysicsUnit)
admin.site.register(PhysicsSubUnit)
admin.site.register(ChemUnit)
admin.site.register(ChemSubUnit)
admin.site.register(CompSciUnit)
admin.site.register(CompSciSubUnit)
admin.site.register(MultipleChoiceQuiz)
admin.site.register(MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(MultipleChoiceChoice)

