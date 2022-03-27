from django.db import models
from datetime import datetime, timedelta
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="Invalid email address"

        email_check=User.objects.filter(email=postData['email'])
        if email_check:
            errors['duplicate']="Invalid email already taken"
     
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match'
        
        return errors
    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = pw,
        )
    def authenticate(self, email, password):
        users=User.objects.filter(email=email)
        if users:
            user=users[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
            else:
                return False
        return False

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()

class ProductManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['product_name']) < 3:
            errors["product_name"] = "Product Name must have at least 3 characters."   
        if len(postData['description']) < 5:
            errors["description"] = "Description must have at least 5 characters."        
        if len(postData['condition']) == 0:
            errors["condition"] = "You must enter condition of product."
        return errors

class Product(models.Model):
    product_name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name = "products",on_delete=models.CASCADE)
    # joined = models.ManyToManyField(User, related_name = "joined_products")
    # product_img = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)            
    objects= ProductManager()