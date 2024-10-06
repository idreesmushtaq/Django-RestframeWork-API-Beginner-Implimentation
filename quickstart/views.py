from rest_framework.decorators import api_view
from rest_framework.response import Response
from quickstart.models import Person
from quickstart.serializers import PersonSerializer,LoginSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator

from rest_framework.decorators import action

#creating an api to check wether a user is a valid user or not

class LoginAPI(APIView):
    def post (self, request):
        data  = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({'message':'Invalid Credentials'})
        token,created = Token.objects.get_or_create(user = user)
        return Response({'token':token.key,'user':user.username,'message':'Login Successfull'})
    
#creating an api for user registration

class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



#making api requests using APIView class
class PersonList(APIView):
    #using authintication and permission classes to make the api secure for the users
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3
        
            paginator = Paginator(objs, page_size)
            serializer = PersonSerializer(paginator.page(page), many=True)
            print('Now the get request is working through APIView and we are able to see the data')
            return Response(serializer.data)
        except Exception as e:
            return Response({'message':'invalid page'})
    
    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('Now the post request is working through APIView and we are able to see the data')
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('Now the put request is working through APIView and we are able to see the data')

            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj ,data = data , partial=True)
        if serializer.is_valid():
            serializer.save()
            print('Now the patch request is working through APIView and we are able to see the data')

            return Response(serializer.data)
        return Response(serializer.error)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        print('Now the patch request is working through APIView and we are able to see the data')

        return Response('Deleted Successfully')
    
# making api requests using function based views
# simply checking how these methods work 
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def index(request):
    course = {
        'name': 'Django REST framework',
        'language': ['Python','javascript','tornado'],
        'course_provider': 'Professional Kashmiri',
    }
    if request.method == 'GET':

        return Response(f'we are getting the data {course}')
    elif request.method == 'POST':
        data = request.data
        print(data)
        return Response(f'we are posting the data {course}')
    elif request.method == 'PUT':
        return Response(f'we are updating the data {course}')
    elif request.method == 'PATCH':        
        return Response(f'we are partially updating the data {course}')
    elif request.method == 'DELETE':    
        return Response(f'we are deleting the data {course}')
    

# now creating a api for login validation

@api_view(['POST'])
def login (request):
    data = request.data
    serialilizer = LoginSerializer(data = data)
    if serialilizer.is_valid():
        data = serialilizer.validated_data
        # print data now to check the user input in the command line
        print(data)
        return Response('Login Successfull')

    return Response(serialilizer.errors)



# Now creating a full functional apis with database interactions
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':

        objs = Person.objects.filter(country__isnull = False,country_id__isnull = False)
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj ,data = data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error)
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response('Deleted Successfully')
        


# Now creating a viewset for the same

class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

#Creating a custom function for the viewset to search the data from the database

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer = PersonSerializer(queryset, many=True)
        return Response({'message':'200','data':serializer.data})


#creating a custom action for the viewset to perform some custom actions using action decorator
    @action(detail=True, methods=['post'])
    def custom_action(self, request, pk):
        obj = Person.objects.get(pk = pk)
        serializer = PersonSerializer(obj)
        print('This is a Email custom action')
        return Response({'message':'The Email has been Sent','data':serializer.data})