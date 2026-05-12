from django.shortcuts import render
from django.http import HttpResponse

def students(request):
    # students = ["Ashley", "John", "Doe"]
    student = {
        "name": "Ashley",
        "age": 25,
        "grade": "A"
    }
    # return HttpResponse(students)
    return HttpResponse(f"Student: {student['name']}, Age: {student['age']}, Grade: {student['grade']}")