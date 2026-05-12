from django.shortcuts import render
from django.http import JsonResponse # for API endpoint
from students.models import Student

def studentsView(request):
    # json response for API endpoint
    students = Student.objects.all().values() # get all students from the database and convert to a list of dictionaries

    # convert the queryset to a list and return as JSON response
    return JsonResponse(list(students), safe=False) # safe=False allows us to return a list instead of a dictionary, which is the default expected by JsonResponse
