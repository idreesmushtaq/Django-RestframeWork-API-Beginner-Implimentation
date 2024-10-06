from django.db import models

# Create your models here.
class Country(models.Model):
    name=models.CharField(max_length=100)
    code=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}, {self.code}"

class Person(models.Model):
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE, related_name='country')
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField()
    phone=models.CharField(max_length=10)

