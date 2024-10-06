# Django-RestframeWork-API-Beginner-Implimentation

# Django REST API Project

This project is a Django-based REST API that manages `Person` and `Country` models. It includes user authentication and custom actions using Django REST Framework.

## Features

- CRUD operations for `Person` and `Country` models.
- User authentication with token-based authentication.
- Custom actions using Django REST Framework's `@action` decorator.

## Requirements

- Python 3.x
- Django 3.x or higher
- Django REST Framework

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

### Endpoints

- `GET /api/people/`: List all people.
- `POST /api/people/`: Create a new person.
- `GET /api/people/{id}/`: Retrieve a person by ID.
- `PUT /api/people/{id}/`: Update a person by ID.
- `PATCH /api/people/{id}/`: Partially update a person by ID.
- `DELETE /api/people/{id}/`: Delete a person by ID.

### Custom Actions

- `POST /api/people/{id}/custom_action/`: Perform a custom action on a person.

### Authentication

- `POST /api/login/`: Login and get an authentication token.
- `POST /api/register/`: Register a new user.

## Example Code

### views.py

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, PersonSerializer
from .models import Person
from rest_framework.decorators import action
from rest_framework import viewsets

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({'message': 'Invalid Credentials'})
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': user.username, 'message': 'Login Successful'})

class PeopleViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=True, methods=['post'])
    def custom_action(self, request, pk):
        obj = Person.objects.get(pk=pk)
        serializer = PersonSerializer(obj)
        print('This is a Email custom action')
        return Response({'message': 'The Email has been Sent', 'data': serializer.data})
