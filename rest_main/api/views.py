from django.shortcuts import render

def studentsView(request):
    student = {
        "id": 1,
        "name": "Ashley",
        "age": 25,
        "grade": "A"
    }
    return render(request, 'students/student_detail.html', {'student': student})
