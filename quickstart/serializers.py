from rest_framework import serializers
from .models import Person, Country
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        if any(char in special_characters for char in data['username']):
            raise serializers.ValidationError('Username should not contain special characters')
        
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('Username already exists')
        
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email already exists')

        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],email=validated_data['email'],password=validated_data['password'])
        return user
class LoginSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password = serializers.CharField()

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name','code']

class PersonSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = Person
        #exclude = ['name','age']
        fields = '__all__'
        #depth = 1


    def validate(self, data):
        special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        if any(char in special_characters for char in data['name']):
            raise serializers.ValidationError('Name should not contain special characters')
        if data['age'] < 18:
            raise serializers.ValidationError('Age should be greater than 18')
        return data