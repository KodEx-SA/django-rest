from django.url import path
from . import views

urlpatterns = [
    path('students/', views.students, name='students'),
]
