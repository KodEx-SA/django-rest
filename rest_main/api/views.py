from django.shortcuts import render
from django.http import JsonResponse # for API endpoint

def studentsView(request):
    # json response for API endpoint
    student = {
        "id": 1,
        "name": "Ashley",
        "age": 25,
        "grade": "A"
    }
    return JsonResponse(student)
