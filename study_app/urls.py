"""
URL configuration for study_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("math", views.math, name="math"),
    path("math/<int:id>", views.study_math, name="study_math"),
    path("physics", views.physics, name="physics"),
    path("physics/<int:id>", views.study_physics, name="study_physics"),
    path("chemistry", views.chemistry, name="chemistry"),
    path("chemistry/<int:id>", views.study_chemistry, name="study_chemistry"),
    path("comp-sci", views.compsci, name="compsci"),
    path("comp-sci/<int:id>", views.study_compsci, name="study_compsci"),
    path("feedback", views.feedback, name="feedback"),
    path("add-feedback", views.add_feedback, name="add_feedback"),
    path("feedback/<int:id>", views.feedback_delete, name="feedback_delete"),
    path("game", views.game, name="game"),
    path("test/<subject>/<unit>", views.test, name="test"),
    path("test/<subject>/<unit>/check-answer", views.test_check, name="test_check"),
    path("test/<subject>/<unit>/show-answer", views.show_answer, name="show_answer"),
    path("testing", views.testing, name="testing")
]