# Django REST Framework — Debugging Notes

A log of issues encountered and fixes applied during development of the `students` API.

---

## Issue 1: `ValueError` — Model Can't Have More Than One Auto-Generated Field

### Error

```
ValueError: Model students.Student can't have more than one auto-generated field.
```

### Cause

The `Student` model had two auto-generated fields conflicting with each other:

- Django's default `id` (BigAutoField) added automatically
- A custom `student_id = models.AutoField(primary_key=True)` field

Django only allows one auto-generated primary key per model.

### Fix

Changed `student_id` from an `AutoField` to a regular `CharField`, letting Django manage the default `id` as the primary key:

```python
# Before (caused conflict)
student_id = models.AutoField(primary_key=True)

# After (correct)
student_id = models.CharField(max_length=20, unique=True)
```

---

## Issue 2: Broken Migration Chain — `NodeNotFoundError`

### Error

```
django.db.migrations.exceptions.NodeNotFoundError: Migration students.0005_alter_student_student_id
dependencies reference nonexistent parent node ('students', '0004_student_id_alter_student_student_id')
```

### Cause

Migration `0004` was deleted manually, but `0005` still referenced it as a dependency, breaking the migration graph.

### Fix

Since this was a development environment with no production data, the cleanest solution was a full migration reset:

```bash
# 1. Delete all migration files (keep __init__.py)
find students/migrations/ -name "*.py" -not -name "__init__.py" -delete

# 2. Drop the SQLite database
rm db.sqlite3

# 3. Regenerate migrations from the current model state
python3 manage.py makemigrations
python3 manage.py migrate
```

> **Note:** Only do this in development. In production, fix the dependency reference inside the broken migration file instead of deleting everything.

---

## Issue 3: Model Code — Indentation & `__str__` Bug

### Problem

The `Student` model had broken indentation and a stray `)` in the `__str__` method:

```python
# Broken
def __str__(self):
return f"{self.name})"  # wrong indentation + extra )
```

### Fix

```python
from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    course = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"  # fixed indentation and removed stray )
```

---

## Issue 4: `AssertionError` — `DjangoModelPermissionsOrAnonReadOnly` on Function-Based View

### Error

```
AssertionError: Cannot apply DjangoModelPermissionsOrAnonReadOnly on a view that does not
set `.queryset` or have a `.get_queryset()` method.
```

### Cause

The default permission class `DjangoModelPermissionsOrAnonReadOnly` in `settings.py` only works with class-based views (like `ViewSet` or `GenericAPIView`) that expose a `queryset`. The `studentsView` was a plain function-based `@api_view`, which has no queryset.

### The View

```python
@api_view(['GET'])
def studentsView(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### Fix Applied

Changed the default permission class in `settings.py` to `IsAuthenticatedOrReadOnly`, which is compatible with both function-based and class-based views:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}
```

### Alternative Fixes (not applied)

**Option A** — Override per-view with a decorator:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def studentsView(request):
    ...
```

**Option B** — Remove all restrictions (development/testing only):

```python
@api_view(['GET'])
@permission_classes([])
def studentsView(request):
    ...
```

### Permission Class Compatibility Reference

| View Type | `DjangoModelPermissionsOrAnonReadOnly` | `IsAuthenticatedOrReadOnly` |
|---|---|---|
| `@api_view` (function-based) | ❌ Not compatible | ✅ Works |
| `GenericAPIView` / `ViewSet` | ✅ Works (needs `queryset`) | ✅ Works |

---

## Final Working State

**`students/models.py`**

```python
from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    course = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
```

**`settings.py` (REST Framework section)**

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}
```

**`api/views.py`**

```python
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def studentsView(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```