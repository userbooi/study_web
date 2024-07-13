from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feedback(models.Model):
    feedback = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "feedback"
        verbose_name_plural = "feedbacks"

    def __str__(self):
        if len(self.feedback) > 20:
            return f"{self.feedback[:20]}..."
        else:
            return self.feedback

class MathMain(models.Model):
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to="images/")
    image = models.BinaryField(editable=True, null=False, blank=False)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class MathUnit(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=250)
    subject = models.ForeignKey(MathMain, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class MathSubUnit(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=250)
    unit = models.ForeignKey(MathUnit, on_delete=models.CASCADE)
    description = models.TextField(blank=False)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class PhysicsMain(models.Model):
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.BinaryField(editable=True, null=False, blank=False)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class PhysicsUnit(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=250)
    subject = models.ForeignKey(PhysicsMain, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class PhysicsSubUnit(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=250)
    unit = models.ForeignKey(PhysicsUnit, on_delete=models.CASCADE)
    description = models.TextField(blank=False)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class ChemMain(models.Model):
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.BinaryField(editable=True, null=False, blank=False)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class ChemUnit(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=250)
    subject = models.ForeignKey(ChemMain, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class ChemSubUnit(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=250)
    unit = models.ForeignKey(ChemUnit, on_delete=models.CASCADE)
    description = models.TextField(blank=False)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class CompSciMain(models.Model):
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.BinaryField(editable=True, null=False, blank=False)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class CompSciUnit(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=250)
    subject = models.ForeignKey(CompSciMain, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class CompSciSubUnit(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=250)
    unit = models.ForeignKey(CompSciUnit, on_delete=models.CASCADE)
    description = models.TextField(blank=False)

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

class MultipleChoiceQuiz(models.Model):
    unit = models.CharField(max_length=250)
    number_of_questions = models.IntegerField(default=4)
    required_score_to_pass = models.IntegerField(default=50)

    class Meta:
        verbose_name_plural = "multiple choice quizzes"

    def __str__(self):
        if len(self.unit) >= 45:
            return f"Test-{self.unit[:45]}..."
        else:
            return f"Test-{self.unit}"

class MultipleChoiceQuestion(models.Model):
    quiz = models.ForeignKey(MultipleChoiceQuiz, on_delete=models.CASCADE, related_name='questions')
    title = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.title) >= 50:
            return f"{self.title[:50]}..."
        else:
            return self.title

class MultipleChoiceChoice(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=150)
    correct = models.BooleanField(default=False)

    def __str__(self):
        if len(self.choice) >= 50:
            return f"{self.choice[:50]}..."
        else:
            return self.choice
