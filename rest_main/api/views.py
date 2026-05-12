# from django.shortcuts import render
# from django.http import JsonResponse # for API endpoint

from students.models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view # for API endpoint, allows us to specify the HTTP methods allowed for the view
from rest_framework.response import Response # for API endpoint, allows us to return a Response object that can be rendered into JSON, XML, etc.
from rest_framework import status # for API endpoint, allows us to return appropriate HTTP status codes in the response

@api_view(['GET']) # specify the HTTP method allowed for this view
def studentsView(request):
    if request.method == 'GET':
        students = Student.objects.all() # get all students from the database
        serializer = StudentSerializer(students, many=True) # serialize the queryset, many=True indicates that we are serializing a queryset (multiple objects)
        return Response(serializer.data, status=status.HTTP_200_OK) # return the serialized data as a JSON response



    # json response for API endpoint
    # students = Student.objects.all().values() # get all students from the database and convert to a list of dictionaries

    # # convert the queryset to a list and return as JSON response
    # return JsonResponse(list(students), safe=False) # safe=False allows us to return a list instead of a dictionary, which is the default expected by JsonResponse
