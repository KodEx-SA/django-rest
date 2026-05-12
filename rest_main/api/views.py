from django.shortcuts import render

def studentsView(request):
    # json response for API endpoint
    student = {
        "id": 1,
        "name": "Ashley",
        "age": 25,
        "grade": "A"
    }
    return JsonResponse(student)
