from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator , MinValueValidator
# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=100)
    institution_number = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name 

class Branch(models.Model):
    name = models.CharField(max_length=100)
    transit_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField(default="admin@enigmatix.io" , validators=[EmailValidator()])
    capacity =models.PositiveIntegerField(null=True , blank=True , validators=[MinValueValidator(0)])   
    last_modified = models.DateTimeField(auto_now=True)
    bank =models.ForeignKey(Bank , on_delete=models.CASCADE , related_name='branches')
    
    def __str__(self):
        return self.name