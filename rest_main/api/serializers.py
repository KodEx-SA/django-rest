''' 
This file defines serializers for the API endpoints. 
Serializers convert complex data types, such as Django models, into native Python datatypes that can then be easily rendered into JSON, XML, 
or other content types. 
They also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data. 
'''

from rest_framework import serializers
from students.models import Student

class StudentSerializer(serializers.ModelSerializer): # define a serializer for the Student model
    class Meta: # specify the model and fields to be serialized
        model = Student
        fields = '__all__'
        # fields = ['student_id', 'name', 'age', 'course']