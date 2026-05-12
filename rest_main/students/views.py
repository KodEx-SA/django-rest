from django.shortcuts import render
from django.http import HttpResponse # for web app endpoint

def students(request): # web app endpoint
    # students = ["Ashley", "John", "Doe"]
    student = {
        "id": 1,
        "name": "Ashley",
        "age": 25,
        "course": "Computer Science"
    }
    # return HttpResponse(students)
    return HttpResponse(f"Student: {student['name']}, Age: {student['age']}, Course: {student['course']}")